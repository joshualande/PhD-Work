""" Code to simulate W44 and fit with different spatial models

    Author: Joshua Lande <joshualande@gmail.com>
"""
from lande.fermi.likelihood.roi_gtlike import Gtlike

from os.path import join, exists
from argparse import ArgumentParser
from tempfile import mkdtemp
import shutil

import yaml
import numpy as np

from skymaps import SkyDir

from uw.like.pointspec import DataSpecification
from uw.like.roi_state import PointlikeState
from uw.like.roi_catalogs import Catalog2FGL
from uw.like.Models import PowerLaw
from uw.like.SpatialModels import EllipticalRing, EllipticalDisk, Disk, Gaussian
from uw.like.pointspec_helpers import get_default_diffuse, PointSource
from uw.like.roi_monte_carlo import SpectralAnalysisMC

from lande.fermi.likelihood.tools import force_gradient
from lande.fermi.likelihood.save import sourcedict
from lande.utilities.save import savedict

def get_catalog():
    return Catalog2FGL('$FERMI/catalogs/gll_psc_v05.fit',
                        latextdir='$FERMI/extended_archives/gll_psc_v05_templates')


def get_diffuse():
    return get_default_diffuse(diffdir='/afs/slac/g/glast/groups/diffuse/rings/2year',
                               gfile='ring_2year_P76_v0.fits',
                               ifile='isotrop_2year_P76_source_v0.txt')


def get_spatial(type):

    # Replace with analytic shape
    skydir=SkyDir(283.98999,1.355)
    major=0.3
    minor=0.19

    if type == 'Point':
        return skydir

    elif type == 'EllipticalRing':
        return EllipticalRing(major_axis=major,
                              minor_axis=minor,
                              pos_angle=-33,
                              fraction=0.75,
                              center=skydir)

    elif type == 'EllipticalDisk':
        # Similarly shaped elliptical disk
        return EllipticalDisk(major_axis=major,
                              minor_axis=minor,
                              pos_angle=-33,
                              center=skydir)

    elif type == 'Disk':
        # Simiarly shaped disk
        return Disk(sigma=np.sqrt(major*minor), center=skydir)
    
    elif type == 'Gaussian':
        # Simiarly shaped gaussian
        return Gaussian(sigma=np.sqrt(major*minor)*(Disk.x68/Gaussian.x68))

    else:
        raise Exception("...")


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("i", type=int)
    parser.add_argument("--edisp", default=False, action='store_true')
    args=parser.parse_args()
    i=args.i
    istr='%05d' % i

    np.random.seed(i)

    emin=1e3
    emax=1e5

    force_gradient(use_gradient=False)

    name='W44'
    catalog = get_catalog()
    w44_2FGL=catalog.get_source(name)

    flux = w44_2FGL.model.i_flux(emin, emax)
    w44_2FGL.model = PowerLaw(index = 2.66) # 2.66 taken from my PLaw fit for 1GeV to 100GeV
    w44_2FGL.model.set_flux(71.2e-9, emin, emax)

    # Simulate with elliptical ring spatial model predicted by 2FGL
    w44_2FGL.spatial_model = get_spatial('EllipticalRing')

    diffuse_sources = get_diffuse() + [w44_2FGL.copy()]

    tempdir=mkdtemp(prefix='/scratch/')

    ft2 = '$FERMI/data/monte_carlo/2fgl/ft2_2fgl.fits'
    ltcube = '$FERMI/data/monte_carlo/2fgl/ltcube_phibins_9.fits'

    ft1 = join(tempdir,'ft1.fits')
    binfile = join(tempdir,'binned.fits')

    ds = DataSpecification(
        ft1files = ft1,
        ft2files = ft2,
        binfile = binfile,
        ltcube = ltcube)

    size = 40
    roi_size = (size/2.0)*np.sqrt(2)

    sa = SpectralAnalysisMC(ds,
                            seed=i,
                            emin=emin,
                            emax=emax,
                            binsperdec=8,
                            event_class=0,
                            roi_dir=w44_2FGL.skydir,
                            minROI=roi_size,
                            maxROI=roi_size,
                            irf='P7SOURCE_V6',
                            zenithcut=100,
                            use_weighted_livetime=True,
                            mc_energy=(args.edisp==False),
                           )

    roi = sa.roi(
        roi_dir=w44_2FGL.skydir,
        point_sources=[],
        diffuse_sources=diffuse_sources,
    )

    likelihood_state = PointlikeState(roi)

    results = r = dict()

    results['mc'] = sourcedict(roi, name, errors=False)

    print roi

    def fit(type):
        spatial_model = get_spatial(type)
        print 'Fitting %s with %s spatial model' % (name,type)

        roi.modify(which=name, spatial_model=spatial_model)
        likelihood_state.restore(just_spectra=True)

        roi.fit()
        if isinstance(roi.get_source(name), PointSource):
            roi.localize(which=name, update=True)
        else:
            roi.fit_extension(which=name)
        roi.fit()
        roi.print_summary(galactic=True)
        results[type] = dict(pointlike=sourcedict(roi,name))

        gtlike = Gtlike(roi, 
                        enable_edisp=(args.edisp==True),
                        binsz=0.05,
                        chatter=4,
                        minbinsz=0.05,
                        rfactor=2,
                       )
        like = gtlike.like
        like.fit(covar=True)
        results[type]['gtlike'] = sourcedict(like,name)

        savedict('results_%s.yaml' % istr,results)

    hypothesis=[ 'Point', 'Disk', 'Gaussian', 'EllipticalDisk', 'EllipticalRing']
    np.random.shuffle(hypothesis)
    for h in hypothesis: fit(h)


shutil.rmtree(tempdir)

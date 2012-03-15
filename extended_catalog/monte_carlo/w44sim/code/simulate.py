""" Code to simulate W44 and fit with different spatial models

    Author: Joshua Lande <joshualande@gmail.com>
"""
from os.path import join, exists
from argparse import ArgumentParser
from tempfile import mkdtemp
import shutil

import yaml
import numpy as np

from skymaps import SkyDir

from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.roi_state import PointlikeState
from uw.like.roi_catalogs import Catalog2FGL
from uw.like.Models import PowerLaw
from uw.like.SpatialModels import EllipticalRing, EllipticalDisk, Disk, Gaussian
from uw.like.pointspec_helpers import get_default_diffuse, PointSource
from uw.like.roi_monte_carlo import SpectralAnalysisMC

from lande.fermi.data.catalogs import dict2fgl
from lande.fermi.likelihood.tools import force_gradient
from lande.fermi.likelihood.save import sourcedict
from lande.utilities.tools import savedict

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
    args=parser.parse_args()
    i=args.i
    istr='%05d' % i

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

    ft2 = dict2fgl['ft2']
    ltcube = dict2fgl['ltcube']


    ft1 = join(tempdir,'ft1.fits')
    binfile = join(tempdir,'binned.fits')

    ds = DataSpecification(
        ft1files = ft1,
        ft2files = ft2,
        binfile = binfile,
        ltcube = ltcube)

    sa = SpectralAnalysisMC(ds,
                            seed=i,
                            emin=emin,
                            emax=emax,
                            binsperdec=8,
                            event_class=0,
                            roi_dir = w44_2FGL.skydir,
                            minROI=10,
                            maxROI=10,
                            irf='P7SOURCE_V6')

    roi = sa.roi(
        roi_dir=w44_2FGL.skydir,
        point_sources=[],
        diffuse_sources=diffuse_sources,
    )

    likelihood_state = PointlikeState(roi)

    results = r = dict()

    results['mc'] = sourcedict(roi, name, errors=False)
    results['mc']['r68'] = roi.get_source('W44').spatial_model.numeric_r68()

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
        results[type] = sourcedict(roi,name)

        if type != 'Point':
            results[type]['r68'] = spatial_model.numeric_r68()

        savedict('results_%s.yaml' % istr,results)

    fit('Point')
    fit('Disk')
    fit('Gaussian')
    fit('EllipticalDisk')
    fit('EllipticalRing')

shutil.rmtree(tempdir)

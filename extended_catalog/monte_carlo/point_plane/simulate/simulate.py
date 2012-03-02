""" Code to simulate W44 and fit with different spatial models

    Author: Joshua Lande <joshualande@gmail.com>
"""
from os.path import join, exists
from argparse import ArgumentParser
from tempfile import mkdtemp

import yaml
import numpy as np

from skymaps import SkyDir

from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.roi_state import PointlikeState
from uw.like.SpatialModels import EllipticalRing, EllipticalDisk, Disk, Gaussian
from uw.like.pointspec_helpers import get_default_diffuse, PointSource
from uw.like.roi_monte_carlo import MonteCarlo

from lande.fermi.likelihood.tools import force_gradient
force_gradient(use_gradient=False)

from lande.fermi.likelihood.save import sourcedict
from lande.utilities.tools import tolist

parser = ArgumentParser()
parser.add_argument("i", type=int)
args=parser.parse_args()
i=args.i
istr='%05d' % i



emin=1e3
emax=1e5

irf='P7SOURCE_V6'

roi_dir = choose_roi_randomly()

diffuse=get_default_diffuse(diffdir='/afs/slac/g/glast/groups/diffuse/rings/2year',
                                      gfile='ring_2year_P76_v0.fits',
                                      ifile='isotrop_2year_P76_source_v0.txt')


savedir='savedir'

mc_kwargs = dict(
    seed=i,
    irf=irf,
    roi_dir=skydir,
    ft2=ft2,
    maxROI=10,
    emin=emin,
    emax=emax,
    gtifile=ltcube)

ft1_diffuse = join(savedir,'ft1_diffuse.fits')
mc=MonteCarlo(
    sources=diffuse,
    ft1=ft1_diffuse,
    **mc_kwargs)
mc.simulate()

for index,flux in [[1.5, 1e-8],
                   [2.0, 3e-8],
                   [2.5, 1e-7]
                   [3.0, 3e-7]]:

    model_mc = PowerLaw(index=index)
    model_mc.set_flux(flux, 1e2, 1e5)

    point = PointSource(name=name, model=model_mc, skydir=skydir)

    ft1_point = join(savedir,'ft1_point.fits')
    mc=MonteCarlo(
        sources=point,
        ft1=ft1_point,
        **mc_kwargs)
    mc.simulate()


    # Simulate with elliptical ring spatial model predicted by 2FGL
    w44_2FGL.spatial_model = get_spatial('EllipticalRing')


    binfile = join(savedir,'binned.fits')
    ds = DataSpecification(
        ft1files = [ft1_point, ft1_diffuse],
        ft2files = ft2,
        binfile = binfile,
        ltcube = ltcube)

    sa = SpectralAnalysis(ds,
                          emin=emin,
                          emax=emax,
                          binsperdec=4,
                          event_class=0,
                          roi_dir = w44_2FGL.skydir,
                          minROI=10,
                          maxROI=10,
                          irf=irf)

    roi = sa.roi(
        point_sources=[point],
        diffuse_sources=diffuse,
    )

    results = r = dict()

    results['mc'] = sourcedict(roi, name, errors=False)

    roi.fit()
    roi.localize(which=name, update=True)
    roi.fit()

    results['point'] = sourcedict(roi, name, errors=False)

    roi.modify(which=name, spatial_model=Disk(sigma=.1))


    roi.fit()
    roi.localize(which=name, update=True)
    roi.fit()

    print roi

    def fit(type):
        spatial_model = get_spatial(type)
        print 'Fitting %s with %s spatial model' % (name,type)

        roi.modify(which=name, spatial_model=spatial_model)
        likelihood_state.restore(just_spectra=True)

        roi.fit()
        if isinstance(roi.get_source(name), PointSource):
        else:
            roi.fit_extension(which=name)
        roi.fit()
        roi.print_summary(galactic=True)
        results[type] = sourcedict(roi,name)

        open('results_%s.yaml' % istr,'w').write(yaml.dump(tolist(results)))

    fit('Point')
    fit('Disk')
    fit('Gaussian')
    fit('EllipticalDisk')
    fit('EllipticalRing')

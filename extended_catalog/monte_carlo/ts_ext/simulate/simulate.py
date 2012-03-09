""" Code to simulate W44 and fit with different spatial models

    Author: Joshua Lande <joshualande@gmail.com>
"""
from os.path import join, exists
from argparse import ArgumentParser
from tempfile import mkdtemp

import yaml
import numpy as np

from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.roi_state import PointlikeState
from uw.like.SpatialModels import EllipticalRing, EllipticalDisk, Disk, Gaussian
from uw.like.pointspec_helpers import get_default_diffuse, PointSource
from uw.like.roi_monte_carlo import MonteCarlo

from lande.fermi.likelihood.tools import force_gradient
force_gradient(use_gradient=False)

from lande.fermi.likelihood.save import sourcedict
from lande.utilities.tools import savedict

parser = ArgumentParser()
parser.add_argument("i", type=int)
args=parser.parse_args()
i=args.i
istr='%05d' % i

emin=1e3
emax=1e5

irf='P7SOURCE_V6'

while True:
    roi_dir=random_on_sphere()
    if abs(roi_dir.b()) < 5:
        break

results = dict()

for index,flux in [[1.5, 1e-8], [2.0, 3e-8], [2.5, 1e-7] [3.0, 3e-7]]:

    tempdir = mkdtemp(prefix='/scratch/')


    model_mc = PowerLaw(index=index)
    model_mc.set_flux(flux, 1e2, 1e5)


    ft1 = join(tempdir,'ft1_point.fits')
    binfile = join(tempdir,'binned.fits')
    ds = DataSpecification(
        ft1files = [ft1, ft1],
        ft2files = ft2,
        binfile = binfile,
        ltcube = ltcube)

    sa = SpectralAnalysisMC(ds,
                            emin=emin,
                            emax=emax,
                            binsperdec=8,
                            event_class=0,
                            roi_dir = roi_dir,
                            minROI=10,
                            maxROI=10,
                            irf=irf,
                            seed=i)

    point = PointSource(name=name, model=model_mc, skydir=roi_dir)

    diffuse=get_default_diffuse(diffdir='/afs/slac/g/glast/groups/diffuse/rings/2year',
                                gfile='ring_2year_P76_v0.fits',
                                ifile='isotrop_2year_P76_source_v0.txt')

    roi = sa.roi(
        roi_dir = roi_dir,
        point_sources=[point],
        diffuse_sources=diffuse,
    )

    r = dict()
    results.append()

    r['mc'] = sourcedict(roi, name, errors=False)

    roi.fit()
    roi.localize(which=name, update=True)
    roi.fit()

    r['point'] = sourcedict(roi, name, errors=False)

    roi.modify(which=name, spatial_model=Disk(sigma=.1))

    roi.fit()
    roi.fit_extension(which=name_mc, estimate_errors=False)
    roi.fit()


    r['extended'] = sourcedict(roi, name, errors=False)

    r['extended']['ts_ext']=roi.TS_ext(which=name_mc)

    savedict('results_%s.yaml' % istr,results)

    shutil.rmtree(tempdir)


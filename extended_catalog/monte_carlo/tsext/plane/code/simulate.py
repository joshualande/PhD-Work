""" Code to simulate W44 and fit with different spatial models

    Author: Joshua Lande <joshualande@gmail.com>
"""
import shutil
from os.path import join, exists
from argparse import ArgumentParser
from tempfile import mkdtemp

import yaml
import numpy as np

from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.roi_state import PointlikeState
from uw.like.SpatialModels import EllipticalRing, EllipticalDisk, Disk, Gaussian
from uw.like.pointspec_helpers import get_default_diffuse, PointSource
from uw.like.roi_monte_carlo import SpectralAnalysisMC
from uw.like.Models import PowerLaw

from lande.fermi.likelihood.tools import force_gradient
force_gradient(use_gradient=False)

from uw.like.roi_analysis import ROIAnalysis
from lande.utilities.decorators import warn_on_exception

ROIAnalysis.fit = warn_on_exception(ROIAnalysis.fit)
ROIAnalysis.localize = warn_on_exception(ROIAnalysis.localize)
ROIAnalysis.fit_extensions = warn_on_exception(ROIAnalysis.fit_extension)

from lande.fermi.likelihood.save import sourcedict
from lande.utilities.tools import savedict
from lande.utilities.random import random_on_sphere


parser = ArgumentParser()
parser.add_argument("i", type=int)
args=parser.parse_args()
i=args.i
istr='%05d' % i

emin=1e3
emax=1e5

irf='P7SOURCE_V6'

np.random.seed(i)

while True:
    roi_dir=random_on_sphere()
    if abs(roi_dir.b()) < 5:
        break

results = []


# v1:
# indices_and_fluxes = [[1.5, 1e-8], [2.0, 3e-8], [2.5, 1e-7], [3.0, 3e-7]]

# v2: 
#indices_and_fluxes = [[1.5, 3e-9], [2.0, 2e-8], [2.5, 1e-7], [3.0, 5e-7]]

# v3:
indices_and_fluxes = [[1.5, 7e-9], [2.0, 3e-8], [2.5, 1e-7], [3.0, 5e-7]]

np.random.shuffle(indices_and_fluxes)
for index,flux in indices_and_fluxes:

    name = 'source_flux_%g_index_%g' % (flux,index)

    tempdir = mkdtemp(prefix='/scratch/')


    model_mc = PowerLaw(index=index)
    model_mc.set_flux(flux, 1e2, 1e5)


    ft1 = join(tempdir,'ft1.fits')
    binfile = join(tempdir,'binned.fits')
    ft2 = join(tempdir, 'ft2.fits')
    ltcube = join(tempdir, 'ltcube.fits')
    ds = DataSpecification(
        ft1files = ft1,
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
                            seed=i,
                            tstart=0,
                            tstop=31556926,
                            ltfrac=0.8,
                           )

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

    r['mc'] = sourcedict(roi, name, errors=False, emin=1e2, emax=1e5)


    roi.fit()
    roi.localize(which=name, update=True)
    roi.fit()

    r['point'] = sourcedict(roi, name, errors=False)

    roi.modify(which=name, spatial_model=Disk(sigma=.1))

    roi.fit()
    roi.fit_extension(which=name, estimate_errors=False)
    roi.fit()


    r['extended'] = sourcedict(roi, name, errors=False)

    r['extended']['TS_ext']=roi.TS_ext(which=name)

    results.append(r)
    savedict('results_%s.yaml' % istr,results)

    shutil.rmtree(tempdir)


#!/usr/bin/env python
from lande.fermi.likelihood.roi_gtlike import Gtlike

from argparse import ArgumentParser
import shutil
from tempfile import mkdtemp
from os.path import join

import yaml
import numpy as np

from skymaps import SkyDir

from uw.like.roi_monte_carlo import SpectralAnalysisMC
from uw.like.pointspec import DataSpecification
from uw.like.pointspec_helpers import PointSource
from uw.like.Models import PowerLaw
from uw.like.roi_state import PointlikeState

from lande.fermi.likelihood.diffuse import get_sreekumar
from lande.fermi.likelihood.save import sourcedict
from lande.fermi.data.catalogs import dict2fgl
from lande.utilities.random import random_on_sphere
from lande.utilities.save import savedict


parser = ArgumentParser()
parser.add_argument("i", type=int)
args= parser.parse_args()

i=args.i
istr='%05d' % i

np.random.seed(i)

roi_dir = SkyDir(0,0,SkyDir.GALACTIC)
name='source'

emin=1e2
emax=1e5

model_mc = PowerLaw(index=2)
model_mc.set_flux(1e-5, emin=emin, emax=emax)

sreekumar = get_sreekumar()
ps = PointSource(name=name, model=model_mc, skydir=roi_dir)

tempdir='savedir'

ds = DataSpecification(
    ft1files = join(tempdir,'ft1.fits'),
    ft2files = dict2fgl['ft2'],
    ltcube = dict2fgl['ltcube'],
    binfile = join(tempdir,'binned.fits'))

sa = SpectralAnalysisMC(ds,
                        binsperdec=8,
                        emin = emin,
                        emax = emax,
                        irf='P7SOURCE_V6',
                        roi_dir=roi_dir,
                        minROI=10,
                        maxROI=10,
                        seed=i,
                        mc_energy=True,
                        savedir=tempdir,
                       )

roi = sa.roi(roi_dir=roi_dir, 
             point_sources=[ps],
             diffuse_sources=[sreekumar])
state = PointlikeState(roi)

results = dict(
    i = i,
    istr = istr)

mc=sourcedict(roi, name)

roi.print_summary()
roi.fit(use_gradient=False)
roi.print_summary()

fit=sourcedict(roi, name)

results['pointlike'] = dict(mc=mc, fit=fit)

state.restore()

gtlike = Gtlike(roi, bigger_roi=True)
like = gtlike.like

mc=sourcedict(like, name)

like.fit(covar=True)

fit = sourcedict(like, name)

results['gtlike'] = dict(mc=mc, fit=fit)

savedict('results_%s.yaml' % istr, results)

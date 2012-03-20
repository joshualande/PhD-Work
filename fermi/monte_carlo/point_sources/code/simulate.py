#!/usr/bin/env python
from lande.fermi.likelihood.roi_gtlike import Gtlike

from argparse import ArgumentParser
import shutil
from tempfile import mkdtemp
from os.path import join

import yaml
import numpy as np

from skymaps import SkyDir

from uw.like.Models import Constant
from uw.like.roi_monte_carlo import SpectralAnalysisMC
from uw.like.pointspec import DataSpecification
from uw.like.roi_state import PointlikeState


from lande.fermi.likelihood.fit import logLikelihood
from lande.fermi.likelihood.diffuse import get_background, get_sreekumar
from lande.fermi.likelihood.save import diffusedict, skydirdict
from lande.fermi.data.catalogs import dict2fgl
from lande.utilities.random import random_on_sphere
from lande.utilities.save import savedict


parser = ArgumentParser()
parser.add_argument("i", type=int)
args= parser.parse_args()

i=args.i
istr='%05d' % i

np.random.seed(i)

difftype=args.difftype

roi_dir = SkyDir(0,0,SkyDir.GALACTIC)
name='source'

emin=emin
emax=emax

model_mc = PowerLaw(index=index)
model_mc.set_flux(1e-8, emin=emin, emax=emax)

sreekumar = get_sreekumar()
ps = PointSource(name=name, model=model_mc, skydir=roi_dir)

tempdir=mkdtemp(prefix='/scratch/')

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
                       )

roi = sa.roi(roi_dir=roi_dir, 
             point_sources=[ps],
             diffuse_sources=[sreekumar])

results = dict(
    i = i,
    istr = istr)

mc=sourcedict(roi)

ll_0 = logLikelihood(roi)

roi.print_summary()
roi.fit(use_gradient=False)
roi.print_summary()
ll_1 = logLikelihood(roi)

fit=diffusedict(roi)
results['pointlike'] = dict(mc=mc, fit=fit, ll_0=ll_0, ll_1=ll_1)

state.restore(just_spectra=True)

gtlike = Gtlike(roi, bigger_roi=True)
like = gtlike.like

mc=diffusedict(like)
ll_0=logLikelihood(like)

like.fit(covar=True)

fit = diffusedict(like)
ll_1 = logLikelihood(like)

results['gtlike'] = dict(mc=mc, fit=fit, ll_0=ll_0, ll_1=ll_1)

savedict('results_%s.yaml' % istr, results)

shutil.rmtree(tempdir)

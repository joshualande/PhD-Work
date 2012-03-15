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
from lande.utilities.tools import savedict


parser = ArgumentParser()
parser.add_argument("i", type=int)
parser.add_argument("--difftype", required=True, choices=['galactic', 'isotropic', 'sreekumar'])
parser.add_argument("--emin", required=True, type=float)
parser.add_argument("--emax", required=True, type=float)
parser.add_argument("--location", required=True, choices=['highlat','lowlat'])
args= parser.parse_args()

i=args.i
istr='%05d' % i

np.random.seed(i)

difftype=args.difftype
location=args.location
emin=args.emin
emax=args.emax

diffdir='/afs/slac/g/glast/groups/diffuse/rings/2year/'

iso = get_background(join(diffdir,'isotrop_2year_P76_source_v0.txt'))
ring = get_background(join(diffdir,'ring_2year_P76_v0.fits'))
sreekumar = get_sreekumar(diff_factor=1)

if difftype == 'galactic':
    for p in iso.smodel.param_names: iso.smodel.freeze(p)
    ring.smodel = Constant()
    diffuse_sources = [iso, ring]
elif difftype == 'isotropic':
    diffuse_sources = [iso ]
elif difftype == 'sreekumar':
    diffuse_sources = [sreekumar]

tempdir=mkdtemp(prefix='/scratch/')



if location == 'highlat':
 log_basedir = "/afs/slac/g/glast/groups/catalog/P7_V4_SOURCE"
 log_basedir = "/afs/slac/g/glast/groups/catalog/P7_V4_SOURCE"
 while True:
        roi_dir=random_on_sphere()
        if roi_dir.l() > 10:
            break
elif location == 'lowlat':
    while True:
        roi_dir=random_on_sphere()
        if roi_dir.l() <= 10:
            break

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

roi = sa.roi(roi_dir=roi_dir, diffuse_sources = diffuse_sources)

state = PointlikeState(roi)

results = dict(
    i = i,
    istr = istr,
    difftype=difftype,
    location=location,
    roi_dir=skydirdict(roi_dir),
    emin=emin,
    emax=emax)

mc=diffusedict(roi)
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

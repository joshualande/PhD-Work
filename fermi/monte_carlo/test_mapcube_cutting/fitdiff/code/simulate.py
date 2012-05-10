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


from lande.fermi.likelihood.save import logLikelihood
from lande.fermi.likelihood.diffuse import get_background, get_sreekumar
from lande.fermi.likelihood.save import diffusedict, skydirdict
from lande.fermi.data.catalogs import dict2fgl
from lande.utilities.random import random_on_sphere
from lande.utilities.save import savedict


parser = ArgumentParser()
parser.add_argument("i", type=int)
parser.add_argument("--difftype", required=True, choices=['galactic', 'isotropic', 'sreekumar'])
parser.add_argument("--emin", required=True, type=float)
parser.add_argument("--emax", required=True, type=float)
parser.add_argument("--time", required=True, choices=['2fgl', '1day', '2years'])
parser.add_argument("--position", required=True, choices=['highlat','lowlat', 'galcenter', 'allsky', ])
args= parser.parse_args()

i=args.i
istr='%05d' % i

np.random.seed(i)

difftype=args.difftype
time=args.time
position=args.position
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

if position == 'highlat':
    while True:
        roi_dir=random_on_sphere()
        if roi_dir.l() > 10:
            break
elif position == 'lowlat':
    while True:
        roi_dir=random_on_sphere()
        if roi_dir.l() <= 10:
            break
elif position == 'galcenter':
    roi_dir = SkyDir(0,0,SkyDir.GALACTIC)
elif position == 'allsky':
    roi_dir = random_on_sphere()
else:
    raise Exception("Unrecognized position %s" % position)


if time == '2years':
    ft2 = join(tempdir,'ft2.fits')
    ltcube = join(tempdir,'ltcube.fits')
    tstart=0
    tstop=63113851.9 # 2 years
    ltfrac=0.9
if time == '1day':
    ft2 = join(tempdir,'ft2.fits')
    ltcube = join(tempdir,'ltcube.fits')
    tstart=0
    tstop=86400,
    ltfrac=0.9
elif time == '2fgl':
    ft2 = dict2fgl['ft2']
    ltcube = dict2fgl['ltcube']
    tstart=None
    tstop=None
    ltfrac=None


ds = DataSpecification(
    ft1files = join(tempdir,'ft1.fits'),
    ft2files = ft2,
    ltcube = ltcube,
    binfile = join(tempdir,'binned.fits'))

sa = SpectralAnalysisMC(ds,
                        binsperdec=8,
                        emin = emin,
                        emax = emax,
                        irf='P7SOURCE_V6',
                        roi_dir=roi_dir,
                        minROI=10*np.sqrt(2),
                        maxROI=10*np.sqrt(2),
                        seed=i,
                        tstart=tstart,
                        tstop=tstop,
                        ltfrac=ltfrac,
                        use_weighted_livetime=True,
                        mc_energy=True,
                        zenithcut=100,
                        savedir=tempdir)

roi = sa.roi(roi_dir=roi_dir, diffuse_sources = diffuse_sources)

state = PointlikeState(roi)

results = dict(
    time=time,
    i=i,
    istr=istr,
    difftype=difftype,
    position=position,
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

gtlike = Gtlike(roi, bigger_roi=False, savedir=tempdir)
like = gtlike.like

mc=diffusedict(like)
ll_0=logLikelihood(like)

like.fit(covar=True)

fit = diffusedict(like)
ll_1 = logLikelihood(like)

results['gtlike'] = dict(mc=mc, fit=fit, ll_0=ll_0, ll_1=ll_1)

savedict('results_%s.yaml' % istr, results)

shutil.rmtree(tempdir)

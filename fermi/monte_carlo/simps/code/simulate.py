#!/usr/bin/env python
from lande.fermi.likelihood.roi_gtlike import Gtlike

from argparse import ArgumentParser
import shutil
from tempfile import mkdtemp
from os.path import join, exists

import yaml
import numpy as np

from skymaps import SkyDir

from uw.like.roi_monte_carlo import MonteCarlo
from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.pointspec_helpers import PointSource
from uw.like.Models import PowerLaw
from uw.like.roi_state import PointlikeState

from lande.fermi.likelihood.diffuse import get_sreekumar
from lande.fermi.likelihood.save import sourcedict
from lande.fermi.data.catalogs import dict2fgl
from lande.fermi.data.livetime import gtltcube
from lande.utilities.random import random_on_sphere
from lande.utilities.save import savedict


parser = ArgumentParser()
parser.add_argument("i", type=int)
parser.add_argument("--time", required=True, choices=['2fgl', '1day', '2years'])
parser.add_argument("--flux", required=True, type=float)
parser.add_argument("--position", required=True, choices=['galcenter', 'allsky' ])
parser.add_argument("--emin", required=True, type=float)
parser.add_argument("--emax", required=True, type=float)

args= parser.parse_args()

i=args.i
istr='%05d' % i

np.random.seed(i)

name='source'

flux=args.flux
position=args.position
time=args.time
emin=args.emin
emax=args.emax

if position == 'galcenter':
    roi_dir = SkyDir(0,0,SkyDir.GALACTIC)
elif position == 'allsky':
    roi_dir=random_on_sphere()

model_mc = PowerLaw(index=2)
model_mc.set_flux(flux, emin=emin, emax=emax)

ps = PointSource(name=name, model=model_mc, skydir=roi_dir)
sreekumar = get_sreekumar()

tempdir=mkdtemp(prefix='/scratch/')

if time == '1day':
    ft2 = join(tempdir,'ft2.fits')
    ltcube = join(tempdir,'ltcube.fits')
    mc_kwargs=dict(
        tstart=0,
        tstop=86400,
        ltfrac=0.9)
elif time == '2years':
    ft2 = join(tempdir,'ft2.fits')
    ltcube = join(tempdir,'ltcube.fits')
    mc_kwargs=dict(
        tstart=0,
        tstop=63113851.9,
        ltfrac=0.9)
elif time == '2fgl':
    ft2 = dict2fgl['ft2']
    ltcube = dict2fgl['ltcube']
    mc_kwargs=dict(gtifile=ltcube)

irf = 'P7SOURCE_V6'
roi_size = 10*np.sqrt(2)
ft1 = join(tempdir,'ft1.fits')

if not exists(ft1):
    mc = MonteCarlo(
        ft1=ft1,
        ft2=ft2,
        sources=[ps,sreekumar],
        emin=emin,
        emax=emax,
        irf=irf,
        maxROI=roi_size,
        savedir=tempdir,
        seed=i,
        **mc_kwargs)
    mc.simulate()

if not exists(ltcube):
    gtltcube(evfile=ft1, scfile=ft2, outfile=ltcube, dcostheta=0.025, binsz=1)

ds = DataSpecification(
    ft1files = ft1,
    ft2files = ft2,
    ltcube = ltcube,
    binfile = join(tempdir,'binned.fits'))

sa = SpectralAnalysis(ds,
                      binsperdec=8,
                      emin = emin,
                      emax = emax,
                      irf=irf,
                      event_class=0,
                      roi_dir=roi_dir,
                      minROI=roi_size,
                      maxROI=roi_size,
                      use_weighted_livetime=True,
                     )

roi = sa.roi(roi_dir=roi_dir, 
             point_sources=[ps],
             diffuse_sources=[sreekumar],
            )
state = PointlikeState(roi)

results = dict(
    i = i,
    position = position,
    time = time,
    emin = emin,
    emax = emax,
    istr = istr)

mc=sourcedict(roi, name)

roi.print_summary()
roi.fit(use_gradient=False)
roi.print_summary()

fit=sourcedict(roi, name)

results['pointlike'] = dict(mc=mc, fit=fit)

state.restore()

gtlike = Gtlike(roi, binsz=1/8., bigger_roi=False, 
                enable_edisp=True, fix_pointlike_ltcube=True)
like = gtlike.like

mc=sourcedict(like, name)

like.fit(covar=True)

fit = sourcedict(like, name)

results['gtlike'] = dict(mc=mc, fit=fit)

savedict('results_%s.yaml' % istr, results)

shutil.rmtree(tempdir)

#!/usr/bin/env python
from lande.fermi.likelihood.roi_gtlike import Gtlike, UnbinnedGtlike

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
from uw.like.SpatialModels import Disk
from uw.like.roi_state import PointlikeState
from uw.like.roi_extended import ExtendedSource

from lande.fermi.likelihood.save import sourcedict
from lande.fermi.data.catalogs import dict2fgl
from lande.fermi.data.livetime import gtltcube
from lande.utilities.random import random_on_sphere
from lande.utilities.save import savedict


parser = ArgumentParser()
parser.add_argument("i", type=int)
parser.add_argument("--time", required=True, choices=['2fgl', '1day', '2years'])
parser.add_argument("--flux", required=True, type=float)
parser.add_argument("--position", required=True, choices=['galcenter', 'allsky', 'bad', 'pole' ])
parser.add_argument("--emin", required=True, type=float)
parser.add_argument("--emax", required=True, type=float)
parser.add_argument("--phibins", required=True, type=int)
parser.add_argument("--savedata", default=False, action='store_true')
parser.add_argument("--spatial", required=True, choices=['point', 'disk'])
parser.add_argument("--irf", required=True)

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
phibins=args.phibins
spatial=args.spatial
irf=args.irf

if position == 'galcenter':
    roi_dir = SkyDir(0,0,SkyDir.GALACTIC)
elif position == 'allsky':
    roi_dir=random_on_sphere()
elif position == 'bad':
    roi_dir=SkyDir(314.4346,-69.5670,SkyDir.GALACTIC)
elif position == 'pole':
    roi_dir=SkyDir(0,-90,SkyDir.GALACTIC)

model_mc = PowerLaw(index=2)
model_mc.set_flux(flux, emin=emin, emax=emax)

if spatial == 'point':
    ps = PointSource(name=name, model=model_mc, skydir=roi_dir)
elif spatial == 'disk':
    spatial_model = Disk(sigma=0.5, center=roi_dir)
    ps = ExtendedSource(name=name, model=model_mc, spatial_model=spatial_model)

if args.savedata:
    tempdir='savedir'
else:
    tempdir=mkdtemp(prefix='/scratch/')

if time == '1day':
    ft2 = '$FERMI/data/monte_carlo/1day/ft2_1day.fits'
    ltcube = '$FERMI/data/monte_carlo/1day/ltcube_phibins_%d.fits' % phibins
elif time == '2years':
    ft2 = '$FERMI/data/monte_carlo/2years/ft2_2years.fits'
    ltcube = '$FERMI/data/monte_carlo/2years/ltcube_phibins_%d.fits' % phibins
elif time == '2fgl':
    ft2 = '$FERMI/data/monte_carlo/2fgl/ft2_2fgl.fits'
    ltcube = '$FERMI/data/monte_carlo/2fgl/ltcube_phibins_%d.fits' % phibins

roi_size = 10*np.sqrt(2)
ft1 = join(tempdir,'ft1.fits')

if not exists(ft1):
    mc = MonteCarlo(
        ft1=ft1,
        ft2=ft2,
        sources=[ps],
        emin=emin,
        emax=emax,
        irf=irf,
        maxROI=roi_size,
        savedir=tempdir,
        seed=i,
        mc_energy=True,
        gtifile=ltcube)
    mc.simulate()

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
                      zenithcut=100,
                     )

roi = sa.roi(roi_dir=roi_dir, 
             point_sources=[ps],
             diffuse_sources=None,
            )
state = PointlikeState(roi)

results = dict(
    i = i,
    position = position,
    time = time,
    emin = emin,
    emax = emax,
    istr = istr,
    phibins = phibins,
    irf = irf,
    spatial = spatial)

mc=sourcedict(roi, name, save_TS=False, errors=False)

roi.print_summary()
roi.fit(use_gradient=False)
roi.print_summary()

fit=sourcedict(roi, name, save_TS=False)

results['pointlike'] = dict(mc=mc, fit=fit)

state.restore()

gtlike = Gtlike(roi, savedir=tempdir)
like = gtlike.like

mc=sourcedict(like, name, save_TS=False)

like.fit(covar=True)

fit = sourcedict(like, name, save_TS=False)

results['gtlike'] = dict(mc=mc, fit=fit)

savedict('results_%s.yaml' % istr, results)

if not args.savedata:
    shutil.rmtree(tempdir)
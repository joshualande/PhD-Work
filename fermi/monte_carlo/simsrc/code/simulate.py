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
from uw.like.SpatialModels import Disk, EllipticalRing
from uw.like.roi_state import PointlikeState
from uw.like.roi_extended import ExtendedSource

from lande.fermi.likelihood.save import sourcedict

from lande.fermi.data.catalogs import dict2fgl
from lande.utilities.random import random_on_sphere
from lande.utilities.save import savedict, argparse_kwargs


parser = ArgumentParser()
parser.add_argument("i", type=int)
parser.add_argument("--time", required=True, choices=['2fgl', '1day', '2years'])
parser.add_argument("--flux", required=True, type=float)
parser.add_argument("--index", required=True, type=float)
parser.add_argument("--position", required=True, choices=['galcenter', 'allsky', 'bad', 'pole', 'w44' ])
parser.add_argument("--emin", required=True, type=float)
parser.add_argument("--emax", required=True, type=float)
parser.add_argument("--phibins", required=True, type=int)
parser.add_argument("--savedata", default=False, action='store_true')
parser.add_argument("--spatial", required=True, choices=['point', 'disk', 'w44'])
parser.add_argument("--irf", required=True)
parser.add_argument("--binsz", required=True, type=float)
parser.add_argument("--minbinsz", required=True, type=float)
parser.add_argument("--size", required=True, type=float)
parser.add_argument("--rfactor", required=True, type=float)

args= parser.parse_args()

i=args.i
istr='%05d' % i

np.random.seed(i)

name='source'

flux=args.flux
index=args.index
phibins=args.phibins

if args.position == 'galcenter':
    roi_dir = SkyDir(0,0,SkyDir.GALACTIC)
elif args.position == 'allsky':
    roi_dir=random_on_sphere()
elif args.position == 'bad':
    roi_dir=SkyDir(314.4346,-69.5670,SkyDir.GALACTIC)
elif args.position == 'pole':
    roi_dir=SkyDir(0,-90,SkyDir.GALACTIC)
elif args.position == 'w44':
    roi_dir=SkyDir(283.98999,1.355)

model_mc = PowerLaw(index=index)
model_mc.set_flux(flux, emin=args.emin, emax=args.emax)

if args.spatial == 'point':
    ps = PointSource(name=name, model=model_mc, skydir=roi_dir)
    point_sources, diffuse_sources = [ps],None
    sources = [ps]
elif args.spatial == 'disk':
    spatial_model = Disk(sigma=0.25, center=roi_dir)
    es = ExtendedSource(name=name, model=model_mc, spatial_model=spatial_model)
    point_sources, diffuse_sources = [],[es]
    sources = [es]
elif args.spatial == 'w44':
    spatial_model = EllipticalRing(major_axis=.3, minor_axis=0.19, pos_angle=-33, fraction=0.75, center=roi_dir)
    es = ExtendedSource(name=name, model=model_mc, spatial_model=spatial_model)
    point_sources, diffuse_sources = [],[es]
    sources = [es]

if args.savedata:
    simdir='simdir'
    fitdir='fitdir'
else:
    simdir=fitdir=mkdtemp(prefix='/scratch/')

if args.time == '1day':
    ft2 = '$FERMI/data/monte_carlo/1day/ft2_1day.fits'
    ltcube = '$FERMI/data/monte_carlo/1day/ltcube_phibins_%d.fits' % args.phibins
elif args.time == '2years':
    ft2 = '$FERMI/data/monte_carlo/2years/ft2_2years.fits'
    ltcube = '$FERMI/data/monte_carlo/2years/ltcube_phibins_%d.fits' % args.phibins
elif args.time == '2fgl':
    ft2 = '$FERMI/data/monte_carlo/2fgl/ft2_2fgl.fits'
    ltcube = '$FERMI/data/monte_carlo/2fgl/ltcube_phibins_%d.fits' % args.phibins

roi_size = (args.size/2.)*np.sqrt(2)
ft1 = join(simdir,'ft1.fits')

if not exists(ft1):
    mc = MonteCarlo(
        ft1=ft1,
        ft2=ft2,
        sources=sources,
        emin=args.emin,
        emax=args.emax,
        irf=args.irf,
        maxROI=roi_size,
        savedir=simdir,
        seed=i,
        mc_energy=True,
        gtifile=ltcube,
        zmax=100)
    mc.simulate()

ds = DataSpecification(
    ft1files = ft1,
    ft2files = ft2,
    ltcube = ltcube,
    binfile = join(simdir,'binned.fits'))

sa = SpectralAnalysis(ds,
                      binsperdec=8,
                      emin = args.emin,
                      emax = args.emax,
                      irf=args.irf,
                      event_class=0,
                      roi_dir=roi_dir,
                      minROI=roi_size,
                      maxROI=roi_size,
                      use_weighted_livetime=True,
                      zenithcut=100,
                     )

roi = sa.roi(roi_dir=roi_dir, 
             point_sources=point_sources,
             diffuse_sources=diffuse_sources,
            )
state = PointlikeState(roi)

results = r = dict(argparse_kwargs(args))

mc=sourcedict(roi, name, save_TS=False, errors=False)

roi.print_summary()
roi.fit(use_gradient=False)
roi.print_summary()

fit=sourcedict(roi, name, save_TS=False)

results['pointlike'] = dict(mc=mc, fit=fit)

state.restore()

gtlike = Gtlike(roi, savedir=fitdir, 
                binsz=args.binsz, 
                minbinsz=args.minbinsz, 
                rfactor=args.rfactor, 
                resample="no", 
                chatter=4)
like = gtlike.like

mc=sourcedict(like, name, save_TS=False)

like.fit(covar=True)

fit = sourcedict(like, name, save_TS=False)

results['gtlike'] = dict(mc=mc, fit=fit)

savedict('results_%s.yaml' % istr, results)

if not args.savedata:
    shutil.rmtree(simdir)

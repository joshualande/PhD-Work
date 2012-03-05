#!/usr/bin/env python

from argparse import ArgumentParser
import shutil
from tempfile import mkdtemp
from os.path import join

import yaml
import numpy as np

from skymaps import SkyDir

from uw.like.roi_monte_carlo import SpectralAnalysisMC
from uw.like.pointspec import DataSpecification
from uw.like.pointspec_helpers import get_default_diffuse


from lande.fermi.likelihood.diffuse import get_background, get_sreekumar
from lande.fermi.likelihood.save import diffusedict, skydirdict
from lande.fermi.likelihood.catalogs import get_2fgl
from lande.utilities.random import random_on_sphere
from lande.utilities.tools import tolist


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
if difftype == 'galactic':
    diffuse_sources = get_default_diffuse(diffdir=diffdir,
                                          gfile='ring_2year_P76_v0.fits',
                                          ifile='isotrop_2year_P76_source_v0.txt')
elif difftype == 'isotropic':
    diffuse_sources = [get_background(join(diffdir,'isotrop_2year_P76_source_v0.txt'))]
elif difftype == 'sreekumar':
    diffuse_sources = [get_sreekumar(diff_factor=1)]


tempdir=mkdtemp(prefix='/scratch/')

catdict = get_2fgl()


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
    ft2files = catdict['ft2'],
    ltcube = catdict['ft1'],
    binfile = join(tempdir,'binned.fits'))


sa = SpectralAnalysisMC(ds,
    emin = emin,
    emax = emax,
    irf='P7SOURCE_V6',
    roi_dir=roi_dir,
    minROI=10,
    maxROI=10,
    seed=i,
)

roi = sa.roi(roi_dir=roi_dir, diffuse_sources = diffuse_sources)

roi.print_summary()
roi.fit(use_gradient=False)
roi.print_summary()

results = dict(
    diffuse=diffusedict(roi),
    difftype=difftype,
    location=location,
    bin_edges=roi.bin_edges,
    roi_dir=skydirdict(roi_dir))

savedict('results_%s.yaml' % istr, results)

shutil.rmtree(tempdir)

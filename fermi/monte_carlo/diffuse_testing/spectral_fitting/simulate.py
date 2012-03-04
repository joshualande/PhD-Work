#!/usr/bin/env python

from argparse import ArgumentParser
import shutil
from tempfile import mkdtemp
from os.path import join

import yaml
import numpy as np

from skymaps import SkyDir

from uw.like.pointspec_helpers import get_default_diffuse
from uw.like.roi_monte_carlo import SpectralAnalysisMC
from uw.like.pointspec import DataSpecification


from lande.fermi.likelihood.diffuse import get_background, get_sreekumar
from lande.fermi.likelihood.save import diffusedict, skydirdict
from lande.utilities.random import random_on_sphere


parser = ArgumentParser()
parser.add_argument("i", type=int)
parser.add_argument("--difftype", required=True, choices=['galactic', 'isotropic', 'sreekumar'])
parser.add_argument("--emin", required=True)
parser.add_argument("--emax", required=True)
parser.add_argument("--location", required=True, choices=['highlat','lowlat'])
args= parser.parse_args()

i=args.i
istr='%05d' % i

np.random.seed(i)

difftype=args.difftype
location=args.location
emin=1e4
emax=1e5

diffdir='/afs/slac/g/glast/groups/diffuse/rings/2year/'
if difftype == 'galactic':
    diffuse_sources = [get_background(join(diffdir,'ring_2year_P76_v0.fits')),
                       get_background(join(diffdir,'isotrop_2year_P76_source_v0.txt'))]
elif difftype == 'isotropic':
    diffuse_sources = [get_background(join(diffdir,'isotrop_2year_P76_source_v0.txt'))]
elif difftype == 'sreekumar':
    diffuse_sources = [get_sreekumar(diff_factor=1)]


tempdir=mkdtemp(prefix='/scratch/')
catalog_basedir = "/afs/slac/g/glast/groups/catalog/P7_V4_SOURCE"


if location == 'highlat':
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
    ft2files = join(catalog_basedir,"ft2_2years.fits"),
    ltcube = join(catalog_basedir,"ltcube_24m_pass7.4_source_z100_t90_cl0.fits"),
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

roi.fit()

roi.print_summary()

results = dict(
    diffuse=diffusedict(roi),
    difftype=difftype,
    location=location,
    roi_dir=skydirdict(roi_dir))

open('results_%s.yaml' % istr, 'w').write(yaml.dump(results))

shutil.rmtree(tempdir)

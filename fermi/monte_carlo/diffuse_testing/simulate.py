#!/usr/bin/env python

from os.path import join

from skymaps import SkyDir

from uw.like.pointspec_helpers import get_default_diffuse
from uw.like.roi_monte_carlo import MonteCarlo

from lande.fermi.likelihood.diffuse import get_background, get_sreekumar

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("difftype",required=True, choices=['galactic', 'isotropic', 'sreekumar'])
parser.add_argument("emin",required=True)
parser.add_argument("emax",required=True)
parser.add_argument("location",required=True, choices=['on_plane','off_plane'])
args= parser.parse_args()

difftype=args.difftype
emin=1e2
emax=1e3

def get_diffuse(difftype):
    if difftype == 'galactic':
        return get_background('/afs/slac/g/glast/groups/diffuse/rings/2year/ring_2year_P76_v0.fits')
    elif difftype == 'isotropic':
        return get_background('/afs/slac/g/glast/groups/diffuse/rings/2year/isotrop_2year_P76_source_v0.txt')
    elif difftype == 'sreekumar':
        return get_sreekumar(diff_factor=1)

catalog_basedir = "/afs/slac/g/glast/groups/catalog/P7_V4_SOURCE"
ft2 = join(catalog_basedir,"ft2_2years.fits")
ltcube = join(catalog_basedir,"ltcube_24m_pass7.4_source_z100_t90_cl0.fits")

tempdir
ft1 = join(savedir,'ft1.fits')


#skydir=SkyDir(125,75,SkyDir.GALACTIC)
skydir=SkyDir(55,85,SkyDir.GALACTIC)

mc=MonteCarlo(
    sources=diffuse,
    seed=0,
    irf='P7SOURCE_V6',
    ft1=ft1,
    ft2=ft2,
    roi_dir=skydir,
    maxROI=10,
    emin=emin,
    emax=emax,
    gtifile=ltcube)
mc.simulate()



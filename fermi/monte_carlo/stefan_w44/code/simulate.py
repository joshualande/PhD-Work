from os.path import join
import shutil
import os
from os.path import expandvars
from argparse import ArgumentParser
import numpy as np
from skymaps import SkyDir
from uw.utilities.xml_parsers import parse_sources
from uw.like.Models import FileFunction, ProductModel, Constant
from uw.like.roi_catalogs import Catalog2FGL
from uw.like.pointspec_helpers import get_default_diffuse
from uw.like.roi_monte_carlo import MonteCarlo


parser = ArgumentParser()
parser.add_argument("i", type=int)
parser.add_argument("--spectrum", required=True, choices=['SmoothBrokenPowerLaw', 'DoubleBrokenSmoothPowerlaw'])
args= parser.parse_args()

spectrum = args.spectrum
i = args.i
istr = '%05d' % i

emin=10
emax=1e6

ft2='/u/gl/bechtol/disk/drafts/radio_quiet/36m_gtlike/trial_v1/ft2-30s_239557414_334152027.fits'
ltcube = '/u/gl/funk/data/GLAST/ExtendedSources/NewAnalysis/gtlike/W44/ltcube_239557414_334152002.fits'
ft1 = 'simulated_ft1.fits'

ps,ds=parse_sources('/u/gl/funk/data/GLAST/ExtendedSources/NewAnalysis/gtlike/W44/ExploreSources/W44_fitted_BINNED_freeClose.PlusP.xml')
sources = ps + ds

d = {s.name:s for s in sources}

# Fix diffuse components
iso = d['iso_p7v6source'] 
iso.smodel['Scale'] = 1
gal = d['gal_2yearp7v6_v0']
gal.smodel['Norm'] = 1
gal.smodel['Index'] = 1

w44 = d['2FGL J1855.9+0121e']

print 'Before flux for w44',w44.model.i_flux(1e2,1e5)

if spectrum == 'LogParabola':
    # w44 in xml is already log parabola
    pass
elif spectrum == 'FileFunction':
    file = join(expandvars('$stefan_w44_code'), 'W44_pi0_model_gtobssim.dat')
    w44.model = ProductModel(Constant(scale=1e-4),FileFunction(file=file))

else:
    raise Exception("...")

print 'After flux used to simulate w44',w44.model.i_flux(1e2,1e5)

irf='P7SOURCE_V6'
mc=MonteCarlo(
    sources=sources,
    seed=i,
    irf=irf,
    ft1=ft1,
    ft2=ft2,
    roi_dir=w44.skydir,
    maxROI=15,
    emin=emin,
    emax=emax,
    gtifile=ltcube,
    savedir='gtobssim_output')
mc.simulate()




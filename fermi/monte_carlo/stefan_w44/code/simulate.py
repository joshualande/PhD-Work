from os.path import join
import shutil
import os
from os.path import expandvars
from argparse import ArgumentParser
import numpy as np
from skymaps import SkyDir
from uw.utilities.xml_parsers import parse_sources, write_sources
from uw.like.Models import SmoothBrokenPowerLaw, SmoothDoubleBrokenPowerLaw
from uw.like.roi_catalogs import Catalog2FGL
from uw.like.pointspec_helpers import get_default_diffuse
from uw.like.roi_monte_carlo import MonteCarlo


parser = ArgumentParser()
parser.add_argument("i", type=int)
parser.add_argument("--spectrum", required=True, choices=['SmoothBrokenPowerLaw', 'SmoothDoubleBrokenPowerLaw'])
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

d = {s.name:s for s in ds}

# Fix diffuse components
iso = d['iso_p7v6source'] 
iso.smodel['Scale'] = 1
gal = d['gal_2yearp7v6_v0']
gal.smodel['Norm'] = 1
gal.smodel['Index'] = 1

w44 = d['2FGL J1855.9+0121e']

catalog = Catalog2FGL('$FERMI/catalogs/gll_psc_v05.fit',
                      latextdir='$FERMI/extended_archives/gll_psc_v05_templates')
catalog_w44 = catalog.get_source('W44')

print 'Before flux for w44',w44.model.i_flux(1e2,1e5)

if spectrum == 'SmoothBrokenPowerLaw':
    w44.model = SmoothDoubleBrokenPowerLaw(
        scale=2e8,
        index1=1.711,
        index=1.711,
        breakvalue12=217,
        beta12=0.03,
        index3=2.85,
        breakvalue23=1723,
        beta23=0.2,
    )
elif spectrum == 'SmoothDoubleBrokenPowerLaw':
    w44.model = SmoothDoubleBrokenPowerLaw(
        scale=2e8,
        index1=0.024,
        index=1.711,
        breakvalue12=217,
        beta12=0.03,
        index3=2.85,
        breakvalue23=1723,
        beta23=0.2,
    )
    w44.model = SmoothDoubleBrokenPowerLaw()

else:
    raise Exception("...")

w44.model.set_flux(catalog_w44.model.i_flux(emin=100,emax=1e5),emin=100,emax=1e5)

print 'After flux used to simulate w44',w44.model.i_flux(1e2,1e5)

write_sources(ps,ds,'gtlike_model.xml')

irf='P7SOURCE_V6'
mc=MonteCarlo(
    sources=ps+ds,
    seed=i,
    irf=irf,
    ft1=ft1,
    ft2=ft2,
    roi_dir=w44.skydir,
    maxROI=15,
    emin=emin,
    emax=emax,
    energy_pad=1,
    gtifile=ltcube,
    savedir='gtobssim_output')
mc.simulate()




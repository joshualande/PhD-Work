from os.path import join
import shutil
import os
from os.path import expandvars
from argparse import ArgumentParser
import numpy as np
from skymaps import SkyDir
from uw.utilities.xml_parsers import parse_sources, write_sources
from uw.like.Models import PowerLaw, SmoothBrokenPowerLaw, FileFunction
from uw.like.roi_catalogs import Catalog2FGL
from uw.like.pointspec_helpers import get_default_diffuse
from uw.like.roi_monte_carlo import MonteCarlo


parser = ArgumentParser()
parser.add_argument("i", type=int)
parser.add_argument("--source", required=True, choices=['W44', 'IC443'])
parser.add_argument("--spectrum", required=True, choices=['PowerLaw', 'SmoothBrokenPowerLaw'])
parser.add_argument("--debug", default=False, action='store_true')
parser.add_argument("--normalization", choices=['standard','same_flux','same_prefactor'])
args= parser.parse_args()

i = args.i
istr = '%05d' % i
source = args.source
spectrum = args.spectrum

emin=10
emax=1e6

ft2='/u/gl/bechtol/disk/drafts/radio_quiet/36m_gtlike/trial_v1/ft2-30s_239557414_334152027.fits'
ft1 = 'simulated_ft1.fits'

catalog = Catalog2FGL('/afs/slac/g/glast/groups/catalog/2FGL/gll_psc_v05.fit',
                      latextdir='/afs/slac/g/glast/groups/catalog/2FGL/gll_psc_v05_templates')

if source == 'W44':
    skydir = SkyDir(284.005,1.345)
    gtifile = '/u/gl/funk/data/GLAST/ExtendedSources/NewAnalysis/gtlike/W44/sel_W44_60_100000.fits'
elif source == 'IC443':
    skydir = SkyDir(94.310,22.580)
    gtifile = '/u/gl/funk/data/GLAST/ExtendedSources/NewAnalysis/gtlike/IC443/sel_IC443_60_100000.fits'


ds = get_default_diffuse(
    diffdir="/nfs/slac/g/ki/ki03/lande/fermi/diffuse/",
    gfile="gal_2yearp7v6_v0.fits",
    ifile="iso_p7v6source.txt")

ds[1].smodel = FileFunction(file='/nfs/slac/g/ki/ki03/lande/fermi/diffuse/iso_p7v6source_extrapolated.txt')

ps,ds = catalog.merge_lists(skydir, radius=15, user_diffuse_list=ds)

d = {s.name:s for s in ds}

if source == 'W44':
    W44 = d['W44']
    """ SmoothBrokenPowerlaw spectrum is from:
            /u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/W44/SmoothBrokenPowerlaw/W44_fitted_BINNED_PlusP_BSP_lowEnergy.fewer.minos.xml

        <spectrum type="SmoothBrokenPowerLaw">
          <parameter error="1.874888615" free="1" max="100" min="0" name="Prefactor" scale="1e-10" value="14.56863965" />
          <parameter error="0.7738550805" free="1" max="4" min="-2" name="Index1" scale="1" value="1.504042874" />
          <parameter free="0" max="2000" min="30" name="Scale" scale="1" value="200" />
          <parameter error="0.04177558875" free="1" max="-1" min="-5" name="Index2" scale="1" value="-1.891184873" />
          <parameter error="9.888298037" free="1" max="1000" min="80" name="BreakValue" scale="1" value="204.3216401" />
          <parameter free="0" max="10" min="0.01" name="Beta" scale="1" value="0.1" />
        </spectrum>
    """
    smooth = SmoothBrokenPowerLaw(
        Norm=14.56863965e-10,
        Index_1=-1.504042874,
        Index_2=1.891184873,
        E_break=204.3216401,
        beta=0.1,
        e0=200)

    if spectrum == 'PowerLaw':
        W44.model = PowerLaw(index=1.891184873, e0=200)

        if args.normalization == 'same_flux':
            W44.model.set_flux(smooth.i_flux(emin=60, emax=2000), emin=60, emax=2000)
        elif args.normalization == 'same_prefactor':
            W44.model.set_prefactor(smooth(3e3),3e3)
        else:
            raise Exception("...")

    else:
        if args.normalization != 'standard':
            raise Exception("...")
        W44.model = smooth


elif source == 'IC443':
    """
    SmoothBrokenPowerlaw Spectrum is from:
        /u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/IC443/SmoothBrokenPowerlaw/IC443_fitted_BINNED_freeMore_BSP_lowEnergy.minos.xml

        <spectrum type="SmoothBrokenPowerLaw">
          <parameter error="1.436546639" free="1" max="1e+10" min="0" name="Prefactor" scale="1e-10" value="12.16848844" />
          <parameter error="0.3813522051" free="1" max="5" min="-2" name="Index1" scale="1" value="-0.2252356061" />
          <parameter free="0" max="2000" min="30" name="Scale" scale="1" value="200" />
          <parameter error="0.02788546588" free="1" max="-1" min="-3" name="Index2" scale="1" value="-1.898928336" />
          <parameter error="25.01445784" free="1" max="1000" min="100" name="BreakValue" scale="1" value="224.1244843" />
          <parameter free="0" max="10" min="0.01" name="Beta" scale="1" value="0.1" />
        </spectrum>
    """
    IC443 = d['IC443']

    smooth = SmoothBrokenPowerLaw(
        Norm=12.16848844e-10,
        Index_1=0.225235606,
        Index_2=1.898928336,
        E_break=224.1244843,
        beta=0.1,
        e0=200)

    if spectrum == 'PowerLaw':
        IC443.model = PowerLaw(index=1.891184873, e0=200)

        if args.normalization == 'same_flux':
            IC443.model.set_flux(smooth.i_flux(emin=60, emax=2000), emin=60, emax=2000)
        elif args.normalization == 'same_prefactor':
            IC443.model.set_prefactor(smooth(3e3),3e3)
        else:
            raise Exception("...")

    else:
        if args.normalization != 'standard':
            raise Exception("...")
        IC443.model = smooth

if args.debug:
    ps = []
    ds = [j for j in ds if j.name == source]

write_sources(ps,ds,'gtlike_model.xml', convert_extended=True, expand_env_vars=True)

irf='P7SOURCE_V6'
mc=MonteCarlo(
    sources=ps+ds,
    seed=i,
    irf=irf,
    ft1=ft1,
    ft2=ft2,
    gtifile=gtifile,
    roi_dir=skydir,
    maxROI=15,
    zmax=100,
    emin=emin,
    emax=emax,
    energy_pad=1,
    savedir='gtobssim_output' if i==0 else None)
mc.simulate()




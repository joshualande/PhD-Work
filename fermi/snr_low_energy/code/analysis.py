from lande.fermi.likelihood.roi_gtlike import Gtlike

import argparse
import math
import os
from os.path import expandvars, join

import numpy as np
import yaml

from skymaps import SkyDir

from uw.like.pointspec import DataSpecification
from uw.like.roi_catalogs import Catalog2FGL
from uw.like.pointspec_helpers import get_default_diffuse
from uw.like.pointspec import SpectralAnalysis
from uw.like.roi_save import load
from uw.like.Models import PowerLaw
from uw.like.Models import SmoothBrokenPowerLaw
from uw.like.SpatialModels import Disk
from uw.like.roi_state import PointlikeState

from lande.fermi.likelihood.tools import force_gradient
from lande.fermi.likelihood.save import sourcedict
from lande.fermi.sed.supersed import SuperSED
from lande.fermi.sed.pointlike import pointlike_sed_to_yaml

# Make numpy shut up because otherwise it is very annoying
np.seterr(all='ignore')

# This code tells pointlike to never use the analytic gradient
force_gradient(use_gradient=False)

results = dict()

parser = argparse.ArgumentParser(description='Specify certain choices for the data analysis.')
parser.add_argument('--source', choices=['ic443','w44'])
args = parser.parse_args()

source=args.source


extra = 'source_%s' % source

print 'Analyzing with pointlike...'

ft2='/u/gl/bechtol/disk/drafts/radio_quiet/36m_gtlike/trial_v1/ft2-30s_239557414_334152027.fits'

if name == 'W44':
    ft1='/u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/W44/SmoothBrokenPowerlaw/W44-ft1.fits'
    ltcube='/u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/W44/ltcube_239557414_334152002.fits'

elif name == 'IC443':
    ft1='u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/IC443/SmoothBrokenPowerlaw/IC443-ft1.fits'
    ltcube='/u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/IC443/ltcube_239557414_334152002.fits'

elif name == 'W51C':
    ft1='u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/W51C/SmoothBrokenPowerlaw/W51C-ft1.fits'
    ltcube='/u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/W51C/ltcube_239557414_334152002.fits'

ds = DataSpecification(
        ft1files=ft1,
        ft2files=ft2,
        ltcube=,
        binfile='binned.fits')

diffuse_sources = get_default_diffuse(
        diffdir=expandvars('$diffuse'),
        gfile="gal_2yearp7v6_v0.fits",
        ifile="iso_p7v6source.txt")

catalog = Catalog2FGL(expandvars('$catalogs/gll_psc_v06.fit'),
        latextdir=expandvars('$catalogs/gll_psc_v06_templates'),
        free_radius=10,
)

sa = SpectralAnalysis(ds,
        emin = emin,
        emax = emax,
        binsperdec=binsperdec,
        roi_dir=casa_dir,
        minROI=minROI,
        maxROI=maxROI,
        event_class=0,
        conv_type = conv_type,
        custom_irf_dir=custom_irf_dir,
        irf=irf)


# finally, we can build the ROI for LAT analysis
roi=sa.roi(
    catalogs=catalog,
    diffuse_sources=diffuse_sources,
    fit_emin = emin,
    fit_emax = emax,
)

name='cas_a'
roi.modify(which='2FGL J2323.4+5849', name=name)

if specmodel=='powerlaw':
    #modify in the ROI the spectral model of your source
    # keep_old_flux means that the overall flux of the new spectral model 
    # will be normalized to be the same as the overall flux of the old spectral model
    roi.modify(which=name, model=PowerLaw(index=2), keep_old_flux=True)
    print 'fitting with Power Law model'
elif specmodel=='sbpl':
    #use spectral model SmoothBrokenPowerLaw
    model=SmoothBrokenPowerLaw(beta=0.1);
    roi.modify(which=name, model=model, keep_old_flux=True)
    print 'fitting with Smooth Broken Power Law'
else:
    print 'fitting with logparabola'

# print out the ROI
roi.print_summary(galactic=True)

# ROIs can be saved for later analysis
roi.save('original_roi.dat')
#
# ROI has been made
#----------------------------------------------------------------
if localization_fit:
    #localization fit
    roi.localize(which=name,update=True)
    results['localization']=roi.get_ellipse()
    roi.save('original_roi.dat')
    #extension test
    state=PointlikeState(roi)
    roi.modify(which=name,spatial_model=Disk(sigma=0.1),keep_old_center=True)
    roi.fit()
    roi.fit_extension(which=name)
    roi.fit()
    ts_ext=roi.TS_ext(which=name)
    results['extension_ts']=ts_ext
    state.restore()
    
#----------------------------------------------------------------
#Do fitting and other analysis here
#
#roi.modify(which='2FGL J2333.3+6237',free=False)
#roi.modify(which='2FGL J2249.1+5758',free=False)
#roi.modify(which='2FGL J2257.5+6222c',free=False)
# print ROI, Perform a spectral fit, print again
roi.print_summary()
roi.fit()
roi.print_summary()

# Get out the paramters for Cas A and save them to a file
results['pointlike'] = sourcedict(roi, name)
save()

roi.save('fitted_roi.dat')

if do_plots:
    # Make the residual TS map
    roi.plot_tsmap(size=mapsize, filename='tsmap.pdf', fitsfile='tsmap.fits')

    # Plot a counts map
    roi.plot_counts_map(filename='counts_map.pdf')

    # Plot a smoothed diffuse-emission-subtracted counts map
    roi.plot_sources(which=name, filename='sources.pdf')

    # Plot the SED
    pointlike_sed_to_yaml(roi.plot_sed(which=name, filename='sed_pointlike.pdf'),'sed_pointlike.yaml')


################################################################################################
print 'Analyzing with gtlike...'

roi1=load('original_roi.dat')
if fast:
    binsize=1/8.
else:
    binsize=1/16.
# to convert from pointlike to gtlike
#gtlike = Gtlike(roi1, binsz=binsize, enable_edisp=True, bigger_roi=False, savedir='cached_data')
gtlike = Gtlike(roi1, binsz=binsize, bigger_roi=False, savedir='cached_data')
like=gtlike.like
like.fit(covar=True)

if do_plots:
    # Here, put the gtlike SED code
    sed = SuperSED(like, name=name, always_upper_limit=True, min_ts=9, freeze_background=freeze_background, verbosity=4)
    sed.plot('sed_gtlike.pdf')
    sed.save('sed_gtlike.yaml')

    if not fast:
        #bin_edges=[1e2,10**2.25,10**2.5,10**2.75,1e3,10**3.25,10**3.5,10**3.75,1e4,10**4.25,10**4.5,10**4.75,1e5]
        bin_esges=np.logspace(2,5,13)
        sed4 = SuperSED(like, name=name, always_upper_limit=True, min_ts=9, freeze_background=freeze_background, 
        bin_edges=bin_edges, verbosity=4)
        sed4.plot('sed4_gtlike.pdf')
        sed4.save('sed4_gtlike.yaml')

        #bin_edges=[1e2,10**2.5,1e3,10**3.5,1e4,10**4.5,1e5]
        bin_edges=np.logspace(2,5,7)
        sed2 = SuperSED(like, name=name, always_upper_limit=True, min_ts=9, freeze_background=freeze_background, 
        bin_edges=bin_edges, verbosity=4)
        sed2.plot('sed2_gtlike.pdf')
        sed2.save('sed2_gtlike.yaml')

like.srcModel="gtlike_model.xml"
like.writeXml()


results['gtlike'] = sourcedict(like, name)
save()


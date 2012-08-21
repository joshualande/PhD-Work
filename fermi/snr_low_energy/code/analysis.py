from lande.fermi.likelihood.roi_gtlike import Gtlike

import argparse
from os.path import expandvars, join

import numpy as np

from skymaps import SkyDir

from uw.like.pointspec import DataSpecification,SpectralAnalysis
from uw.like.roi_catalogs import Catalog2FGL
from uw.like.pointspec_helpers import get_default_diffuse

from lande.fermi.likelihood.tools import force_gradient
from lande.fermi.likelihood.save import sourcedict
from lande.utilities.save import savedict
from lande.fermi.sed.supersed import SuperSED
from lande.fermi.sed.pointlike import pointlike_sed_to_yaml

# Make numpy shut up because otherwise it is very annoying
np.seterr(all='ignore')

# This code tells pointlike to never use the analytic gradient
force_gradient(use_gradient=False)

results = dict()

parser = argparse.ArgumentParser(description='Specify certain choices for the data analysis.')
parser.add_argument('--name', choices=['IC443','W44','W51C'])
parser.add_argument('--conv-type', type=int, required=True, choices=[0,1,-1])
parser.add_argument('--test', default=False, action='store_true')
args = parser.parse_args()

name=args.name
conv_type=args.conv_type

if args.test:
    emin=1e2
    emax=1e5
    binsperdec=2
else:
    emin=10**1.75 # 56 MeV
    emax=1e5
    binsperdec=8

save=lambda: savedict('results_%s.yaml' % name, results)


ft2='/u/gl/bechtol/disk/drafts/radio_quiet/36m_gtlike/trial_v1/ft2-30s_239557414_334152027.fits'

if name == 'W44':
    ft1='/u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/W44/SmoothBrokenPowerlaw/W44-ft1.fits'
    ltcube='/u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/W44/ltcube_239557414_334152002.fits'
    roi_dir=SkyDir(283.98999023,1.35500002)
elif name == 'IC443':
    ft1='/u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/IC443/SmoothBrokenPowerlaw/IC443-ft1.fits'
    ltcube='/u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/IC443/ltcube_239557414_334152002.fits'
    roi_dir=SkyDir(94.30999756,22.57999992)
elif name == 'W51C':
    ft1='/u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/W51C/SmoothBrokenPowerlaw/W51C-ft1.fits'
    ltcube='/u/gl/funk/data3/ExtendedSources/NewAnalysis/gtlike/W51C/ltcube_239557414_334152002.fits'
    roi_dir=SkyDir(290.81799316,14.14500046)
else:
    raise Exception("...")

ds = DataSpecification(
        ft1files=ft1,
        ft2files=ft2,
        ltcube=ltcube,
        binfile='binned_ct=%s.fits' % conv_type)

diffuse_sources = get_default_diffuse(
        diffdir=expandvars('$diffuse'),
        gfile="gal_2yearp7v6_v0.fits",
        ifile="iso_p7v6source_extrapolated.txt")

catalog = Catalog2FGL(expandvars('$catalogs/gll_psc_v07.fit'),
        latextdir=expandvars('$extended_archives/gll_psc_v07_templates'),
        free_radius=5,
)


if args.test:
    roi_size=5
else:
    roi_size=10*np.sqrt(2)

print 'conv',conv_type
sa = SpectralAnalysis(ds,
        emin = emin,
        emax = emax,
        binsperdec=binsperdec,
        roi_dir=roi_dir,
        minROI=roi_size,
        maxROI=roi_size,
        conv_type = conv_type,
        irf='P7SOURCE_V6')


# finally, we can build the ROI for LAT analysis
roi=sa.roi(
    catalogs=catalog,
    diffuse_sources=diffuse_sources,
    fit_emin = emin,
    fit_emax = emax,
)


roi.plot_counts_map(filename='counts_before.pdf')

# print out the ROI
roi.print_summary(galactic=True)
print roi

roi.fit(fit_bg_first=True)
roi.print_summary(galactic=True)
print roi

# Get out the paramters for Cas A and save them to a file
results['pointlike'] = sourcedict(roi, name)
save()


# Plot the SED
pointlike_sed_to_yaml(roi.plot_sed(which=name, filename='sed_pointlike.pdf'),'sed_pointlike.yaml')

gtlike = Gtlike(roi, binsz=1/8., bigger_roi=False, savedir='savedir', enable_edisp=True)
like=gtlike.like

like.fit(covar=True)
results['gtlike'] = sourcedict(like, name)
save()

sed = SuperSED(like, name=name, freeze_background=False)
sed.plot('sed_gtlike.pdf')
sed.save('sed_gtlike.yaml')

from argparse import ArgumentParser
from os.path import join, expandvars

from uw.like.pointspec import DataSpecification  

from uw.like.pointspec import SpectralAnalysis  
from skymaps import SkyDir  

parser = ArgumentParser()
parser.add_argument("i", type=int)
parser.add_argument("--source", required=True, choices=['W44', 'IC443'])
parser.add_argument("--spectrum", required=True, choices=['PowerLaw', 'SmoothBrokenPowerLaw'])
args= parser.parse_args()

i = args.i
istr = '%05d' % i
source = which = args.source
spectrum = args.spectrum

simdir = join("$stefan_w44_sims","v2","job_source_%s_spectrum_%s" % (source,spectrum),istr)

data_specification = DataSpecification(
    ft1files = join(simdir,"simulated_ft1.fits"),
    ft2files = "/u/gl/bechtol/disk/drafts/radio_quiet/36m_gtlike/trial_v1/ft2-30s_239557414_334152027.fits",
    ltcube   = "/u/gl/funk/data/GLAST/ExtendedSources/NewAnalysis/gtlike/W44/ltcube_239557414_334152002.fits",
    binfile  = "binned.fits")

if source == 'W44':
    roi_dir = SkyDir(284.005,1.345)
elif source == 'IC443':
    roi_dir = SkyDir(94.310,22.580)

sa = SpectralAnalysis(data_specification,
                      binsperdec = 8,
                      emin       = 10, # MeV  
                      emax       = 1e6, # MeV  
                      irf        = "P6_V3_DIFFUSE",  
                      roi_dir    = roi_dir,  
                      maxROI     = 10,
                      minROI     = 10,
                      use_weighted_livetime=True)

roi = sa.roi_from_xml(
    xmlfile=expandvars(join(simdir,"gtlike_model.xml")),
    roi_dir=roi_dir,
    fit_emin=10**1.75, # 56 MeV
    fit_emax=10**3.25, # 1778 MeV
#    fit_emin=1e2,
#    fit_emax=1e3,
)

print 'bins',roi.bin_edges

roi.print_summary(galactic=True)

"""
roi.fit(use_gradient=False)

roi.print_summary(galactic=True)
"""

roi.plot_sed(which=which,filename='sed.pdf', use_ergs=True)

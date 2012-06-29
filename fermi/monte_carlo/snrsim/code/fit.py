from lande.fermi.likelihood.roi_gtlike import Gtlike

from argparse import ArgumentParser
from os.path import join, expandvars


from skymaps import SkyDir  

from uw.like.pointspec import DataSpecification, SpectralAnalysis  
from uw.like.roi_state import PointlikeState

from lande.fermi.likelihood.save import sourcedict
from lande.utilities.save import savedict
from lande.fermi.sed.supersed import SuperSED
from lande.fermi.sed.pointlike import pointlike_sed_to_yaml


parser = ArgumentParser()
parser.add_argument("i", type=int)
parser.add_argument("--source", required=True, choices=['W44', 'IC443'])
parser.add_argument("--spectrum", required=True, choices=['PowerLaw', 'SmoothBrokenPowerLaw'])
parser.add_argument("--normalization", choices=['standard','same_flux','same_prefactor'])
parser.add_argument("--simdir", required=True)
parser.add_argument("--debug", default=False, action='store_true')
args= parser.parse_args()

i = args.i
istr = '%05d' % i
source = which = args.source
spectrum = args.spectrum
normalization = args.normalization

simdir = join(args.simdir,"job_spectrum_%s_normalization_%s_source_%s" % (spectrum,normalization,source),istr)

if source == 'W44':
    roi_dir = SkyDir(284.005,1.345)
    name = 'W44'
    ltcube = "/u/gl/funk/data/GLAST/ExtendedSources/NewAnalysis/gtlike/W44/ltcube_239557414_334152002.fits"
elif source == 'IC443':
    roi_dir = SkyDir(94.310,22.580)
    name = 'IC443'
    ltcube = "/u/gl/funk/data/GLAST/ExtendedSources/NewAnalysis/gtlike/IC443/ltcube_239557414_334152002.fits"

data_specification = DataSpecification(
    ft1files = join(simdir,"simulated_ft1.fits"),
    ft2files = "/u/gl/bechtol/disk/drafts/radio_quiet/36m_gtlike/trial_v1/ft2-30s_239557414_334152027.fits",
    ltcube   = ltcube,
    binfile  = "binned.fits")


sa = SpectralAnalysis(data_specification,
                      binsperdec = 8,
                      emin       = 10, # MeV  
                      emax       = 1e6, # MeV  
                      irf        = 'P7SOURCE_V6',
                      roi_dir    = roi_dir,  
                      maxROI     = 10,
                      event_class= 0,
                      minROI     = 10,
                      use_weighted_livetime=True)

roi = sa.roi_from_xml(
    xmlfile=expandvars(join(simdir,"gtlike_model.xml")),
    roi_dir=roi_dir,
    fit_emin=10**1.75, # 56 MeV
    fit_emax=10**3.25, # 1778 MeV
)

state=PointlikeState(roi)

results=dict()

print 'bins',roi.bin_edges

roi.print_summary(galactic=True)

results['pointlike'] = dict()
results['pointlike']['mc'] = sourcedict(roi,which,errors=False)

roi.fit(use_gradient=False, fit_bg_first = True)
results['pointlike']['fit'] = sourcedict(roi,which)

roi.print_summary(galactic=True)
print roi

roi.plot_counts_map(filename='counts_map.pdf')

roi.print_summary(galactic=True)
print roi

s=roi.plot_sed(which=which,filename='sed_pointlike.pdf', use_ergs=True)
pointlike_sed_to_yaml(s,'sed_pointlike.yaml')
roi.toXML('results_pointlike.xml')

state.restore()

gtlike = Gtlike(roi, savedir='gtlike_savedir', enable_edisp=True)
like = gtlike.like

results['gtlike'] = dict()
results['gtlike']['mc'] = sourcedict(like,name,errors=False)

like.fit(covar=True)
results['gtlike']['fit'] = sourcedict(like,name)

if args.debug: 
    # in debug mode, there is no background model,
    # so the TS is meaningless. Here, instead
    # just always plot the data points.
    sed_kwargs=dict(min_ts=float('-inf'))
else:
    sed_kwargs=dict()

sed = SuperSED(like, name=name, **sed_kwargs)
sed.save('sed_gtlike.yaml')
sed.plot('sed_gtlike.pdf')

savedict('results_%s.yaml' % name,results)
like.writeXml('results_gtlike.xml')

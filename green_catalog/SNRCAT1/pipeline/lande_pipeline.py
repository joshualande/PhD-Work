
from argparse import ArgumentParser

import yaml
import numpy as np

from lande_toolbag import tolist

from snr_setup import get_snr, setup_roi
from snr_helper import pointlike_analysis, gtlike_analysis, plots

from likelihood_tools import force_gradient

force_gradient(use_gradient=False)

parser = ArgumentParser()
parser.add_argument("--superfile", required=True)
parser.add_argument("--name", required=True)
parser.add_argument("--emin", type=float, default=1e4)
parser.add_argument("--emax", type=float, default=1e5)
parser.add_argument("--no-plots", action='store_true', default=False)
parser.add_argument("--no-gtlike", action='store_true', default=False)
args=parser.parse_args()

do_plots = not args.no_plots
do_gtlike = not args.no_gtlike


name=args.name
superfile=args.superfile

results=dict(name=name)

# *) Build the ROI
roi=setup_roi(name,superfile, fit_emin=args.emin, fit_emax=args.emax)

# get the SNR as an extended source object.

snr_radio_template = get_snr(name, superfile)
snrsize = snr_radio_template.spatial_model['sigma']

# *) modify the ROI to remove overlaping background sources. 
deleted_sources = []
for source in roi.get_sources():
    if np.degrees(source.skydir.difference(snr_radio_template.skydir)) < snrsize + 0.1:
        deleted_sources.append(roi.del_source(source))

for source in roi.get_sources():
    # Freeze the spectrum (but not flux) of all other sources in the ROI.
    if np.any(source.model.free):
        free=np.asarray([True]+[False]*(len(source.model._p)-1))
        roi.modify(which=source,free=free)

kwargs = dict(name=name, emin=args.emin, emax=args.emax, snrsize=snrsize)
plot_kwargs = dict(name=name, snrsize = snrsize, deleted_sources = deleted_sources, superfile=superfile)

def save():
    f=open('results_%s.yaml' % name,'w')
    yaml.dump(tolist(results),f)

print '\n\nAnalyze SNR with radio template\n\n'

roi.add_source(snr_radio_template)

results['radio'] = {}
results['radio']['pointlike']=pointlike_analysis(roi, hypothesis='radio', **kwargs)
save()
if do_gtlike: results['radio']['gtlike']=gtlike_analysis(roi, hypothesis='radio', upper_limit=True, **kwargs)
save()
if do_plots: plots(roi, hypothesis='radio', **plot_kwargs)

print '\n\nAnalyze SNR as point-like source\n\n'

# Best to start with initial spectral model, for convergence regions.
roi.del_source(which=name)
roi.add_source(get_snr(name, superfile, point_like=True))

results['point'] = {}
results['point']['pointlike']=pointlike_analysis(roi, hypothesis='point', localize=True, **kwargs)
save()
if do_gtlike: results['point']['gtlike']=gtlike_analysis(roi, hypothesis='point', **kwargs)
save()
if do_plots: plots(roi, hypothesis='point', **plot_kwargs)

print '\n\nAnalyze SNR as extended source\n\n'

roi.del_source(which=name)
roi.add_source(get_snr(name, superfile))

results['extended'] = {}
results['extended']['pointlike']=pointlike_analysis(roi, hypothesis='extended', fit_extension=True, **kwargs)
save()
if do_gtlike: results['extended']['gtlike']=gtlike_analysis(roi, hypothesis='extended', **kwargs)
save()
if do_plots: plots(roi, hypothesis='extended', **plot_kwargs)


for which in ['pointlike','gtlike']:
    try:
        results['extended'][which]['ts_ext'] = \
                2*(results['extended'][which]['logLikelihood'] - \
                   results['point'][which]['logLikelihood'])
    except:
        pass

save()


from argparse import ArgumentParser

import yaml
import numpy as np

from toolbag import tolist

from snr_helper import pointlike_analysis, gtlike_analysis

parser = ArgumentParser()
parser.add_argument("--snrdata", required=True)
parser.add_argument("--name", required=True)
parser.add_argument("--emin", type=float, default=1e4)
parser.add_argument("--emax", type=float, default=1e5)

args=parser.parse_args()

name=args.name
snrdata=args.snrdata
emin=args.emin
emax=args.emax

results=dict(name=name)

# *) Build the ROI
roi=setup_roi(name,snrdata, fit_emin=emin, fit_emax=emax)

# get the SNR as an extended source object.

snr_radio_template = get_snr(name, snrdata)
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


print '\n\nAnalyze SNR with radio template\n\n'

roi.add_source(snr_radio_template)

results['radio'] = {}
results['radio']['pointlike']=pointlike_analysis(roi,'radio')
results['radio']['gtlike']=gtlike_analysis(roi,upper_limit=True)

print '\n\nAnalyze SNR as point-like source\n\n'

# Best to start with initial spectral model, for convergence regions.
roi.del_source(which=name)
roi.add_source(get_snr(name, snrdata, point_like=True))

results['point'] = {}
results['point']['pointlike']=pointlike_analysis(roi,'point', localize=True)
results['point']['gtlike']=gtlike_analysis(roi)

print '\n\nAnalyze SNR as extended source\n\n'

roi.del_source(which=name)
roi.add_source(get_snr(name, snrdata))

results['extended'] = {}
results['extended']['pointlike']=pointlike_analysis(roi, 'extended', fit_extension=True)
results['extended']['gtlike']=gtlike_analysis(roi)


for which in ['pointlike','gtlike']:
    results['extended'][which]['ts_ext'] = \
            2*(results['extended'][which]['logLikelihood'] - \
               results['point'][which]['logLikelihood'])

f=open('results_%s.yaml' % name,'w')
yaml.dump(tolist(results),f)

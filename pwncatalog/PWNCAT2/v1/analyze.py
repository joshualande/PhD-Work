#!/usr/bin/env python

# This import has to come first
from analyze_helper import plots,pointlike_analysis,gtlike_analysis,save_results,plot_phaseogram,plot_phase_vs_time

import os
from glob import glob

from setup_pwn import setup_pwn,get_source
from argparse import ArgumentParser
import yaml

from collections import defaultdict
import numpy as np
np.seterr(all='ignore')

parser = ArgumentParser()
parser.add_argument("--pwndata", required=True)
parser.add_argument("-p", "--pwnphase", required=True)
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
parser.add_argument("--emin", default=1e2, type=float)
parser.add_argument("--emax", default=10**5.5, type=float)
parser.add_argument("--no-point", default=False, action="store_true")
parser.add_argument("--no-extended", default=False, action="store_true")
parser.add_argument("--no-gtlike", default=False, action="store_true")
parser.add_argument("--no-plots", default=False, action="store_true")
parser.add_argument("--no-cutoff", default=False, action="store_true")
parser.add_argument("--no-upper-limit", default=False, action="store_true")
parser.add_argument("--no-extension-upper-limit", default=False, action="store_true")
args=parser.parse_args()

do_point = not args.no_point
do_extended = not args.no_extended
do_gtlike = not args.no_gtlike
do_plots = not args.no_plots
do_cutoff = not args.no_cutoff
do_upper_limit = not args.no_upper_limit
do_extension_upper_limit = not args.no_extension_upper_limit

name=args.name
emin=args.emin
emax=args.emax

phase=yaml.load(open(args.pwnphase))[name]['phase']

print 'phase = ',phase


print 'Creating the output directories'

seddir='seds'
datadir='data'
plotdir='plots'
for dir in [seddir, datadir, plotdir]: 
    if not os.path.exists(dir): os.makedirs(dir)

print 'Making phaseogram'

ft1 = yaml.load(open(args.pwndata))[name]['ft1']
plot_phaseogram(name, ft1, phase, '%s/phaseogram_%s.png' % (plotdir,name))
plot_phase_vs_time(name, ft1, phase, '%s/phase_vs_time_%s.png' % (plotdir,name))


print 'Building the ROI'

roi=setup_pwn(name,args.pwndata, phase=phase, 
              free_radius=5, max_free=10, fit_emin=args.emin, fit_emax=args.emax,
              savedir='savedir')


from modify import modify_roi
modify_roi(name,roi)

results=r=defaultdict(lambda: defaultdict(dict))


kwargs = dict(roi=roi, name=name, 
              seddir=seddir, datadir=datadir, plotdir=plotdir,
              emin=emin, emax=emax)



r['at_pulsar']['pointlike']=pointlike_analysis(hypothesis='at_pulsar', upper_limit=do_upper_limit, 
                                               cutoff=do_cutoff, do_plots=do_plots, **kwargs)
save_results(results,name)
if do_gtlike: r['at_pulsar']['gtlike']=gtlike_analysis(hypothesis='at_pulsar', upper_limit=do_upper_limit, cutoff=do_cutoff, **kwargs)

if do_point:
    r['point']['pointlike']=pointlike_analysis(hypothesis='point', localize=True, cutoff=do_cutoff, 
                                               extension_upper_limit=do_extension_upper_limit, do_plots=do_plots, **kwargs)
    save_results(results,name)
    if do_gtlike: r['point']['gtlike']=gtlike_analysis(hypothesis='point', cutoff=do_cutoff, **kwargs)

if do_extended:
    roi.del_source(name)
    roi.add_source(get_source(name,args.pwndata, extended=True))

    r['extended']['pointlike']=pointlike_analysis(hypothesis='point', cutoff=do_cutoff, 
                                                  fit_extension=True, do_plots=do_plots, **kwargs)
    save_results(results,name)
    if do_gtlike: r['extended']['gtlike']=gtlike_analysis(hypothesis='point', cutoff=do_cutoff, **kwargs)

    for which in ['pointlike','gtlike']:
        results['extended'][which]['ts_ext'] = \
                2*(results['extended'][which]['logLikelihood'] - \
                   results['point'][which]['logLikelihood'])

save_results(results,name)

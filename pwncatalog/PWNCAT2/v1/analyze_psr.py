#!/usr/bin/env python

# This import has to come first
from analyze_helper import plots,pointlike_analysis,gtlike_analysis,save_results,plot_phaseogram,plot_phase_vs_time,all_energy
from uw.pulsar.phase_range import PhaseRange
from likelihood_tools import force_gradient

import os
from glob import glob

from setup_pwn import setup_pwn
from argparse import ArgumentParser
import yaml

from collections import defaultdict
import numpy as np
np.seterr(all='ignore')

parser = ArgumentParser()
parser.add_argument("--pwndata", required=True)
group=parser.add_mutually_exclusive_group(required=True)
group.add_argument("-p", "--pwnphase")
group.add_argument("--no-phase-cut", default=False, action="store_true")
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
parser.add_argument("--emin", default=1e2, type=float)
parser.add_argument("--binsperdec", default=4, type=int)
parser.add_argument("--localization-emin", default=1e3, type=float)
parser.add_argument("--emax", default=10**5.5, type=float)
parser.add_argument("--use-gradient", default=False, action="store_true")
parser.add_argument("--no-at-pulsar", default=False, action="store_true")
parser.add_argument("--no-point", default=False, action="store_true")
parser.add_argument("--no-extended", default=False, action="store_true")
parser.add_argument("--no-gtlike", default=False, action="store_true")
parser.add_argument("--no-plots", default=False, action="store_true")
parser.add_argument("--no-cutoff", default=False, action="store_true")
parser.add_argument("--no-upper-limits", default=False, action="store_true")
parser.add_argument("--no-seds", default=False, action="store_true")
parser.add_argument("--no-extension-upper-limits", default=False, action="store_true")
parser.add_argument("--no-savedir", default=False, action="store_true")
parser.add_argument("--max-free", default=10, type=float)
args=parser.parse_args()

do_at_pulsar = not args.no_at_pulsar
do_point = not args.no_point
do_extended = not args.no_extended
do_gtlike = not args.no_gtlike
do_plots = not args.no_plots
do_cutoff = not args.no_cutoff
do_upper_limits = not args.no_upper_limits
do_extension_upper_limits = not args.no_extension_upper_limits
do_seds = not args.no_seds

force_gradient(use_gradient=args.use_gradient)

name=args.name
emin=args.emin
localization_emin=args.localization_emin
emax=args.emax

if not all_energy(emin,emax) and do_cutoff:
    parser.error("Cutoff test can only be performed for analysis over all energy.")

if args.no_phase_cut:
    phase = PhaseRange(0,1)
else:
    phase=yaml.load(open(args.pwnphase))[name]['phase']

print 'phase = ',phase

print 'Making phaseogram'

ft1 = yaml.load(open(args.pwndata))[name]['ft1']
if not os.path.exists('plots'): os.makedirs('plots')
plot_phaseogram(name, ft1, off_pulse=phase, filename='plots/phaseogram_%s.png' % (name))
plot_phase_vs_time(name, ft1, off_pulse=phase, filename='plots/phase_vs_time_%s.png' % (name))

savedir=None if args.no_savedir else 'savedir'

def get_roi(**kwargs):
    print 'Building the ROI'
    roi=setup_pwn(name,args.pwndata, phase=phase, 
                  free_radius=5, max_free=args.max_free, fit_emin=emin, fit_emax=emax, 
                  savedir=savedir,
                  binsperdec=args.binsperdec,
                  **kwargs)

    from modify_psr import modify_roi
    modify_roi(name,roi)
    return roi

results=r=defaultdict(lambda: defaultdict(dict))
results['name']=name
results['phase']=phase

kwargs = dict(name=name, seds = do_seds, emin=emin, emax=emax)
pointlike_kwargs = kwargs.copy()
pointlike_kwargs.update(dict(localization_emin=localization_emin))
gtlike_kwargs = kwargs.copy()

save=lambda:save_results(results,name)

if do_at_pulsar:
    roi=get_roi(extended=False)
    r['at_pulsar']['pointlike']=pointlike_analysis(roi, hypothesis='at_pulsar', upper_limit=do_upper_limits, 
                                                   cutoff=do_cutoff, **pointlike_kwargs)
    save()
    if do_plots: plots(roi, name, 'at_pulsar', emin, emax)
    if do_gtlike: r['at_pulsar']['gtlike']=gtlike_analysis(roi, hypothesis='at_pulsar', upper_limit=do_upper_limits, cutoff=do_cutoff, **gtlike_kwargs)
    save()

if do_point:
    roi=get_roi(extended=False)
    r['point']['pointlike']=pointlike_analysis(roi, hypothesis='point', localize=True, cutoff=do_cutoff, 
                                               extension_upper_limit=do_extension_upper_limits, **pointlike_kwargs)
    save()
    if do_plots: plots(roi, name, 'point', emin, emax)
    if do_gtlike: r['point']['gtlike']=gtlike_analysis(roi, hypothesis='point', cutoff=do_cutoff, **gtlike_kwargs)
    save()

if do_extended:
    roi=get_roi(extended=True)

    r['extended']['pointlike']=pointlike_analysis(roi, hypothesis='extended', cutoff=do_cutoff, 
                                                  fit_extension=True, **pointlike_kwargs)
    save()
    if do_plots: plots(roi, name, 'extended', emin, emax)
    if do_gtlike: r['extended']['gtlike']=gtlike_analysis(roi, hypothesis='extended', cutoff=do_cutoff, **gtlike_kwargs)
    save()

    for which in ['pointlike','gtlike']:
        try:
            results['extended'][which]['ts_ext'] = \
                    2*(results['extended'][which]['logLikelihood'] - results['point'][which]['logLikelihood'])
        except KeyError:
            pass

save()

#!/usr/bin/env python

# This import has to come first
from analyze_helper import plots,pointlike_analysis,gtlike_analysis,save_results,all_energy


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
group=parser.add_mutually_exclusive_group(required=True)
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
parser.add_argument("--emin", default=10**4, type=float)
parser.add_argument("--emax", default=10**5.5, type=float)
parser.add_argument("--binsperdec", default=4, type=float)
parser.add_argument("--use-gradient", default=False, action="store_true")
parser.add_argument("--no-gtlike", default=False, action="store_true")
parser.add_argument("--no-plots", default=False, action="store_true")
parser.add_argument("--no-upper-limits", default=False, action="store_true")
parser.add_argument("--no-seds", default=False, action="store_true")
parser.add_argument("--no-savedir", default=False, action="store_true")
parser.add_argument("--max-free", default=10, type=float)
args=parser.parse_args()

do_gtlike = not args.no_gtlike
do_plots = not args.no_plots
do_upper_limits = not args.no_upper_limits
do_seds = not args.no_seds

force_gradient(use_gradient)

name=args.name
emin=args.emin
emax=args.emax

savedir='savedir' if not args.no_savedir else None

def get_roi(**kwargs):
    print 'Building the ROI'
    roi=setup_pwn(name,args.pwndata, 
                  free_radius=5, max_free=args.max_free, fit_emin=args.emin, fit_emax=args.emax, 
                  binsperdec=args.binsperdec,
                  savedir=savedir,
                  **kwargs)

results=r=defaultdict(lambda: defaultdict(dict))
results['name']=name

kwargs = dict(name=name, seds = do_seds, emin=emin, emax=emax)

save=lambda:save_results(results,name)

roi=get_roi(extended=False)
r['at_tev']['pointlike']=pointlike_analysis(roi, hypothesis='at_tev', upper_limit=do_upper_limits, **kwargs)
save()
if do_plots: plots(roi, name, 'at_tev', emin, emax)
if do_gtlike: r['at_tev']['gtlike']=gtlike_analysis(roi, hypothesis='at_tev', upper_limit=do_upper_limits, **kwargs)
save()

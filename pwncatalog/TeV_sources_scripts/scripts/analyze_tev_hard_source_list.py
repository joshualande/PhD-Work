#!/usr/bin/env python

# This import has to come first
from analyze_helper_hard_source_list import plots,pointlike_analysis,gtlike_analysis,save_results
from likelihood_tools import force_gradient

import os
from glob import glob

from setup_pwn_hard_source_list import setup_tev
from argparse import ArgumentParser
import yaml

from collections import defaultdict
import numpy as np
np.seterr(all='ignore')

import sys
print sys.version_info

parser = ArgumentParser()
parser.add_argument("--tevsources", required=True)
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
parser.add_argument("--emin", default=10**4, type=float)
parser.add_argument("--emax", default=10**5.5, type=float)
parser.add_argument("-i","--initialization", default="0.1")

parser.add_argument("--no-at-tev", default=False, action="store_true")
parser.add_argument("--no-point", default=False, action="store_true")
parser.add_argument("--no-extended", default=False, action="store_true")

parser.add_argument("--use-gradient", default=False, action="store_true")
parser.add_argument("--no-gtlike", default=False, action="store_true")
parser.add_argument("--no-plots", default=False, action="store_true")
parser.add_argument("--no-upper-limits", default=False, action="store_true")
parser.add_argument("--no-seds", default=False, action="store_true")
parser.add_argument("--max-free", default=10, type=float)
args=parser.parse_args()

initial=args.initialization

do_at_tev = not args.no_at_tev
do_point = not args.no_point
do_extended = not args.no_extended

do_gtlike = not args.no_gtlike
do_plots = not args.no_plots

do_upper_limits = not args.no_upper_limits
do_seds = not args.no_seds

force_gradient(use_gradient=args.use_gradient)

name=args.name
emin=args.emin
emax=args.emax
ft1 = yaml.load(open(args.tevsources))[name]['ft1']
ft2 = yaml.load(open(args.tevsources))[name]['ft2']
ltcube = yaml.load(open(args.tevsources))[name]['ltcube']

from modify_tev import *

def get_roi(**kwargs):
    print 'Building the ROI'
    roi=setup_tev(name,args.tevsources, ft1, ft2, ltcube,
                  free_radius=5, max_free=args.max_free, 
                  fit_emin=emin, fit_emax=emax, 
                  **kwargs)

    from modify_tev import modify_roi
    modify_roi(name,roi,hypothese="at_tev")
    return roi

results=r=defaultdict(lambda: defaultdict(dict))
results['name']=name

kwargs = dict(name=name, seds=do_seds, emin=emin, emax=emax)

save=lambda:save_results(results,name)
freelist=[]
if do_at_tev:
    roi=get_roi(extended=True)
    r['at_tev']['pointlike']=pointlike_analysis(roi, hypothesis='at_tev', upper_limit=do_upper_limits, **kwargs)
    save()
    if do_plots:
        plots(roi, name, 'at_tev', emin, emax, size=3.0)
        plots(roi, name, 'at_tev', emin, emax, size=5.0)
        if name=="Westerlund_2" or name=="HESS_J1026-582":
            plots(roi, name, 'at_tev', emin, emax, size=10.0)
    if do_gtlike: r['at_tev']['gtlike']=gtlike_analysis(roi, hypothesis='at_tev', upper_limit=do_upper_limits, **kwargs)
    save()

if do_point:
    roi=get_roi(extended=False)
    if len(freelist)!=0:
        from uw.like.SpatialModels import PointSource
    r['point']['pointlike']=pointlike_analysis(roi, hypothesis='point', upper_limit=do_upper_limits, localize=True, **kwargs)
    save()
    if do_plots:
        plots(roi, name, 'point', emin, emax, size=3.0)
        plots(roi, name, 'point', emin, emax, size=5.0)
        if name=="Westerlund_2" or name=="HESS_J1026-582":
            plots(roi, name, 'point', emin, emax, size=10.0)
    if do_gtlike: r['point']['gtlike']=gtlike_analysis(roi, hypothesis='point', upper_limit=do_upper_limits, **kwargs)
    save()

if do_extended:
    roi=get_roi(extended=False)
    from uw.like.SpatialModels import Gaussian, Disk
    roi.modify(which=name,spatial_model=Disk(0.1))
    r['extended']['pointlike']=pointlike_analysis(roi, hypothesis='extended', upper_limit=do_upper_limits, fit_extension=True, initial=initial, **kwargs)
    save()
    if do_plots:
        plots(roi, name, 'extended', emin, emax, size=3.0)
        plots(roi, name, 'extended', emin, emax, size=5.0)
        if name=="Westerlund_2" or name=="HESS_J1026-582":
            plots(roi, name, 'extended', emin, emax, size=10.0)
    if do_gtlike: r['extended']['gtlike']=gtlike_analysis(roi, hypothesis='extended', upper_limit=do_upper_limits, **kwargs)
    save()

    for which in ['pointlike','gtlike']:
        try:
            r['extended'][which]['ts_ext'] = \
                    2*(r['extended'][which]['logLikelihood'] - r['point'][which]['logLikelihood'])
        except KeyError:
            pass

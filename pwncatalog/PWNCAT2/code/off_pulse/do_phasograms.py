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
parser.add_argument("-r", "--roifile", required=True, help="ROI definition")
args=parser.parse_args()

name=args.name

phase=yaml.load(open(args.pwnphase))[name]['phase']
radi=yaml.load(open(args.roifile))[name]['ROI']
en=yaml.load(open(args.roifile))[name]['E']
print 'phase = ',phase




print 'Creating the output directories'

seddir='seds'
datadir='data'
plotdir='plots'
for dir in [seddir, datadir, plotdir]: 
    if not os.path.exists(dir): os.makedirs(dir)

print 'Making phaseogram'

ft1 = yaml.load(open(args.pwndata))[name]['ft1']
print ft1
print phase
print name
print radi
print en
plot_phaseogram(name, ft1, phase, '%s/phaseogram_%s.png' % (plotdir,name), emin=en, emax= 3.0e5, radius=radi)
plot_phase_vs_time(name, ft1, phase, '%s/phase_vs_time_%s.png' % (plotdir,name), emin=en, emax= 3.0e5, radius=radi)


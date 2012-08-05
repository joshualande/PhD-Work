#!/usr/bin/env python

# has to come first
from analyze_helper import gtlike_analysis,plots,save_results,plot_phaseogram,plot_phase_vs_time
from analyze_helper import import_module

import os
from argparse import ArgumentParser

import yaml

from skymaps import SkyDir

from uw.like.SpatialModels import Gaussian

from lande.fermi.likelihood.tools import force_gradient
from lande.utilities.tools import parse_strip_known_args
from lande.fermi.likelihood.variability import VariabilityTester
from lande.fermi.likelihood.models import build_gtlike_model

from analyze_psr import get_args
from setup_pwn import load_pwn


parser = ArgumentParser()
parser.add_argument("--hypothesis", required=True, choices=['at_pulsar', 'point', 'extended'])
parser.add_argument("--followup", required=True, choices=['tsmaps','plots', 'gtlike', 'variability','extul', 'temp'])
followup_args = parse_strip_known_args(parser)

hypothesis = followup_args.hypothesis
followup = followup_args.followup

args = get_args()
do_cutoff = not args.no_cutoff

force_gradient(use_gradient=args.use_gradient)

name = args.name

roi = load_pwn('roi_%s_%s.dat' % (hypothesis,name))


if followup == 'gtlike':

    modify = import_module(args.modify)
    model0=modify.cutoff_model0(name)
    model1=modify.cutoff_model1(name)

    results = {hypothesis:{}}
    results[hypothesis]['gtlike']=gtlike_analysis(roi, name=name,
                                                  max_free = args.max_free,
                                                  hypothesis=hypothesis, 
                                                  cutoff=(do_cutoff and hypothesis in ['at_pulsar', 'point']),
                                                  model0=model0,
                                                  model1=model1,
                                                 )

    save_results(results,'results_%s_%s_%s.yaml' % (name,followup,hypothesis))

if followup in ['plots','tsmaps']:

    if not os.path.exists('plots'): 
        os.makedirs('plots')

    pwndata=yaml.load(open(args.pwndata))[name]
    ft1 = pwndata['ft1']
    pulsar_position = SkyDir(*pwndata['cel'])
    phase = roi.extra['phase']
    pwnphase=roi.extra['pwnphase']

    print 'Making phaseogram'

    plot_kwargs = dict(ft1=ft1, skydir=pulsar_position, phase_range=phase, 
                       emin=pwnphase['optimal_emin'], emax=pwnphase['emax'], radius=pwnphase['optimal_radius'])
    plot_phaseogram(title='Phaseogram for %s' % name, filename='plots/phaseogram_%s.png' % name, **plot_kwargs)
    plot_phase_vs_time(title='Phase vs Time for %s' % name, filename='plots/phase_vs_time_%s.png' % name, **plot_kwargs)

    new_sources = roi.extra['new_sources']
    overlay_kwargs = dict(pulsar_position=pulsar_position, new_sources=new_sources)
    
    if followup == 'plots':
        plots(roi, name, hypothesis, do_plots=True, do_tsmap=False, **overlay_kwargs)
    elif followup == 'tsmaps':
        plots(roi, name, hypothesis, do_plots=False, do_tsmap=True, **overlay_kwargs)


elif followup == 'variability':

    roi.print_summary()
    roi.fit(use_gradient=False)
    roi.print_summary()

    v = VariabilityTester(roi,name, nbins=36)
    v.plot(filename='plots/variability_%s_hypothesis_%s.pdf' % (name,hypothesis))

    results = {hypothesis:{'variability':v.todict()}}
    save_results(results,'results_%s_%s_%s.yaml' % (name,followup,hypothesis))

elif followup == 'extul':
    print 'Calculating extension upper limit'

    r=roi.extension_upper_limit(which=name, confidence=0.95, spatial_model=Gaussian)
    results = {hypothesis:{'pointlike':{'extension_upper_limit':r}}}
    save_results(results,'results_%s_%s_%s.yaml' % (name,followup,hypothesis))

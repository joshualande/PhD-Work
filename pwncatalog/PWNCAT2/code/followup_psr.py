#!/usr/bin/env python

from analyze_psr import get_args()
from setup_pwn import load_pwn


parser = ArgumentParser()
parser.add_argument("--hypothesis", required=True, choice=['at_pulsar', 'point', 'extended'])
parser.add_argument("--followup", required=True, choice=['plots', 'gtlike', 'variability'])
group=parser.parse_known_args(required=True)

hypothesis = args.hypothesis
followup = args.followup

args = get_args()
do_upper_limits = not args.no_upper_limits
do_cutoff = not args.no_cutoff

name = args.name

gtlike_kwargs = dict(name=name, seds = do_seds)

roi = load_pwn('roi_%s_%s.dat' % (hypothesis,name))


if followup == 'gtlike':
    results = dict(hypothesis=dict())
    ul = (hypothesis == 'at_pulsar') and do_upper_limits
    r[hypothesis]['gtlike']=gtlike_analysis(roi, hypothesis=hypothesis, upper_limit=ul, cutoff=do_cutoff, **gtlike_kwargs)

    save_results(results,name, hypothesis=hypothesis, followup=followup)

elif followup == 'plots':

    if not os.path.exists('plots'): os.makedirs('plots')

    pwndata=yaml.load(open(args.pwndata))[name]
    ft1 = pwndata['ft1']
    pulsar_position = SkyDir(*pwndata['cel'])

    print 'Making phaseogram'

    plot_kwargs = dict(ft1=ft1, skydir=pulsar_position, phase_range=phase, 
                       emin=pwnphase['optimal_emin'], emax=pwnphase['emax'], radius=pwnphase['optimal_radius'])
    plot_phaseogram(title='Phaseogram for %s' % name, filename='plots/phaseogram_%s.png' % name, **plot_kwargs)
    plot_phase_vs_time(title='Phase vs Time for %s' % name, filename='plots/phase_vs_time_%s.png' % name, **plot_kwargs)


    new_sources = roi.extra['new_sources']
    overlay_kwargs = dict(pulsar_position=pulsar_position, new_sources=new_sources)
    if do_plots: plots(roi, name, hypothesis, **overlay_kwargs)

elif followup == 'variability':

    roi.print_summary()
    roi.fit(use_gradient=False)
    roi.print_summary()

    v = VariabilityTester(roi,name, nbins=36)
    v.plot(filename='variability_%s_hypothesis_%s.pdf' % (name,hypothesis)

    results = v.todict()
    save_results(results,name, hypothesis=hypothesis, followup=followup)



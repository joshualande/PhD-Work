import yaml
import numpy as np

# This import has to come first
from analyze_helper import save_results

from setup_pwn import setup_pwn,get_source
from argparse import ArgumentParser

from uw.pulsar.phase_range import PhaseRange

results=dict()

parser = ArgumentParser()
parser.add_argument("--pwndata", required=True)
parser.add_argument("-p", "--pwnphase", required=True)
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
parser.add_argument("--emin", default=1e2, type=float)
parser.add_argument("--emax", default=10**5.5, type=float)
args=parser.parse_args()

name=args.name
good_phase=PhaseRange(yaml.load(open(args.pwnphase))[name]['phase'])

phase_center = good_phase.phase_center
good_dphi = good_phase.phase_fraction

print 'good_phase = %s, %s +/- %s' % (good_phase, phase_center, good_dphi/2)

npts = 10
dphis = np.linspace(0,good_dphi+0.1, npts+1)[1:]

phases = [PhaseRange(phase_center-dphi/2, phase_center+dphi/2) for dphi in dphis]

results['dphis'] = dphis
results['phases'] = phases
results['TS'] = []

for phase,dphi in zip(phases,dphis):

    roi=setup_pwn(name,args.pwndata, phase=phase, 
                  free_radius=5, max_free=10, 
                  fit_emin=args.emin, fit_emax=args.emax)
    roi.modify(which=name, index=2, free=[True,False])

    roi.print_summary()
    roi.fit()
    roi.print_summary()

    ts = roi.TS(which=name,quick=False)

    results['TS'].append(ts)

    # here, make plot
    print 'phase=%s, dphi=%s, ts=%s' % (phase,dphi,ts)


save_results(results,name)

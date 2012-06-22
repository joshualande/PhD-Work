from argparse import ArgumentParser
from os.path import expandvars

import yaml
import numpy as np
import pylab as P

from skymaps import SkyDir

from uw.pulsar.phase_range import PhaseRange

from lande.utilities.tools import tolist

from lande.fermi.pulsar.data import get_phases
from lande.fermi.pulsar.plotting import plot_phaseogram
from lande.fermi.pulsar.optimize import OptimizePhases

#from lande.fermi.pulsar.offpeak import OffPeakBB, plot_phaseogram_blocks
from lande.fermi.pulsar.offpeak import OffPeakBB, plot_phaseogram_blocks


def find_offpeak(ft1,name,skydir, pwncat1phase, emax=100000):

    # First, find energy and radius that maximize H test.

    opt = OptimizePhases(ft1,skydir, emax=emax, verbose=True)

    print 'optimal energy=%s & radius=%s, h=%s' % (opt.optimal_emin,opt.optimal_radius,opt.optimal_h)

    # Get optimal phases
    phases = get_phases(ft1, skydir, opt.optimal_emin, emax, opt.optimal_radius)

    # compute bayesian blocks on the optimized list of phases
    off_peak_bb = OffPeakBB(phases)


    global results
    results=tolist(
        dict(
            name=name,
            pwncat1phase = pwncat1phase.tolist() if pwncat1phase is not None else None,
            off_peak_phase = off_peak_bb.off_peak.tolist(),
            blocks = off_peak_bb.blocks,
            optimal_emin = opt.optimal_emin,
            emax = emax,
            optimal_radius = opt.optimal_radius,
            ncpPrior=off_peak_bb.ncpPrior,
            actual_ncpPrior=off_peak_bb.actual_ncpPrior,
            )
        )

    yaml.dump(results,open('results_%s.yaml' % name,'w'))

    plot_phaseogram_blocks(ft1, 
         skydir = skydir, 
         emin = opt.optimal_emin, 
         emax = emax, 
         radius = opt.optimal_radius, 
         phase_range = off_peak_bb.off_peak,
         blocks_kwargs=dict(color='green'),
         phase_range_kwargs=dict(color='green', label='blocks'),
         data_kwargs=dict(color='red'),
         blocks = off_peak_bb.blocks)

    if pwncat1phase is not None:
        PhaseRange(pwncat1phase).axvspan(label='pwncat1', alpha=0.25, color='blue')

    P.legend()
    P.title(name)
    P.savefig('results_%s.pdf' % name)
    P.savefig('results_%s.png' % name)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--pwndata", required=True)
    parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
    parser.add_argument("--pwncat1phase", required=True)
    args=parser.parse_args()

    name=args.name
    pwndata=expandvars(args.pwndata)

    d=yaml.load(open(pwndata))[name]
    ft1=d['ft1']
    print ft1

    pwncat1 = yaml.load(open(expandvars(args.pwncat1phase)))
    if pwncat1.has_key(name):
        pwncat1phase=PhaseRange(*pwncat1[name]['phase'])
    else:
        pwncat1phase=None

    skydir = SkyDir(*d['cel'])
    find_offpeak(ft1,name,skydir,pwncat1phase=pwncat1phase)

from argparse import ArgumentParser
import copy
import numbers
import pickle
import yaml
import numpy as np
import pylab as P

from setup_pwn import setup_pwn

from uw.pulsar import lc_plotting_func
from uw.pulsar import lcprimitives as lp
from uw.pulsar.lcprimitives import * # for the eval
from uw.pulsar.lc_off_peak import OffPeak
from uw.pulsar.phase_range import PhaseRange
from uw.pulsar import lcfitters as lf
from uw.like.Models import ExpCutoff
from toolbag import tolist


def off_peak_bb(phases,ncpPrior=3):

    bb = BayesianBlocks.BayesianBlocks(phases)
    xx, yy = bb.lightCurve(ncpPrior)

    # min:
    



def find_offpeak(ft1,name,rad,peaks,pwncat1phase):
    
    plc = lc_plotting_func.PulsarLightCurve(ft1, 
                                           psrname=name, radius=rad,
                                           emin=50, emax=300000)
    plc.fill_phaseogram()

    phases = plc.get_phases()


    off_peak.axvspan(label='lande', alpha=0.25, color='green')
    pwncat1phase.axvspan(label='pwncat1', alpha=0.25, color='blue')

    P.legend()

    P.title(name)

    P.savefig('results_%s.pdf' % name)
    #P.savefig('phaseogram_%s.pdf' % name)

    global results
    results=tolist(
            dict(
                lande_phase = off_peak.tolist(),
                pwncat1phase = pwncat1phase.tolist(),
                )
            )

    yaml.dump(results,open('results_%s.yaml' % name,'w'))

    results['lcf'] = lcf
    results['init_template'] = init_template
    results['final_template'] = lct

    pickle.dump(results,open('results_%s.pickle' % name,'w'))


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--pwndata", required=True)
    parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
    parser.add_argument("--pwnphase", required=True)
    parser.add_argument("--pwnpeaks", required=True)
    parser.add_argument("--rad", default=1)
    args=parser.parse_args()

    name=args.name
    pwndata=args.pwndata

    ft1=yaml.load(open(pwndata))[name]['ft1']

    pwncat1phase=PhaseRange(*yaml.load(open(args.pwnphase))[name]['phase'])

    peaks=yaml.load(open(args.pwnpeaks))[name]['peaks']

    print peaks
    if peaks is None: parser.exit('no peaks')

    TSdc = find_TSdc(name,pwndata)

    peaks=yaml.load(open(args.pwnpeaks))[name]['peaks']

    find_offpeak(ft1,name,rad=args.rad,peaks=peaks,pwncat1phase=pwncat1phase, TSdc=TSdc)

from argparse import ArgumentParser
import copy
import numbers
import pickle
import yaml
import numpy as np
import pylab as P

import BayesianBlocks

from uw.pulsar import lc_plotting_func
from uw.pulsar.phase_range import PhaseRange
from lande_toolbag import tolist

class OffPeakBB(object):
    def __init__(self,phases,ncpPrior=9):

        bb = BayesianBlocks.BayesianBlocks(phases)
        xx, yy = bb.lightCurve(ncpPrior)

        self.xx = np.asarray(xx)
        self.yy = np.asarray(yy)


def find_offpeak(ft1,name,rad,pwncat1phase):
    
    plc = lc_plotting_func.PulsarLightCurve(ft1, 
                                           psrname=name, radius=rad,
                                           emin=50, emax=300000)
    plc.fill_phaseogram()

    phases = plc.get_phases()
    phases.sort()

    off_peak_bb = OffPeakBB(phases)

    nbins=100
    bins = np.linspace(0,1,100)

    fig = P.figure(None)
    axes = fig.add_subplot(111)

    axes.hist(phases,bins=bins,histtype='step',ec='red',lw=1)
    axes.set_ylabel('Normalized Profile')
    axes.set_xlabel('Phase')
    axes.grid(True)

    binsz = (bins[1]-bins[0])
    print phases
    print off_peak_bb.xx
    print off_peak_bb.yy*binsz

    P.plot(off_peak_bb.xx,off_peak_bb.yy*binsz)

    #off_peak.axvspan(label='bb', alpha=0.25, color='green')
    pwncat1phase.axvspan(label='pwncat1', alpha=0.25, color='blue')

    P.legend()

    P.title(name)

    P.savefig('results_%s.pdf' % name)
    #P.savefig('phaseogram_%s.pdf' % name)

    global results
    results=tolist(
            dict(
#                bb_phase = off_peak.tolist(),
                pwncat1phase = pwncat1phase.tolist(),
                )
            )

    yaml.dump(results,open('results_%s.yaml' % name,'w'))

    pickle.dump(results,open('results_%s.pickle' % name,'w'))


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--pwndata", required=True)
    parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
    parser.add_argument("--pwnphase", required=True)
    parser.add_argument("--rad", default=1)
    args=parser.parse_args()

    name=args.name
    pwndata=args.pwndata

    ft1=yaml.load(open(pwndata))[name]['ft1']

    pwncat1phase=PhaseRange(*yaml.load(open(args.pwnphase))[name]['phase'])

    find_offpeak(ft1,name,rad=args.rad,pwncat1phase=pwncat1phase)

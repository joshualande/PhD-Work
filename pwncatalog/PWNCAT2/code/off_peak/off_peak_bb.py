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
    """ Algorithm to compute the off peak window
        of a pulsar using a Bayesian block analysis. 
        
        N.B. I ran into some preliminary problems using
        this algorithm running Bayesian blocks in
        unbinned mode becasue it would try to find
        very small structure in the light curves
        which I knew to be unphysical.
        The reasonable solution I decided upon was
        to run Bayesian Blocks in binned mode
        with a binsize of 1/100 in pulsar phase.
        This washes out any structure on smaller
        scales and appaers to help
        the method only find physically large enough
        structure in the pulsar light curve. """
       
    @staticmethod
    def _max_phase(phases, ncpPrior):
        """ find the (approximate) maximum in the pulsar light curve 
        
            This is conveniently determined by using
            bayesian blocks upon the un-rotated light curve. """
            
        tstart=0
        bins = np.linspace(0,1,21)
        bin_content = np.histogram(phases, bins=bins)[0]
        bin_sizes = np.ones_like(phases)*(bins[1]-bins[0])
        bb = BayesianBlocks.BayesianBlocks(tstart,bin_content.tolist(),bin_sizes.tolist())
        xx, yy = bb.lightCurve(ncpPrior)
        return xx[np.argmax(yy)]

    def __init__(self,phases,ncpPrior=3):
        """ phases is the numpy array of pulsar phases. """

        self.phases = phases
        self.ncpPrior = ncpPrior

        self.max_phase = max_phase = self._max_phase(phases, ncpPrior)
        print 'max phase',max_phase

        self.offset_phases = (phases - max_phase) % 1
        #self.offset_phases.sort()
        #print 'offset_phases = ',self.offset_phases

        #self.bb = BayesianBlocks.BayesianBlocks(self.offset_phases)
        #offset_xx, yy = self.bb.lightCurve(ncpPrior)

        tstart=0
        bins = np.linspace(0,1,21)
        bin_content = np.histogram(self.offset_phases, bins=bins)[0]
        bin_sizes = np.ones_like(self.offset_phases)*(bins[1]-bins[0])
        bb = BayesianBlocks.BayesianBlocks(tstart,bin_content.tolist(),bin_sizes.tolist())
        offset_xx, yy = bb.lightCurve(ncpPrior)


        print offset_xx, yy 
        offset_xx = np.asarray(offset_xx)
        yy = np.asarray(yy)

        # first, get phase range by finding the lowest valey
        min_bin = np.argmin(yy)
        phase_min = max_phase + offset_xx[min_bin]
        phase_max = max_phase + offset_xx[min_bin+1]
        phase_range = phase_max - phase_min
        phase_min, phase_max = phase_min + 0.1*phase_range, phase_max - 0.1*phase_range
        self.phase_range = PhaseRange(phase_min, phase_max)

        # next, construct un-offset bayesian blocks

        # bayesian blocks dont always go exactly to the phase edges
        offset_xx[0] = 0
        offset_xx[-1] = 1

        xx = (max_phase + offset_xx)
        divide = np.where( xx > 1)[0]

        if len(divide)>0:
            # rotate blocks to correct phase
            first_overflow = divide[0]
            xx = np.append(xx[first_overflow:] % 1,xx[:first_overflow])
            yy = np.append(yy[first_overflow:],yy[:first_overflow])

        # connect the (now disconnected) edges to 0 and 1
        if xx[0] != 0:
            xx = np.append(0, xx)
            yy = np.append(yy[0], yy)
        if xx[-1] != 1:
            xx = np.append(xx, 1)
            yy = np.append(yy, yy[-1])

        self.xx, self.yy = xx, yy



def find_offpeak(ft1,name,rad,pwncat1phase):
    
    plc = lc_plotting_func.PulsarLightCurve(ft1, 
                                           psrname=name, radius=rad,
                                           emin=1000, emax=300000)
    plc.fill_phaseogram()

    phases = plc.get_phases()

    global off_peak_bb
    off_peak_bb = OffPeakBB(phases)

    nbins=100
    bins = np.linspace(0,1,100)

    fig = P.figure(None)
    axes = fig.add_subplot(111)

    axes.hist(phases,bins=bins,histtype='step',ec='red',lw=1)
    axes.set_ylabel('Counts')
    axes.set_xlabel('Phase')
    axes.set_xlim(0,1)
    axes.grid(True)

    binsz = bins[1]-bins[0]
    P.plot(off_peak_bb.xx,off_peak_bb.yy*binsz)

    off_peak_bb.phase_range.axvspan(label='bb', alpha=0.25, color='green')
    if pwncat1phase is not None:
        pwncat1phase.axvspan(label='pwncat1', alpha=0.25, color='blue')

    P.legend()

    P.title(name)

    P.savefig('results_%s.pdf' % name)

    global results
    results=tolist(
        dict(
            pwncat1phase = pwncat1phase.tolist() if pwncat1phase is not None else None,
            bayesian_blocks = dict(
                off_peak = off_peak_bb.phase_range.tolist(),
                xx = off_peak_bb.xx,
                yy = off_peak_bb.yy,
                ) 
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

    pwncat1 = yaml.load(open(args.pwnphase))
    if pwncat1.has_key(name):
        pwncat1phase=PhaseRange(*pwncat1[name]['phase'])
    else:
        pwncat1phase=None

    find_offpeak(ft1,name,rad=args.rad,pwncat1phase=pwncat1phase)

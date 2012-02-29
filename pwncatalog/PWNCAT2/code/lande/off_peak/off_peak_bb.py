from argparse import ArgumentParser
from os.path import expandvars

import yaml
import numpy as np
import pylab as P

import BayesianBlocks

from skymaps import SkyDir

from uw.utilities.fitstools import rad_extract

from uw.pulsar import lc_plotting_func
from uw.pulsar.phase_range import PhaseRange
from uw.pulsar.stats import hm
from uw.like.roi_image import memoize

from lande.utilities.toolbag import tolist

from lande.fermi.pulsar.data import get_phases
from lande.fermi.pulsar.plotting import plot_phaseogram

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
        bins = np.linspace(0,1,51)
        bin_content = np.histogram(phases, bins=bins)[0]
        bin_sizes = np.ones_like(phases)*(bins[1]-bins[0])
        bb = BayesianBlocks.BayesianBlocks(tstart,bin_content.tolist(),bin_sizes.tolist())
        xx, yy = bb.lightCurve(ncpPrior)
        return xx[np.argmax(yy)]

    def __init__(self,phases,ncpPrior=5):
        """ phases is the numpy array of pulsar phases. """

        self.phases = phases
        self.ncpPrior = ncpPrior

        self.max_phase = max_phase = self._max_phase(phases, ncpPrior)
        print 'max phase',max_phase

        self.offset_phases = (phases - max_phase) % 1

        tstart=0
        bins = np.linspace(0,1,51)
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
        self.off_peak = PhaseRange(phase_min, phase_max)

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

        self.blocks = dict(xx = xx, yy = yy)


class OptimizePhases(object):
    """ very simple object to load in an ft1 file and
        optimize the radius & energy to find the
        best pulsations. """

    def __init__(self, ft1, skydir, emax,
                 ens=np.linspace(100,1000,21),
                 rads=np.linspace(0.1,2,20),
                 verbose=False 
                ):

        self.ft1 = ft1
        self.skydir = skydir
        self.emax = emax

        stats = np.empty([len(ens),len(rads)])

        for iemin,emin in enumerate(ens):
            for irad,radius in enumerate(rads):
                phases = get_phases(ft1, skydir, emin, emax, radius)
                stat = hm(phases) if len(phases) > 0 else 0
                if verbose: print 'emin=%s, radius=%s, stat=%s, len=%s, n0=%s' % (emin,radius,stat,len(phases),np.sum(phases==0))
                stats[iemin,irad] = stat

        a = np.argmax(stats)
        coord_e, coord_r = np.unravel_index(a, stats.shape)

        self.optimal_emin = ens[coord_e]
        self.optimal_radius = rads[coord_r]
        self.optimal_h = np.max(stats)


def plot(ft1, off_peak_phase, blocks, pwncat1phase=None, **kwargs):

    # plot bins
    axes, bins = plot_phaseogram(ft1, **kwargs)

    # plot blocks
    binsz = bins[1]-bins[0]
    axes.plot(np.asarray(blocks['xx']),np.asarray(blocks['yy'])*binsz)

    # plot phase ranges
    PhaseRange(off_peak_phase).axvspan(label='bb', alpha=0.25, color='green')
    if pwncat1phase is not None:
        PhaseRange(pwncat1phase).axvspan(label='pwncat1', alpha=0.25, color='blue')


def find_offpeak(ft1,name,skydir,pwncat1phase, emax=100000):

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
            pwncat1phase = pwncat1phase.tolist() if pwncat1phase is not None else None,
            off_peak_phase = off_peak_bb.off_peak.tolist(),
            blocks = off_peak_bb.blocks,
            optimal_emin = opt.optimal_emin,
            emax = emax,
            optimal_radius = opt.optimal_radius,
            )
        )

    yaml.dump(results,open('results_%s.yaml' % name,'w'))

    plot(ft1, 
         skydir = skydir, 
         emin = opt.optimal_emin, 
         emax = emax, 
         radius = opt.optimal_radius, 
         off_peak_phase = off_peak_bb.off_peak,
         blocks = off_peak_bb.blocks, 
         pwncat1phase = pwncat1phase)
    P.legend()
    P.title(name)
    P.savefig('results_%s.pdf' % name)


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

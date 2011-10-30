import pylab as P
import numpy as np

from uw.pulsar.lc_plotting_func import PulsarLightCurve
from uw.pulsar.phase_range import PhaseRange
def _get_pulsar_data(ft1, phase, radius=1, emin=100, emax=300000):

    plc = PulsarLightCurve(ft1, emin=emin, emax=emax, radius=radius)
    plc.fill_phaseogram()
    phases = plc.get_phases()
    times = plc.get_times()
    return phases, times

def plot_phaseogram(name, ft1, phase, filename):
    """ Simple code to plot a phaseogram. """
    phases, times = _get_pulsar_data(ft1, phase)

    nbins=50
    fig = P.figure(None, figsize=(5,5))
    axes = fig.add_subplot(111)
    axes.hist(phases,bins=np.linspace(0,1,nbins+1),histtype='step',ec='red',normed=True,lw=1)
    axes.set_xlim(0,1)
    axes.set_title(name)
    axes.set_xlabel('phase')

    PhaseRange(phase).axvspan(axes=axes, label='pwncat1', alpha=0.25, color='green')
    P.savefig(filename)

def plot_phase_vs_time(name, ft1, phase, filename):
    """ Simple code to plot phase vs time. """
    phases, times = _get_pulsar_data(ft1, phase)

    # here, put a 2d histogram
    fig = P.figure(None, figsize=(5,5))
    fig.subplots_adjust(left=0.2)
    axes = fig.add_subplot(111)
    d, xedges, yedges = np.histogram2d(times, phases, bins=(50,50), range=[[min(times), max(times)], [0,1]])

    extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
    axes.imshow(d, extent=extent, interpolation='nearest', aspect='auto')
    axes.set_xlabel('phase')
    axes.set_ylabel('MJD')
    axes.set_title(name)

    P.savefig(filename)

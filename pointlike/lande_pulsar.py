import pylab as P
import numpy as np

from uw.utilities.fitstools import rad_extract

from uw.pulsar.lc_plotting_func import PulsarLightCurve
from uw.pulsar.phase_range import PhaseRange
def _get_pulsar_data(ft1, radius=1, emin=100, emax=300000):

    plc = PulsarLightCurve(ft1, emin=emin, emax=emax, radius=radius)
    plc.fill_phaseogram()
    phases = plc.get_phases()
    times = plc.get_times()
    return phases, times

def plot_phaseogram(name, ft1, filename, title=None, off_pulse=None):
    """ Simple code to plot a phaseogram. """
    phases, times = _get_pulsar_data(ft1)

    nbins=50
    fig = P.figure(None, figsize=(5,5))
    axes = fig.add_subplot(111)
    axes.hist(phases,bins=np.linspace(0,1,nbins+1),histtype='step',ec='red',normed=True,lw=1)
    axes.set_xlim(0,1)

    if title is None: title = 'Phaseogram for %s' % name
    axes.set_title(title)

    axes.set_xlabel('phase')

    if off_pulse is not None:
        PhaseRange(off_pulse).axvspan(axes=axes, alpha=0.5, color='blue')
    P.savefig(filename)
    return axes

def plot_phase_vs_time(name, ft1, filename, title=None, off_pulse=None):
    """ Simple code to plot phase vs time. """
    phases, times = _get_pulsar_data(ft1)

    # here, put a 2d histogram
    fig = P.figure(None, figsize=(5,5))
    fig.subplots_adjust(left=0.2)
    axes = fig.add_subplot(111)

    # Note about 2D histograms: 
    #  http://www.physics.ucdavis.edu/~dwittman/Matplotlib-examples/
    hist, xedges, yedges = np.histogram2d(phases, times, bins=(50,50), range=[[0,1], [min(times), max(times)]])
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1] ]
    axes.imshow(hist.T,extent=extent,interpolation='nearest',origin='lower', aspect='auto')

    if off_pulse is not None:
        PhaseRange(off_pulse).axvspan(axes=axes, alpha=0.5, color='white')

    axes.set_xlabel('phase')
    axes.set_ylabel('MJD')

    if title is None: title = 'Phase vs Time for %s' % name
    axes.set_title(title)

    P.savefig(filename)
    return axes

def get_phases(ft1, skydir, emin, emax, radius):
    ed = rad_extract(ft1,skydir,radius,return_cols=['PULSE_PHASE'])
    all_phases = ed['PULSE_PHASE']

    cut = (ed['ENERGY'] < emax) & (ed['DIFFERENCES'] < np.radians(radius))
    return all_phases[cut]




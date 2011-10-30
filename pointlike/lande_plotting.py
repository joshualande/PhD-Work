import os

import pylab as P
import numpy as np

from uw.like.roi_extended import BandFitExtended
from uw.utilities import keyword_options



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

 
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from uw.like.roi_plotting import ROITSMapPlotter
from uw.like.roi_state import PointlikeState
import pywcsgrid2
class ROITSMapBandPlotter(object):

    defaults = ROITSMapPlotter.defaults 
    defaults=keyword_options.change_defaults(defaults,'figsize',(9,4))

    @keyword_options.decorate(defaults)
    def __init__(self,roi,bin_edges,**kwargs):

        self.roi = roi
        keyword_options.process(self, kwargs)

        self.bin_edges = bin_edges
        self.nplots = len(bin_edges) - 1

        for e in bin_edges:
            if not np.any(np.abs(e-roi.bin_edges) < 0.5):
                raise Exception("Energy %.1f inconsistent with ROI energy binning." % e)

        self.lower_energies = bin_edges[:-1]
        self.upper_energies = bin_edges[1:]

        state = PointlikeState(roi)
 
        # step 1, test consistentcy of each energy with binning in pointlike

        self.tsmaps = []
        for i,(lower,upper) in enumerate(zip(self.lower_energies, self.upper_energies)):
            roi.change_binning(fit_emin=lower,fit_emax=upper)
            self.tsmaps.append(ROITSMapPlotter(roi,title='',show_colorbar=(i==0),**kwargs))

        state.restore()

    def show(self,filename=None):
        print 'figsize = ',self.figsize

        self.fig = fig = P.figure(self.fignum,self.figsize)
        P.clf()

        header = self.tsmaps[0].pf[0].header

        self.grid = grid = ImageGrid(fig, (1, 1, 1), 
                                     nrows_ncols = (1, self.nplots),
                                     axes_pad=0.1, share_all=True,
                                     cbar_mode="single", cbar_pad="2%",
                                     cbar_location="right",
                                     axes_class=(pywcsgrid2.Axes,
                                                 dict(header=header)))

        for i,(tsmap,lower,upper) in enumerate(zip(self.tsmaps,self.lower_energies,self.upper_energies)):
            tsmap.show(axes=grid[i], cax=grid.cbar_axes[0] if i==0 else None)
            format_energy=lambda x: '%.1f' % (x/1000.) if x < 1000 else '%.0f' % (x/1000.)
            lower_string=format_energy(lower)
            upper_string=format_energy(upper)
            grid[i].add_inner_title("%s-%s GeV" % (lower_string,upper_string), loc=2)

        if filename is not None: P.savefig(filename)



def plot_ds9_contour(ax,contour,**kwargs):
    """ Parse a ds9 format contour file. Kwargs goes into the plot function. """
    lines=open(os.path.expandvars(contour)).readlines()
    ras,decs=[],[]
    for line in lines:
        if line.strip() is '':
            ax['fk5'].plot(ras,decs,'-',**kwargs)
            ras,decs=[],[]
        else:
            ra,dec=line.split()
            ras.append(float(ra)); decs.append(float(dec))

def plot_lat(file,ax,
             plot_kwargs = dict(color='black', marker='o', 
                                linestyle='none', capsize=0, markersize=4, 
                                label='LAT'),
             ul_kwargs = dict(color='black', marker='o', 
                              linestyle='none', capsize=0, markersize=0),
             xlabel='Energy (MeV)',
             ylabel=r'$\mathrm{E}^2$ dN/dE $(\mathrm{MeV}\ \mathrm{cm}^{-2}\ \mathrm{s}^{-1})$'
            ):
    """ Plot onto a matplotlib axes ax a file created by the SED object. 
        fmt = format of points

        X axes is assumed to be 
    """
    lat_lines=open(file).readlines()

    lat_lines=[line.strip() for line in lat_lines]
    lat_lines=[line for line in lat_lines if line != '']

    # First, make sure header is good
    if lat_lines[0].split() != ['Energy','Flux','Flux_Err']:
        raise Exception("Unable to parse LAT header")
    if lat_lines[1].split() != ['[MeV]','[ph/cm^2/s/MeV]']:
        raise Exception("Unable to parse LAAT header")
    
    # load in data
    lat_lines = lat_lines[2:]
    energy, flux, flux_err = zip(*[line.split() if len(line.split())==3 else line.split()+[''] for line in lat_lines])
    energy = np.asarray(map(float,energy))

    ul = np.asarray([True if '<' in i else False for i in flux])
    flux = np.asarray([float(i.replace('<','')) for i in flux])

    flux_err = np.asarray([float(i) if i is not '' else 0 for i in flux_err])

    # plot data ponits which are not upper limits
    ax.errorbar(energy[~ul],(energy**2*flux)[~ul],
                yerr=(energy**2*flux_err)[~ul],
                **plot_kwargs
                )

    if sum(ul)>0:
        # Plot upper limits
        ax.errorbar(energy[ul],(energy**2*flux)[ul],
                    yerr=[ (0.4*energy**2*flux)[ul], np.zeros_like(energy[ul]) ],
                    lolims=True,
                    **ul_kwargs
                   )

    if xlabel is not None: ax.set_xlabel(xlabel)
    if ylabel is not None: ax.set_ylabel(ylabel)

    ax.set_xscale('log')
    ax.set_yscale('log')

def plot_hess(file,ax, 
              xlabel='Energy (MeV)',
              ylabel=r'$\mathrm{E}^2$ dN/dE $(\mathrm{MeV}\ \mathrm{cm}^{-2}\ \mathrm{s}^{-1})$',
              **kwargs
             ):
    """ Plot HESS data points taken
        from HESS Auxilary website pages. 
    """

    plot_kwargs=dict(capsize=0, marker='+', color='black', markersize=4, linestyle='none', label='H.E.S.S')
    plot_kwargs.update(kwargs)


    hess_lines=open(file).readlines()

    hess_lines=[line.strip() for line in hess_lines]
    hess_lines=[line for line in hess_lines if line != '']

    if hess_lines[0].split() != ['Energy','Flux','Flux','Error_low','Flux','Error_high']:
        raise Exception("Unable to parse hess header")
    if hess_lines[1].split() != ['[TeV]','[/TeV','cm^2','s]']:
        raise Exception("Unable to parse hess header")

    hess_lines = hess_lines[2:]
    energy, flux, flux_low, flux_high = map(np.asarray,zip(*[map(float,line.split()) for line in hess_lines]))

    # convert energy to MeV
    energy *= 1e6
    # convert TeV poitns to MeV cm^-2 s^-1
    # TeV^-1 cm^-2 s^-1 * (1TeV/1e6 MeV) * MeV**2 = MeV cm^-1 s^-1
    flux *= 1e-6
    flux_low *= 1e-6
    flux_high *= 1e-6

    # not sure if there are

    ax.errorbar(energy,energy**2*flux,
                yerr=[energy**2*flux_low,energy**2*flux_high],
                **plot_kwargs)

    if xlabel is not None: ax.set_xlabel(xlabel)
    if ylabel is not None: ax.set_ylabel(ylabel)

    ax.set_xscale('log')
    ax.set_yscale('log')

def fix_axesgrid(grid):
    """ Remove the ticks which overlap with nearby axes. """
    if grid._direction != 'row': 
        raise Exception("Not implemented")

    nrows,ncols=grid._nrows,grid._ncols

    for row in range(nrows):
        for col in range(ncols):
            ax = grid[row*ncols + col]
            print row,col,ax.get_xticks(),ax.get_yticks()
            if row != 0 and col==0:
                ax.set_yticks(ax.get_yticks()[0:-1])
            if col != ncols-1 and row==nrows-1:
                ax.set_xticks(ax.get_xticks()[0:-1])


import os

import pylab as P
import numpy as np
import pywcsgrid2

from uw.utilities import keyword_options
 
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from uw.like.roi_plotting import ROITSMapPlotter, ROISmoothedSources, ROISmoothedSource
from uw.like.roi_state import PointlikeState
from lande_sed import LandeSED

def plot_gtlike_cutoff_test(cutoff_results, sed_results, filename=None, title=None, 
                            model_0_kwargs=dict(color='red', zorder=0),
                            model_1_kwargs=dict(color='blue', zorder=0),
                            sed_kwargs=dict(),
                            plot_kwargs=dict(),
                           ):
    """ Plots the cutoff test performed of a spectrum using the function
        likelihood_tools.gtlike_test_cutoff.

        Input:
            cutoff_dict: created by likelihood_tools.gtlike_test_cutoff
            sed_dict: created by LandeSED.todict(). Can also be a yaml
              file created by LandeSED.save().

            model_0_kwargs: kwargs for model_0's plot 
            model_1_kwargs: kwargs for model_0's plot 
            sed_kwargs: kwargs to pass into LandeSED
              E.G. flux_units, flux_units, figsize, ...
    """
    sed=LandeSED(sed_results,**sed_kwargs)

    axes=sed.plot(plot_spectral_fit=False, **plot_kwargs)
    axes.autoscale(enable=False)

    model_0 = LandeSED.dict_to_spectrum(cutoff_results['model_0'])
    model_1 = LandeSED.dict_to_spectrum(cutoff_results['model_1'])
    sed.plot_spectrum(model_0, **model_0_kwargs)
    sed.plot_spectrum(model_1, **model_1_kwargs)

    if title is None:
        axes.set_title('Gtlike Cutoff test for %s' % sed.name)
    else:
        axes.set_title(title)


    if filename is not None: P.savefig(filename)
    return axes
        

class ROIBandPlotter(object):

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

        self.maps = []
        for i,(lower,upper) in enumerate(zip(self.lower_energies, self.upper_energies)):
            roi.change_binning(fit_emin=lower,fit_emax=upper)
            self.maps.append(self.object(roi,title='',**kwargs))

        state.restore()

    def show(self,filename=None):
        print 'figsize = ',self.figsize

        self.fig = fig = P.figure(self.fignum,self.figsize)
        P.clf()

        header = self.maps[0].header

        self.grid = grid = ImageGrid(fig, (1, 1, 1), 
                                     nrows_ncols = (1, self.nplots),
                                     axes_pad=0.1, share_all=True,
                                     cbar_location="top",
                                     cbar_mode="each",
                                     cbar_size="7%",
                                     cbar_pad="2%",
                                     axes_class=(pywcsgrid2.Axes,
                                                 dict(header=header)))

        for i,(map,lower,upper) in enumerate(zip(self.maps,self.lower_energies,self.upper_energies)):
            map.show(axes=grid[i], cax=grid[i].cax)
            format_energy=lambda x: '%.1f' % (x/1000.) if x < 1000 else '%.0f' % (x/1000.)
            lower_string=format_energy(lower)
            upper_string=format_energy(upper)
            grid[i].add_inner_title("%s-%s GeV" % (lower_string,upper_string), loc=2)

        if filename is not None: P.savefig(filename)

class ROITSMapBandPlotter(ROIBandPlotter):
    object = ROITSMapPlotter
    defaults = object.defaults 
    defaults=keyword_options.change_defaults(defaults,'figsize',(9,4))

class ROISourcesBandPlotter(ROIBandPlotter):
    object = ROISmoothedSources
    defaults = object.defaults 
    defaults=keyword_options.change_defaults(defaults,'figsize',(9,4))

class ROISourceBandPlotter(ROIBandPlotter):
    object = ROISmoothedSource
    defaults = object.defaults 
    defaults=keyword_options.change_defaults(defaults,'figsize',(9,4))



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
                              linestyle='none', markersize=0),
             xlabel='Energy (MeV)',
             ylabel=r'$\mathrm{E}^2$ dN/dE $(\mathrm{MeV}\ \mathrm{cm}^{-2}\ \mathrm{s}^{-1})$'
            ):
    """ Plot onto a matplotlib axes ax a file created by the SED object. 
        fmt = format of points

        X axes is assumed to be 
    """
    lat_lines=open(file).readlines()

    lat_lines=[line.strip() for line in lat_lines]
    lat_lines=[line for line in lat_lines if line != '' and line[0] != '#' ]

    # First, make sure header is good
    if lat_lines[0].split() != ['Lower_Energy', 'Upper_Energy', 'Energy','dN/dE','dN/dE_Err']:
        raise Exception("Unable to parse LAT header. Bad names: %s" % lat_lines[0])
    if lat_lines[1].split() != ['[MeV]', '[MeV]', '[MeV]','[ph/cm^2/s/MeV]', '[ph/cm^2/s/MeV]']:
        raise Exception("Unable to parse LAT header. Bad units: %s" % lat_lines[1])
    
    # load in data
    lat_lines = lat_lines[2:]
    lower_energy, upper_energy, energy, flux, flux_err = zip(*[line.split() if len(line.split())==5 else line.split()+[''] for line in lat_lines])
    energy = np.asarray(map(float,energy))

    ul = np.asarray([True if '<' in i else False for i in flux])
    flux = np.asarray([float(i.replace('<','')) for i in flux])

    flux_err = np.asarray([float(i) if i is not '' else 0 for i in flux_err])

    # plot data points which are not upper limits
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
            if row != 0 and col==0:
                ax.set_yticks(ax.get_yticks()[0:-1])
            if col != ncols-1 and row==nrows-1:
                ax.set_xticks(ax.get_xticks()[0:-1])


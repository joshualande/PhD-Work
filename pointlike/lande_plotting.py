import os

import pylab as P
import numpy as np
import pywcsgrid2

from uw.utilities import keyword_options
 
from mpl_toolkits.axes_grid1.axes_grid import ImageGrid
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
from matplotlib.patheffects import withStroke

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


def label_axesgrid(grid, stroke=True, **kwargs):
    """ Add "(a)" to first plot, "(b)" to second, ... """

    text_kwargs=dict(frameon=False, loc=2, prop=dict(size=14))
    text_kwargs.update(kwargs)

    for i,g in enumerate(grid):
        _at = AnchoredText('(%s)' % chr(i+97), **text_kwargs)

        if stroke:
            _at.txt._text.set_path_effects([withStroke(foreground="w", linewidth=3)])

        g.add_artist(_at)


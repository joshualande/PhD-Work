import pylab as P

import numpy as np

from uw.like.roi_extended import BandFitExtended
from uw.utilities import keyword_options

import os

class TSExtVsEnergy(object):

    """ Object to make a plot of TSext vs energy. """


    defaults = (
            ('which',           None,  'Source to analyze'),
            ('title',           None, 'Title for the plot'),
            ('fignum',             1,                   ''),
            ('figsize',        (6,4),                   ''),
    )

    @keyword_options.decorate(defaults)
    def __init__(self, roi, **kwargs):
        keyword_options.process(self, kwargs)

        roi.setup_energy_bands()
        self.emin = np.asarray([eb.emin for eb in roi.energy_bands])
        self.emax = np.asarray([eb.emax for eb in roi.energy_bands])

        which = self.which
        old_roi_p   = roi.get_parameters().copy()

        # extended hypothesis

        source=roi.get_source(which='IC443')
        sm = source.spatial_model
        manager,index=roi.mapper(which)
        roi.fit(use_gradient=True)

        self.ll_ext,self.ll_pt = [],[]


        for eb in roi.energy_bands:
            self.ll_ext.append(
                -sum(band.logLikelihood() for band in eb.bands)
                )


        sm.shrink()
        manager.bgmodels[index].initialize_counts(roi.bands)
        roi.__update_state__()

        roi.fit(use_gradient=True, estimate_errors=False)

        # point hypothesis

        manager,index=roi.mapper('IC443')
        for eb in roi.energy_bands:
            self.ll_pt.append(
                -sum(band.logLikelihood() for band in eb.bands)
                )

        sm.unshrink()
        manager.bgmodels[index].initialize_counts(roi.bands)

        roi.set_parameters(old_roi_p)
        roi.__update_state__()

        self.ll_ext = np.asarray(self.ll_ext)
        self.ll_pt = np.asarray(self.ll_pt)

        self.ts_ext=2*(self.ll_ext-self.ll_pt)
        self.ts_ext[self.ts_ext<0]=0

    def show(self,filename=None,axes=None):

        if axes is None:
            fig = P.figure(self.fignum,self.figsize)
            axes = fig.get_axes([0.15,0.15,0.7,0.7])
            P.clf()

        ax = self.axes = axes

        ax.set_xlabel(r'Energy (MeV)')
        ax.set_ylabel(r'$\mathrm{TS}_\mathrm{ext}$')
        ax.semilogx(self.emin,self.ts_ext,'k',drawstyle='steps-post')

        if self.title is None: 
            self.title = '$\mathrm{TS}_\mathrm{ext}$ vs Energy'
            self.title += ' for %s' % self.source.name

        ax.set_title(self.title)

        if filename is not None:
            P.savefig(filename)


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

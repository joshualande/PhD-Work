import pylab as P
import numpy as np

from uw.like.roi_extended import BandFitExtended
from uw.utilities import keyword_options

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

        which = self.which
        old_roi_p   = roi.get_parameters().copy()

        # extended hypothesis

        source=roi.get_source(which='IC443')
        sm = source.spatial_model
        manager,index=roi.mapper(which)
        roi.setup_energy_bands()
        roi.fit(use_gradient=True)

        self.emin = np.asarray([eb.emin for eb in roi.energy_bands])
        self.emax = np.asarray([eb.emax for eb in roi.energy_bands])
        self.ll_ext,self.ll_pt = [],[]


        for eb in roi.energy_bands:
            bfe=BandFitExtended(index,eb,roi)
            bfe.fit(saveto='bandfits')

            ll = -sum(bfe.bandLikelihoodExtended([band.bandfits if band.bandfits > 0 else 0],
                                                 band, myband) \
                                    for band,myband in zip(bfe.bands,bfe.mybands))
            self.ll_ext.append(ll)


        sm.shrink()
        manager.bgmodels[index].initialize_counts(roi.bands)
        roi.__update_state__()

        roi.fit(use_gradient=True, estimate_errors=False)

        # point hypothesis

        manager,index=roi.mapper('IC443')
        roi.setup_energy_bands()
        for eb in roi.energy_bands:
            eb.bandFit(which=index,saveto='bandfits')

            ll = -sum(band.bandLikelihood([band.bandfits if
                                           band.bandfits > 0 else 0],index) \
                              for band in eb.bands)

            self.ll_pt.append(ll)

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


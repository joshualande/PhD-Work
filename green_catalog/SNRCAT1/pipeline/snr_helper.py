# Not entirely sure why, but pyLikelihood
# will get a swig::stop_iteraiton error
# unless it is imported first.
from roi_gtlike import Gtlike


from lande_localize import GridLocalize
from snr_setup import get_snr
from uw.like.roi_plotting import ROISmoothedSource
from uw.like.roi_extended import ExtendedSource

from likelihood_tools import sourcedict,powerlaw_upper_limit

import pylab as P
import pyfits

import yaml
import os


def overlay_on_plot(name, axes, header, roi, deleted_sources):
    """ Overlay:
        * Deleted 2FGL sources
        * the SNR + best fit extension. 
        * Any avaliable SNR contours
    """
    for source in deleted_sources:
        axes['gal'].plot([source.skydir.l()],[source.skydir.b()], marker='*', color='green', 
                         markeredgecolor='white', markersize=12)

    source = roi.get_source(name)

    # plot the best fit SNR position/center in blue
    ROISmoothedSource.overlay_source(source, axes, color='blue', zorder=10)

    if isinstance(source,ExtendedSource):
        # overlay the best fit SNR size in blue
        ROISmoothedSource.overlay_extension(source, axes, header, extension_color='blue',
                                            extension_zorder=10)


def plots(roi, name, hypothesis, snrsize, deleted_sources):
    """ make a smoothed counts map + tsmap. 

        here, plot again the region before + after background subtraction

        Here, plot 'radio' size + extended source best fit spatial model
    """
    
    plot_size = max(snrsize*4, 3)
    
    for kernel_rad in [0.1,0.25]:
        for function,title_base,filename_base in [[roi.plot_sources,'Diffuse Subtracted','sources'],[roi.plot_source,'BG Source Subtracted','source']]:
            smooth=function(which = name,
                            size = plot_size, 
                            kernel_rad=kernel_rad, 
                            colorbar_radius = max(snrsize, 1),
                            title=r'%s %s ($\sigma_\mathrm{smooth}=%g^\circ$)' % (title_base,name,kernel_rad))
            overlay_on_plot(name, smooth.axes, smooth.header, roi, deleted_sources)
            P.savefig('%s_%s_kernel_%g_%s.png' % (filename_base,hypothesis,kernel_rad,name))


    # Residual TS Map
    tsmap=roi.plot_tsmap(size = plot_size, pixelsize = 1./8, title='Residual TS Map %s' % name)
    overlay_on_plot(name, tsmap.axes, tsmap.header, roi, deleted_sources)
    P.savefig('tsmap_residual_%s_%s.png' % (hypothesis,name))

    # Source TS Map
    roi.zero_source(name)
    tsmap=roi.plot_tsmap(size = plot_size, pixelsize = 1./8, title='Source TS Map %s' % name)
    overlay_on_plot(name, tsmap.axes, tsmap.header, roi, deleted_sources)
    roi.unzero_source(name)
    P.savefig('tsmap_source_%s_%s.png' % (hypothesis,name))


def gtlike_analysis(roi, name, emin, emax, hypothesis, snrsize, upper_limit=False):
    """ perform spectral fit with gtlike to crosscheck the point-like anlaysis. """

    print '\n\nPerforming Gtlike analysis\n\n'

    gtlike=Gtlike(roi,binsz=1./8)
    like=gtlike.like

    like.fit(covar=True)

    results = sourcedict(like,name,emin=emin,emax=emax)
    if upper_limit:
        # *) Perform upper limits assuming spectral index 2

        # N.B., for the E>10GeV analysis we are very much in the Poisson instead
        # of Gaussian regime. The likelihood function will be VERY linear. As a result,
        # delta_log_like_limits = 50 should be much more reasonable (not quite sure
        # how to quantify this right now...)
        results['upper_limit'] = powerlaw_upper_limit(like,name, delta_log_like_limits=50, verbosity=2)

    return results

def pointlike_analysis(roi, name, emin, emax, hypothesis, snrsize, 
                       localize=False, fit_extension=False, upper_limit=False):

    print '\n\nPerforming Pointlike analysis for %s hypothesis\n\n' % hypothesis

    def fit():
        """ Convenience function incase fit fails. """
        try:
            roi.fit()
        except Exception, ex:
            print 'ERROR spectral fitting: ', ex

    print 'Initial Spectral Model for %s hypothesis:' % hypothesis
    roi.print_summary(galactic=True)


    if localize:
        # Note, no preliminary spectral fit of point-like
        # source before localization since the fit could
        # likely fail to converge.
        try:
            print 'First, localize with GridLocalize (helps with convergence)'
            size=max(snrsize,0.5)
            grid=GridLocalize(roi,which=name,size=size,pixelsize=size/10)
            skydir = grid.best_position()
            print 'Using Grid Localize, best position is (l,b)=(%.3f,%.3f)' % (skydir.l(),skydir.b())

            roi.modify(which=name, skydir=skydir)

            roi.localize(which=name, update=True)
        except Exception, ex:
            print 'ERROR localizing: ',ex

    if fit_extension:
        fit()

        roi.fit_extension(which=name)
        ts_ext = roi.TS_ext(which=name) # can comapre to acutal point-like hypothesis

    fit()

    print 'Final Spectral Model for %s hypothesis:' % hypothesis
    roi.print_summary(galactic=True)

    results=sourcedict(roi,name,emin=emin,emax=emax)

    if fit_extension: 
        results['ts_ext_function'] = ts_ext

    if upper_limit:
        results['upper_limit'] = powerlaw_upper_limit(roi,name, verbosity=2)

    roi.save('roi_%s.dat' % hypothesis)

    return results

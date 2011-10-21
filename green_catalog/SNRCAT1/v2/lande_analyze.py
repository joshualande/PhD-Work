# Not entirely sure why, but pyLikelihood
# will get a swig::stop_iteraiton error
# unless it is imported first.
from roi_gtlike import Gtlike


from lande_localize import GridLocalize
from setup_snr import setup_roi, get_snr
from uw.like.roi_plotting import ROISmoothedSource
from uw.like.Models import PowerLaw
from uw.like.roi_extended import ExtendedSource

from toolbag import tolist,sourcedict,powerlaw_upper_limit

import numpy as np
import pylab as P
import pyfits

from argparse import ArgumentParser
import yaml
import os


def overlay_on_plot(axes,header, roi):
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

    # overlay the green catalog SNR in red
    ROISmoothedSource.overlay_extension(get_snr(name,snrdata), axes, header, extension_color='red',
                                       extension_zorder=10)

    temp=yaml.load(open(snrdata))[name]
    if temp.has_key('contour'):
        contour = temp['contour']
        p = pyfits.open(os.path.expandvars(contour['file']))
        hdu = p[contour['hdu']]
        levels = eval(contour['levels'])
        axes[hdu.header].contour(hdu.data, levels, colors='lightblue')

def plots(hypothesis):
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
            overlay_on_plot(smooth.axes, smooth.header, roi)
            P.savefig('%s_%s_kernel_%g_%s.png' % (filename_base,hypothesis,kernel_rad,name))


    # Residual TS Map
    tsmap=roi.plot_tsmap(size = plot_size, pixelsize = 1./8, title='Residual TS Map %s' % name)
    overlay_on_plot(tsmap.axes, tsmap.header, roi)
    P.savefig('tsmap_residual_%s_%s.png' % (hypothesis,name))

    # Source TS Map
    roi.zero_source(name)
    tsmap=roi.plot_tsmap(size = plot_size, pixelsize = 1./8, title='Source TS Map %s' % name)
    overlay_on_plot(tsmap.axes, tsmap.header, roi)
    roi.unzero_source(name)
    P.savefig('tsmap_source_%s_%s.png' % (hypothesis,name))


def gtlike_analysis(roi, upper_limit=False):
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

def pointlike_analysis(roi, hypothesis, localize=False, fit_extension=False):

    print '\n\nPerforming Pointlike analysis for %s hypothesis\n\n' % hypothesis

    def fit():
        """ Convenience function incase fit fails. """
        try:
            roi.fit(use_gradient=True)
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
            size=size=max(snrsize,0.5)
            grid=GridLocalize(roi,which=name,size,pixelsize=size/10)
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

    roi.save('roi_%s.dat' % hypothesis)

    print 'Making Plots for %s hypothesis' % hypothesis
    plots(hypothesis)

    return results


parser = ArgumentParser()
parser.add_argument("--snrdata", required=True)
parser.add_argument("--name", required=True)
parser.add_argument("--emin", type=float, default=1e4)
parser.add_argument("--emax", type=float, default=1e5)

args=parser.parse_args()

name=args.name
snrdata=args.snrdata
emin=args.emin
emax=args.emax

results=dict(name=name)

# *) Build the ROI
roi=setup_roi(name,snrdata, fit_emin=emin, fit_emax=emax)

# get the SNR as an extended source object.

snr_radio_template = get_snr(name, snrdata)
snrsize = snr_radio_template.spatial_model['sigma']

# *) modify the ROI to remove overlaping background sources. 
deleted_sources = []
for source in roi.get_sources():
    if np.degrees(source.skydir.difference(snr_radio_template.skydir)) < snrsize + 0.1:
        deleted_sources.append(roi.del_source(source))

for source in roi.get_sources():
    # Freeze the spectrum (but not flux) of all other sources in the ROI.
    if np.any(source.model.free):
        free=np.asarray([True]+[False]*(len(source.model._p)-1))
        roi.modify(which=source,free=free)


print '\n\nAnalyze SNR with radio template\n\n'

roi.add_source(snr_radio_template)

results['radio'] = {}
results['radio']['pointlike']=pointlike_analysis(roi,'radio')
results['radio']['gtlike']=gtlike_analysis(roi,upper_limit=True)

print '\n\nAnalyze SNR as point-like source\n\n'

# Best to start with initial spectral model, for convergence regions.
roi.del_source(which=name)
roi.add_source(get_snr(name, snrdata, point_like=True))

results['point'] = {}
results['point']['pointlike']=pointlike_analysis(roi,'point', localize=True)
results['point']['gtlike']=gtlike_analysis(roi)

print '\n\nAnalyze SNR as extended source\n\n'

roi.del_source(which=name)
roi.add_source(get_snr(name, snrdata))

results['extended'] = {}
results['extended']['pointlike']=pointlike_analysis(roi, 'extended', fit_extension=True)
results['extended']['gtlike']=gtlike_analysis(roi)


for which in ['pointlike','gtlike']:
    results['extended'][which]['ts_ext'] = \
            2*(results['extended'][which]['logLikelihood'] - \
               results['point'][which]['logLikelihood'])

f=open('results_%s.yaml' % name,'w')
yaml.dump(tolist(results),f)

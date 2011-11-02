# Not entirely sure why, but pyLikelihood
# will get a swig::stop_iteraiton error
# unless it is imported first.

import pylab as P
import numpy as np
from roi_gtlike import Gtlike
import yaml
from toolbag import tolist
from likelihood_tools import sourcedict,powerlaw_upper_limit, test_cutoff, plot_all_seds, paranoid_gtlike_fit
from SED import SED
from LikelihoodState import LikelihoodState
from uw.pulsar.phase_range import PhaseRange

from lande_pulsar import plot_phaseogram,plot_phase_vs_time
from lande_plotting import ROITSMapBandPlotter, ROISourceBandPlotter, ROISourcesBandPlotter


all_energy=lambda emin,emax: np.allclose([emin,emax],[1e2,10**5.5], rtol=0, atol=1)
high_energy=lambda emin,emax: np.allclose([emin,emax],[10**4.5,10**5.5], rtol=0, atol=1)
three_bins=[1e2,1e3,1e4,10**5.5]

def plots(roi, name, hypothesis, emin, emax, datadir, plotdir, size=5, tsmap_pixelsize=0.1):
    plot_kwargs = dict(size=size, pixelsize=tsmap_pixelsize)

    if all_energy(emin,emax):
        ROISourceBandPlotter(roi, which=name, bin_edges=three_bins, size=size).show(filename='%s/band_source_%s_%s.png' % (plotdir,hypothesis,name))
        ROISourcesBandPlotter(roi,which=name, bin_edges=three_bins, size=size).show(filename='%s/band_sources_%s_%s.png' % (plotdir,hypothesis,name))

    print 'Making plots for hypothesis %s' % hypothesis
    roi.plot_tsmap(filename='%s/residual_tsmap_%s_%s.png' % (plotdir,hypothesis,name), **plot_kwargs)

    if all_energy(emin,emax):
        ROITSMapBandPlotter(roi,  bin_edges=three_bins, **plot_kwargs).show(filename='%s/band_residual_tsmap_%s_%s.png' % (plotdir,hypothesis,name))

    for pixelsize in [0.1,0.25]:
        roi.plot_counts_map(filename="%s/counts_%g_%s_%s.png"%(plotdir,pixelsize,hypothesis,name),
                            countsfile="%s/counts_%g_%s_%s.fits"%(datadir,pixelsize,hypothesis,name),
                            modelfile="%s/model_%g_%s_%s.fits"%(datadir,pixelsize,hypothesis,name),
                            **plot_kwargs)

    roi.zero_source(which=name)

    roi.plot_tsmap(filename='%s/source_tsmap_%s_%s.png' % (plotdir,hypothesis, name), **plot_kwargs)

    if np.allclose([emin,emax],[1e2,10**5.5], rtol=0, atol=1):
        ROITSMapBandPlotter(roi,bin_edges=three_bins, **plot_kwargs).show(filename='%s/band_source_tsmap_%s_%s.png' % (plotdir,hypothesis,name))

    for pixelsize in [0.1,0.25]:
        roi.plot_counts_map(filename="%s/counts_excess_%g_%s_%s.png"%(plotdir,pixelsize,hypothesis,name),
                            countsfile="%s/counts_excess_%g_%s_%s.fits"%(datadir,pixelsize,hypothesis,name),
                            modelfile="%s/model_excess_%g_%s_%s.fits"%(datadir,pixelsize,hypothesis,name),
                            **plot_kwargs)
    roi.unzero_source(which=name)

    roi.plot_source(which=name,filename='%s/source_%s_%s.png' % (plotdir, hypothesis, name), 
                    size=size, label_psf=False)
    roi.plot_sources(which=name,filename='%s/sources_%s_%s.png' % (plotdir, hypothesis, name), 
                     size=size, label_psf=False)

    roi.toRegion('%s/region_%s_%s.reg'%(datadir,hypothesis, name))
    roi.plot_slice(which=name,filename="%s/slice_%s_%s.png"%(plotdir,hypothesis, name),
                   datafile='%s/slice_%s_%s.dat'%(datadir,hypothesis, name))
    try:
        roi.plot_counts_spectra(filename="%s/spectra_%s_%s.png"%(plotdir,hypothesis, name))
    except Exception, ex:
        print 'ERROR with plot_counts_spectra: ', ex


def pointlike_analysis(roi, name, hypothesis, emin, emax,
                       seddir, datadir, plotdir,
                       upper_limit=False, localize=False,
                       fit_extension=False, extension_upper_limit=False,
                       do_plots=True, cutoff=False):
    """ emin + emax used for computing upper limits. """
    print 'Performing Pointlike analysis for %s' % hypothesis

    print_summary = lambda: roi.print_summary(galactic=True)
    print_summary()

    print roi

    def fit():
        """ Convenience function incase fit fails. """
        try:
            roi.fit()
        except Exception, ex:
            print 'ERROR spectral fitting pointlike: ', ex
        print_summary()

    fit()

    if localize:
        try:
            roi.localize(name, update=True)
        except Exception, ex:
            print 'ERROR localizing pointlike: ', ex
        fit()

    if fit_extension:
        try:
            roi.fit_extension(name)
            roi.localize(name, update=True)
        except Exception, ex:
            print 'ERROR extension fitting pointlike: ', ex
        fit()

    p = sourcedict(roi, name)

    if extension_upper_limit:
        print 'Calculating extension upper limit'
        p['extension_upper_limit']=roi.extension_upper_limit(which=name, confidence=0.95, spatial_model=Gaussian(), npoints=10)

    if upper_limit:
        p['upper_limit']=powerlaw_upper_limit(roi, name, emin=emin, emax=emax, cl=.95)
    if cutoff:
        p['test_cutoff']=test_cutoff(roi,name)
    print_summary()

    roi.plot_sed(which=name,filename='%s/sed_pointlike_%s_%s.png' % (seddir,hypothesis,name), use_ergs=True)
    plot_all_seds(roi, filename='%s/all_seds_pointlike_%s_%s.png' % (seddir,hypothesis,name), use_ergs=True)

    roi.toXML(filename="%s/srcmodel_pointlike_%s_%s.xml"%(datadir, hypothesis, name))
 
    roi.save('roi_%s_%s.dat' % (hypothesis,name))

    if do_plots: plots(roi, name, hypothesis, emin, emax, datadir, plotdir)
    return p


def gtlike_analysis(roi, name, hypothesis, emin, emax, seddir, datadir, plotdir, upper_limit=False, cutoff=False):
    print 'Performing Gtlike crosscheck for %s' % hypothesis

    gtlike=Gtlike(roi)
    global like
    like=gtlike.like

    paranoid_gtlike_fit(like)

    like.writeXml("%s/srcmodel_gtlike_%s_%s.xml"%(datadir, hypothesis, name))

    r=sourcedict(like, name)

    if upper_limit:
        try:
            r['upper_limit'] = powerlaw_upper_limit(like, name, emin=emin, emax=emax, cl=.95)
        except Exception, ex:
            print 'ERROR gtlike upper limit: ', ex
            r['upper_limit'] = -1
    if cutoff:
        try:
            r['test_cutoff']=test_cutoff(like,name)
        except Exception, ex:
            print 'ERROR gtlike test cutoff: ', ex
            r['test_cutoff']=-1

    r['sed']={}
    def sed(kind,**kwargs):

        print 'Making %s SED' % kind
        sed = SED(like, name, always_upper_limit=True, **kwargs)
        sed.plot('%s/sed_gtlike_%s_%s.png' % (seddir,kind,name)) 
        sed.verbosity=True
        sed.save('%s/sed_gtlike_%s_%s.dat' % (seddir,kind,name))
        r['sed'][kind]=sed.todict()

    if all_energy(emin,emax):
        sed('4bpd_%s' % hypothesis,bin_edges=np.logspace(2,5.5,15))
        sed('2bpd_%s' % hypothesis,bin_edges=np.logspace(2,5.5,8))
        sed('1bpd_%s' % hypothesis,bin_edges=three_bins)
    elif high_energy(emin,emax):
        sed('4bpd_%s' % hypothesis,bin_edges=np.logspace(4.5,5.5,5))
        sed('2bpd_%s' % hypothesis,bin_edges=np.logspace(4.5,5.5,3))
    else:
        # just use regular binning
        sed(hypothesis)

    return r
    
def save_results(results, name): 
    open('results_%s.yaml' % name,'w').write(
        yaml.dump(tolist(results)))


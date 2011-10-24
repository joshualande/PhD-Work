# Not entirely sure why, but pyLikelihood
# will get a swig::stop_iteraiton error
# unless it is imported first.

import numpy as np
from roi_gtlike import Gtlike
import yaml
from toolbag import tolist
from likelihood_tools import sourcedict,powerlaw_upper_limit, test_cutoff, plot_all_seds
from SED import SED

def plots(roi, name, hypothesis, size=5):
    print 'Making plots for hypothesis %s' % hypothesis
    roi.plot_tsmap(filename='residual_tsmap_%s_%s.png' % (hypothesis,name), size=size, pixelsize=0.1)
    for pixelsize in [0.1,0.25]:
        roi.plot_counts_map(filename="counts_%g_%s_%s.png"%(pixelsize,hypothesis,name),
                            countsfile="counts_%g_%s_%s.fits"%(pixelsize,hypothesis,name),
                            modelfile="model_%g_%s_%s.fits"%(pixelsize,hypothesis,name),
                            pixelsize=pixelsize,size=size)
    roi.zero_source(which=name)
    roi.plot_tsmap(filename='source_tsmap_%s_%s.png' % (hypothesis, name), size=size, pixelsize=0.1)
    for pixelsize in [0.1,0.25]:
        roi.plot_counts_map(filename="counts_excess_%g_%s_%s.png"%(pixelsize,hypothesis,name),
                            countsfile="counts_excess_%g_%s_%s.fits"%(pixelsize,hypothesis,name),
                            modelfile="model_excess_%g_%s_%s.fits"%(pixelsize,hypothesis,name),
                            pixelsize=pixelsize,size=size)
    roi.unzero_source(which=name)

    roi.plot_source(which=name,filename='source_%s_%s.png' % (hypothesis, name), 
                    size=size, label_psf=False)
    roi.plot_sources(which=name,filename='sources_%s_%s.png' % (hypothesis, name), 
                     size=size, label_psf=False)

    roi.toRegion('region_%s_%s.reg'%(hypothesis, name))
    roi.toXML(filename="srcmodel_%s_%s.xml"%(hypothesis, name))
    roi.plot_slice(which=name,filename="slice_%s_%s.png"%(hypothesis, name),
                   datafile='slice_%s_%s.dat'%(hypothesis, name))
    try:
        roi.plot_counts_spectra(filename="spectra_%s_%s.png"%(hypothesis, name))
    except Exception, ex:
        print 'ERROR with plot_counts_spectra: ', ex


def pointlike_analysis(roi, name, hypothesis, emin, emax,
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
            print 'ERROR spectral fitting: ', ex
        print_summary()

    fit()

    if localize:
        try:
            roi.localize(name, update=True)
        except Exception, ex:
            print 'ERROR localizing: ', ex
        fit()

    if fit_extension:
        try:
            roi.fit_extension(name)
            roi.localize(name, update=True)
        except Exception, ex:
            print 'ERROR localizing: ', ex
        fit()

    p = sourcedict(roi, name)

    if extension_upper_limit:
        print 'Calculating extension upper limit'
        p['extension_upper_limit']=roi.extension_upper_limit(which=name, confidence=0.95, spatial_model=Gaussian(), npoints=10)

    if upper_limit:
        p['upper_limit'] = powerlaw_upper_limit(roi, name, emin=emin, emax=emax, cl=.95)
    if cutoff:
        p['test_cutoff']=test_cutoff(roi,name)

    roi.plot_sed(which=name,filename='sed_pointlike_%s_%s.png' % (hypothesis,name), use_ergs=True)
    plot_all_seds(roi, filename='all_seds_pointlike_%s_%s.png' % (hypothesis,name), use_ergs=True)
 
    roi.save('roi_%s_%s.dat' % (hypothesis,name))

    if do_plots: plots(roi, name, hypothesis)
    return p

def gtlike_analysis(roi, name, hypothesis, emin, emax, upper_limit=False, cutoff=False):
    print 'Performing Gtlike crosscheck for %s' % hypothesis

    gtlike=Gtlike(roi)
    like=gtlike.like
    like.fit(covar=True)

    r=sourcedict(like, name)

    if upper_limit:
        r['upper_limit'] = powerlaw_upper_limit(like, name, emin=emin, emax=emax, cl=.95)
    
    if cutoff:
        r['test_cutoff']=test_cutoff(like,name)

    def sed(kind,**kwargs):

        print 'Making %s SED' % kind
        sed = SED(like, name, **kwargs)
        sed.plot('sed_gtlike_%s_%s.png' % (kind,name)) 
        sed.verbosity=True
        sed.save('sed_gtlike_%s_%s.dat' % (kind,name))

    if np.allclose([emin,emax],[1e2,10**5.5], rtol=0, atol=1):
        sed('4bpd_%s' % hypothesis,bin_edges=np.logspace(2,10**5.5,15))
        sed('1bpd_%s' % hypothesis,bin_edges=[1e2, 1e3, 1e4,10**5.5])
    else:
        # just use regular binning
        sed(hypothesis)

    return r
    
def save_results(results, name): 
    open('results_%s.yaml' % name,'w').write(
        yaml.dump(tolist(results)))


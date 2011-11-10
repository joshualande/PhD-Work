# Not entirely sure why, but pyLikelihood
# will get a swig::stop_iteraiton error
# unless it is imported first.

import pylab as P
import numpy as np
from roi_gtlike import Gtlike
import yaml
from toolbag import tolist
from likelihood_tools import sourcedict,powerlaw_upper_limit, test_cutoff, plot_all_seds, paranoid_gtlike_fit
from LikelihoodState import LikelihoodState
from uw.pulsar.phase_range import PhaseRange
from uw.like.SpatialModels import Gaussian

from lande_extended import fit_extension_frozen
from lande_pulsar import plot_phaseogram,plot_phase_vs_time
from lande_plotting import ROITSMapBandPlotter, ROISourceBandPlotter, ROISourcesBandPlotter,plot_gtlike_cutoff_test
from lande_sed import LandeSED


all_energy=lambda emin,emax: np.allclose([emin,emax],[1e2,10**5.5], rtol=0, atol=1)
high_energy=lambda emin,emax: np.allclose([emin,emax],[10**4.5,10**5.5], rtol=0, atol=1)
three_bins=[1e2,1e3,1e4,10**5.5]

def plots(roi, name, hypothesis, emin, emax, 
          datadir, plotdir, size=5, tsmap_pixelsize=0.1):
    plot_kwargs = dict(size=size, pixelsize=tsmap_pixelsize)

    print 'Making plots for hypothesis %s' % hypothesis
    roi.plot_tsmap(filename='%s/tsmap_residual_%s_%s.png' % (plotdir,hypothesis,name), 
                   title='Residual TS Map for %s' % name,
                   **plot_kwargs)

    if all_energy(emin,emax):
        ROITSMapBandPlotter(roi,  bin_edges=three_bins, **plot_kwargs).show(filename='%s/band_tsmap_residual_%s_%s.png' % (plotdir,hypothesis,name))

    for pixelsize in [0.1,0.25]:
        roi.plot_counts_map(filename="%s/counts_residual_%g_%s_%s.png"%(plotdir,pixelsize,hypothesis,name),
                            countsfile="%s/counts_residual_%g_%s_%s.fits"%(datadir,pixelsize,hypothesis,name),
                            modelfile="%s/model_residual_%g_%s_%s.fits"%(datadir,pixelsize,hypothesis,name),
                            size=size, pixelsize=pixelsize)

    roi.zero_source(which=name)

    roi.plot_tsmap(filename='%s/tsmap_source_%s_%s.png' % (plotdir,hypothesis, name), 
                   title='Source TS Map for %s' % name,
                   **plot_kwargs)

    if np.allclose([emin,emax],[1e2,10**5.5], rtol=0, atol=1):
        ROITSMapBandPlotter(roi,bin_edges=three_bins, **plot_kwargs).show(filename='%s/band_tsmap_source_%s_%s.png' % (plotdir,hypothesis,name))

    for pixelsize in [0.1,0.25]:
        roi.plot_counts_map(filename="%s/counts_source_%g_%s_%s.png"%(plotdir,pixelsize,hypothesis,name),
                            countsfile="%s/counts_source_%g_%s_%s.fits"%(datadir,pixelsize,hypothesis,name),
                            modelfile="%s/model_source_%g_%s_%s.fits"%(datadir,pixelsize,hypothesis,name),
                            size=size, pixelsize=pixelsize)
    roi.unzero_source(which=name)

    # smoothed counts maps

    for kernel_rad in [0.1,0.25]:
        kwargs = dict(which=name, size=size, kernel_rad=kernel_rad)
        roi.plot_source(filename='%s/source_%g_%s_%s.png' % (plotdir, kernel_rad, hypothesis, name), **kwargs)
        roi.plot_sources(filename='%s/sources_%g_%s_%s.png' % (plotdir, kernel_rad, hypothesis, name), **kwargs)

        if all_energy(emin,emax):
            ROISourceBandPlotter(roi, bin_edges=three_bins, **kwargs).show(filename='%s/band_source_%g_%s_%s.png' % (plotdir,kernel_rad,hypothesis,name))
            ROISourcesBandPlotter(roi, bin_edges=three_bins, **kwargs).show(filename='%s/band_sources_%g_%s_%s.png' % (plotdir,kernel_rad,hypothesis,name))


    roi.toRegion('%s/region_%s_%s.reg'%(datadir,hypothesis, name))
    roi.plot_slice(which=name,filename="%s/slice_%s_%s.png"%(plotdir,hypothesis, name),
                   datafile='%s/slice_%s_%s.dat'%(datadir,hypothesis, name))

    roi.plot_radial_integral(which=name,filename="%s/radial_integral_%s_%s.png"%(plotdir,hypothesis, name),
                             datafile='%s/radial_integral_%s_%s.dat'%(datadir,hypothesis, name))
    try:
        roi.plot_counts_spectra(filename="%s/spectra_%s_%s.png"%(plotdir,hypothesis, name))
    except Exception, ex:
        print 'ERROR with plot_counts_spectra: ', ex


def pointlike_analysis(roi, name, hypothesis, emin, emax, localization_emin,
                       seddir, datadir, plotdir,
                       upper_limit=False, localize=False,
                       fit_extension=False, extension_upper_limit=False,
                       cutoff=False, seds=False):
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
            if localization_emin != emin: roi.change_binning(localization_emin,emax)
            roi.localize(name, update=True)
        except Exception, ex:
            print 'ERROR localizing pointlike: ', ex
        finally:
            if localization_emin != emin: roi.change_binning(emin,emax)
        fit()

    if fit_extension:
        try:
            if localization_emin != emin: roi.change_binning(localization_emin,emax)
            fit_extension_frozen(roi,name)
            roi.localize(name, update=True)
        except Exception, ex:
            print 'ERROR extension fitting pointlike: ', ex
        finally:
            if localization_emin != emin: roi.change_binning(emin,emax)
        fit()

    p = sourcedict(roi, name)

    if extension_upper_limit:
        print 'Calculating extension upper limit'
        p['extension_upper_limit']=roi.extension_upper_limit(which=name, confidence=0.95, spatial_model=Gaussian())

    if upper_limit:
        p['upper_limit']=powerlaw_upper_limit(roi, name, emin=emin, emax=emax, cl=.95)
    if cutoff:
        p['test_cutoff']=test_cutoff(roi,name)
    print_summary()

    if seds:
        roi.plot_sed(which=name,filename='%s/sed_pointlike_%s_%s.png' % (seddir,hypothesis,name), use_ergs=True)
        plot_all_seds(roi, filename='%s/all_seds_pointlike_%s_%s.png' % (seddir,hypothesis,name), use_ergs=True)

    roi.toXML(filename="%s/srcmodel_pointlike_%s_%s.xml"%(datadir, hypothesis, name))
 
    roi.save('roi_%s_%s.dat' % (hypothesis,name))

    return p


def gtlike_analysis(roi, name, hypothesis, emin, emax, seddir, datadir, plotdir, upper_limit=False, cutoff=False, seds=False):
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

    def sed(kind,**kwargs):
        print 'Making %s SED' % kind
        sed = LandeSED(like, name, always_upper_limit=True, **kwargs)
        sed.plot('%s/sed_gtlike_%s_%s.png' % (seddir,kind,name)) 
        sed.save('%s/sed_gtlike_%s_%s.yaml' % (seddir,kind,name))

    if seds:
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

    if cutoff:
        try:
            r['test_cutoff']=test_cutoff(like,name)
            plot_gtlike_cutoff_test(cutoff_results=r['test_cutoff'],
                                    sed_results='%s/sed_gtlike_2bpd_%s_%s.yaml' % (seddir,hypothesis,name),
                                    filename='%s/test_cutoff_%s_%s.png' % (plotdir,hypothesis,name))
        except Exception, ex:
            print 'ERROR gtlike test cutoff: ', ex
            r['test_cutoff']=-1

    return r
    
def save_results(results, name): 
    open('results_%s.yaml' % name,'w').write(
        yaml.dump(tolist(results)))


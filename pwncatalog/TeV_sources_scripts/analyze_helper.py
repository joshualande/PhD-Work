# Not entirely sure why, but pyLikelihood
# will get a swig::stop_iteraiton error
# unless it is imported first.
import os
import pylab as P
import numpy as np
from roi_gtlike import Gtlike
import yaml
from toolbag import tolist
from likelihood_tools import sourcedict,powerlaw_upper_limit, test_cutoff, plot_all_seds, paranoid_gtlike_fit,freeze_insignificant_to_catalog,fix_bad_cutoffs,fit_prefactor
from uw.like.roi_state import PointlikeState
from uw.pulsar.phase_range import PhaseRange
from uw.like.SpatialModels import Gaussian

from lande_extended import fit_extension_frozen
from lande_pulsar import plot_phaseogram,plot_phase_vs_time
from lande_plotting import ROITSMapBandPlotter, ROISourceBandPlotter, ROISourcesBandPlotter,plot_gtlike_cutoff_test
from lande_sed import LandeSED

from setup_pwn import get_catalog

all_energy=lambda emin,emax: np.allclose([emin,emax],[1e2,10**5.5], rtol=0, atol=1)
high_energy=lambda emin,emax: np.allclose([emin,emax],[10**4,10**5.5], rtol=0, atol=1) 
higher_energy=lambda emin,emax: np.allclose([emin,emax],[10**4.5,10**5.5], rtol=0, atol=1)

three_bins=[1e2,1e3,1e4,10**5.5]

def plots(roi, name, hypothesis, emin, emax, 
          datadir='data', plotdir='plots', size=5, tsmap_pixelsize=0.1):
    plot_kwargs = dict(size=size, pixelsize=tsmap_pixelsize)

    for dir in [datadir, plotdir]: 
        if not os.path.exists(dir): os.makedirs(dir)

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
        print kwargs
        try :
            roi.plot_source(filename='%s/source_%g_%s_%s.png' % (plotdir, kernel_rad, hypothesis, name), **kwargs)
            roi.plot_sources(filename='%s/sources_%g_%s_%s.png' % (plotdir, kernel_rad, hypothesis, name), **kwargs)
        except :
            print "pas reussi a tracer %s/source_%g_%s_%s.png" % (plotdir, kernel_rad, hypothesis, name)
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


def pointlike_analysis(roi, name, hypothesis, emin, emax, localization_emin=None,
                       seddir='seds', datadir='data', plotdir='plots',
                       upper_limit=False, localize=False,
                       fit_extension=False, extension_upper_limit=False,
                       cutoff=False, seds=False):
    """ emin + emax used for computing upper limits. """
    print 'Performing Pointlike analysis for %s' % hypothesis

    for dir in [seddir, datadir, plotdir]: 
        if not os.path.exists(dir): os.makedirs(dir)

    print_summary = lambda: roi.print_summary(galactic=True)
    print_summary()

    print roi

    def fit(just_prefactor=False):
        """ Convenience function incase fit fails. """
        try:
            if just_prefactor:
                fit_prefactor(roi, name) 
            else:
                roi.fit()
                # For some reason, one final fit seems to help with convergence and not getting negative TS values *shurgs*
                roi.fit() 
        except Exception, ex:
            print 'ERROR spectral fitting pointlike: ', ex
        print_summary()

    saved_state = PointlikeState(roi)

    # More robust to first fit the prefactor of PWN since the starting value is often very bad
    fit(just_prefactor=True)

    sav_model=roi.get_model(which=name)

    saved_state.restore()

    roi.modify(which=name,model=sav_model)

    fit()
    freeze_insignificant_to_catalog(roi, get_catalog(), exclude_names=[name], min_ts=500)
    fit() 
    fix_bad_cutoffs(roi, exclude_names=[name])
    # second fit necessary after these fixes, which change around sources.
    fit()

    if roi.TS(which=name,quick=False)<20.0:
        from uw.like.Models import PowerLaw
        roi.modify(which=name,model=PowerLaw(p=[1.0e-15,2.0]),free=[True,False])

    if localize:
        try:
            if localization_emin is not None and localization_emin != emin: 
                roi.change_binning(localization_emin,emax)
            roi.localize(name, update=True)
        except Exception, ex:
            print 'ERROR localizing pointlike: ', ex
        finally:
            if localization_emin is not None and localization_emin != emin: 
                roi.change_binning(emin,emax)
        fit()

    if fit_extension:
        init_flux = roi.get_model(which=name).i_flux(emin,emax)
        try:
            if localization_emin is not None and localization_emin != emin: 
                before_state = PointlikeState(roi)
                roi.change_binning(localization_emin,emax)

            fit_extension_frozen(roi,name)
            roi.localize(name, update=True)

        except Exception, ex:
            print 'ERROR extension fitting pointlike: ', ex
        finally:
            if localization_emin is not None and localization_emin != emin: 

                # after switching energy range, the fit may have gone horribly
                # wrong (due to being a different energy range). 
                # A good strategy to improve robustness of fit
                # is to set the ROI back to what it was before extnesion
                # fit and then modify just the spatial model
                # to what the fit found.
                spatial_model = roi.get_source(name).spatial_model
                before_state.restore() # This restores previous energy
                roi.modify(which=name, spatial_model=spatial_model, keep_old_center=False)
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


def gtlike_analysis(roi, name, hypothesis, emin, emax, 
                    seddir='seds', datadir='data', plotdir='plots',
                    upper_limit=False, cutoff=False, seds=False):
    print 'Performing Gtlike crosscheck for %s' % hypothesis

    for dir in [seddir, datadir, plotdir]: 
        if not os.path.exists(dir): os.makedirs(dir)

    gtlike=Gtlike(roi)
    global like
    like=gtlike.like

    paranoid_gtlike_fit(like)

    like.writeXml("%s/srcmodel_gtlike_%s_%s.xml"%(datadir, hypothesis, name))

    r=sourcedict(like, name)

    if upper_limit:
        r['upper_limit'] = powerlaw_upper_limit(like, name, emin=emin, emax=emax, cl=.95, delta_log_like_limits=10)

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
            sed('4bpd_%s' % hypothesis,bin_edges=np.logspace(4,5.5,7))
            sed('2bpd_%s' % hypothesis,bin_edges=np.logspace(4,5.5,4))
        elif higher_energy(emin,emax):
            sed('4bpd_%s' % hypothesis,bin_edges=np.logspace(4.5,5.5,5))
            sed('2bpd_%s' % hypothesis,bin_edges=np.logspace(4.5,5.5,3))
        else:
            # just use regular binning
            sed(hypothesis)

    if cutoff:
        r['test_cutoff']=test_cutoff(like,name)
        try:
            plot_gtlike_cutoff_test(cutoff_results=r['test_cutoff'],
                                    sed_results='%s/sed_gtlike_2bpd_%s_%s.yaml' % (seddir,hypothesis,name),
                                    filename='%s/test_cutoff_%s_%s.png' % (plotdir,hypothesis,name))
        except Exception, ex:
            print 'ERROR plotting cutoff test:', ex

    return r
    
def save_results(results, name): 
    open('results_%s.yaml' % name,'w').write(
        yaml.dump(tolist(results)))


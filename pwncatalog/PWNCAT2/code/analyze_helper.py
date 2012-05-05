# Not entirely sure why, but pyLikelihood
# will get a swig::stop_iteraiton error
# unless it is imported first.
from lande.fermi.likelihood.roi_gtlike import Gtlike

import traceback
import sys
import os
import pylab as P
import numpy as np

import yaml

from uw.like.roi_state import PointlikeState
from uw.pulsar.phase_range import PhaseRange
from uw.like.SpatialModels import Gaussian

from lande.utilities.tools import tolist

from lande.fermi.sed.plotting import plot_all_seds
from lande.fermi.likelihood.fit import paranoid_gtlike_fit, fit_prefactor, freeze_insignificant_to_catalog, freeze_bad_index_to_catalog
from lande.fermi.likelihood.save import sourcedict, get_full_energy_range
from lande.fermi.likelihood.limits import powerlaw_upper_limit
from lande.fermi.likelihood.localize import GridLocalize, paranoid_localize
from lande.fermi.likelihood.cutoff import plot_gtlike_cutoff_test, test_cutoff, fix_bad_cutoffs
from lande.fermi.likelihood.bandfitter import BandFitter
from lande.fermi.pulsar.plotting import plot_phaseogram,plot_phase_vs_time
from lande.fermi.sed.supersed import SuperSED
from lande.fermi.data.plotting import ROITSMapBandPlotter, ROISourceBandPlotter, ROISourcesBandPlotter

from setup_pwn import PWNRegion

close=lambda x,y: np.allclose(x,y, rtol=0, atol=1)
all_energy=lambda emin,emax: close([emin,emax],[1e2,10**5.5]) or close([emin,emax],[1e2,1e5])
high_energy=lambda emin,emax: close([emin,emax],[10**4,10**5.5])
higher_energy=lambda emin,emax: close([emin,emax],[10**4.5,10**5.5])

def one_bin_per_dec(emin,emax):
    assert close(emin,1e2) and (close(emax,1e5) or close(emax,10**5.5))
    if close(emax,1e5):
        return np.logspace(2,5,4)
    elif close(emax,10*5.5):
        return [1e2,1e3,1e4,10**5.5]

def two_bin_per_dec(emin,emax):
    assert close(emin,1e2) and (close(emax,1e5) or close(emax,10**5.5))
    if close(emax,1e5):
        return np.logspace(2,5,7)
    elif close(emax,10*5.5):
        return np.logspace(2,5.5,8)

def four_bin_per_dec(emin,emax):
    assert close(emin,1e2) and (close(emax,1e5) or close(emax,10**5.5))
    if close(emax,1e5):
        return np.logspace(2,5,13)
    elif close(emax,10*5.5):
        return np.logspace(2,5.5,15)

def overlay_on_plot(axes, pulsar_position):
    """ Function to overlay on all plots
        * The pulsar position
        * New non-2FGL sources addded to the ROI. """
    axes['gal'].plot([pulsar_position.l()],[pulsar_position.b()], 
                     marker='*', color='green',
                     markeredgecolor='white', markersize=12, zorder=1)

def tsmap_plots(roi, name, hypothesis, datadir, plotdir, size, tsmap_pixelsize=0.1, **common_kwargs):
    """ TS maps """
    emin, emax = get_full_energy_range(roi)

    tsmap_kwargs = dict(size=size, pixelsize=tsmap_pixelsize, **common_kwargs)

    roi.plot_tsmap(filename='%s/tsmap_residual_%s_%s_%sdeg.png' % (plotdir,hypothesis,name,size), 
                   title='Residual TS Map for %s' % name,
                   **tsmap_kwargs)

    if all_energy(emin,emax):
        ROITSMapBandPlotter(roi,  bin_edges=one_bin_per_dec(emin,emax), **tsmap_kwargs).show(filename='%s/band_tsmap_residual_%s_%s_%sdeg.png' % (plotdir,hypothesis,name,size))

    roi.zero_source(which=name)

    roi.plot_tsmap(filename='%s/tsmap_source_%s_%s_%sdeg.png' % (plotdir,hypothesis, name,size), 
                   title='Source TS Map for %s' % name,
                   **tsmap_kwargs)

    if all_energy(emin,emax):
        ROITSMapBandPlotter(roi,bin_edges=one_bin_per_dec(emin,emax), **tsmap_kwargs).show(filename='%s/band_tsmap_source_%s_%s_%sdeg.png' % (plotdir,hypothesis,name,size))

    roi.unzero_source(which=name)

def counts_plots(roi, name, hypothesis, datadir, plotdir, size, **common_kwargs):
    """ Counts plots """
    emin, emax = get_full_energy_range(roi)

    counts_kwargs = dict(size=size, **common_kwargs)
    for pixelsize in [0.1,0.25]:
        roi.plot_counts_map(filename="%s/counts_residual_%g_%s_%s_%sdeg.png"%(plotdir,pixelsize,hypothesis,name,size),
                            countsfile="%s/counts_residual_%g_%s_%s_%sdeg.fits"%(datadir,pixelsize,hypothesis,name,size),
                            modelfile="%s/model_residual_%g_%s_%s_%sdeg.fits"%(datadir,pixelsize,hypothesis,name,size),
                            pixelsize=pixelsize,
                            **counts_kwargs)


    roi.zero_source(which=name)

    for pixelsize in [0.1,0.25]:
        roi.plot_counts_map(filename="%s/counts_source_%g_%s_%s_%sdeg.png"%(plotdir,pixelsize,hypothesis,name,size),
                            countsfile="%s/counts_source_%g_%s_%s_%sdeg.fits"%(datadir,pixelsize,hypothesis,name,size),
                            modelfile="%s/model_source_%g_%s_%s_%sdeg.fits"%(datadir,pixelsize,hypothesis,name,size),
                            pixelsize=pixelsize,
                            **counts_kwargs)
    roi.unzero_source(which=name)

    roi.plot_slice(which=name,filename="%s/slice_%s_%s.png"%(plotdir,hypothesis, name),
                   datafile='%s/slice_%s_%s.dat'%(datadir,hypothesis, name))

    roi.plot_radial_integral(which=name,filename="%s/radial_integral_%s_%s.png"%(plotdir,hypothesis, name),
                             datafile='%s/radial_integral_%s_%s.dat'%(datadir,hypothesis, name))
    try:
        roi.plot_counts_spectra(filename="%s/spectra_%s_%s.png"%(plotdir,hypothesis, name))
    except Exception, ex:
        print 'ERROR with plot_counts_spectra: ', ex
        traceback.print_exc(file=sys.stdout) 

def smooth_plots(roi, name, hypothesis, datadir, plotdir, size, **common_kwargs):
    """ smoothed counts maps """
    emin, emax = get_full_energy_range(roi)

    smooth_kwargs = dict(which=name, 
                         override_center=roi.roi_dir,
                         size=size,
                         colorbar_radius=1, # most interesting within one degrees
                         **common_kwargs)

    for kernel_rad in [0.1,0.25]:
        roi.plot_source(filename='%s/source_%g_%s_%s_%sdeg.png' % (plotdir, kernel_rad, hypothesis, name, size), kernel_rad=kernel_rad, **smooth_kwargs)
        roi.plot_sources(filename='%s/sources_%g_%s_%s_%sdeg.png' % (plotdir, kernel_rad, hypothesis, name, size), kernel_rad=kernel_rad, **smooth_kwargs)

        if all_energy(emin,emax):
            ROISourceBandPlotter(roi, bin_edges=one_bin_per_dec(emin,emax), kernel_rad=kernel_rad, **smooth_kwargs).show(filename='%s/band_source_%g_%s_%s_%sdeg.png' % (plotdir,kernel_rad,hypothesis,name,size))
            ROISourcesBandPlotter(roi, bin_edges=one_bin_per_dec(emin,emax), kernel_rad=kernel_rad, **smooth_kwargs).show(filename='%s/band_sources_%g_%s_%s_%sdeg.png' % (plotdir,kernel_rad,hypothesis,name,size))


def plots(roi, name, hypothesis, 
          pulsar_position, new_sources,
          datadir='data', plotdir='plots', 
          tsmap_pixelsize=0.1):

    print 'Making plots for hypothesis %s' % hypothesis

    extra_overlay = lambda ax: overlay_on_plot(ax, pulsar_position=pulsar_position)

    # Override marker for new sources to be red stars
    override_kwargs = {source.name:dict(color='red',marker='*') for source in new_sources}

    common_kwargs = dict(extra_overlay=extra_overlay, 
                         overlay_kwargs=dict(override_kwargs=override_kwargs))

    for dir in [datadir, plotdir]: 
        if not os.path.exists(dir): os.makedirs(dir)

    #for size in [5,10]:
    for size in [5]:
        args = (roi, name, hypothesis, datadir, plotdir, size)
        counts_plots(*args, **common_kwargs)
        smooth_plots(*args, **common_kwargs)
        tsmap_plots(*args, tsmap_pixelsize=0.1, **common_kwargs)

    roi.toRegion('%s/region_%s_%s.reg'%(datadir,hypothesis, name))

def pointlike_analysis(roi, name, hypothesis, localization_emin=None,
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

    emin, emax = get_full_energy_range(roi)

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
            traceback.print_exc(file=sys.stdout)
        print_summary()

    # More robust to first fit the prefactor of PWN since the starting value is often very bad
    fit(just_prefactor=True)

    while 1:
        fit()
        any_changed = freeze_bad_index_to_catalog(roi, PWNRegion.get_catalog(), exclude_names=[name], min_ts=9)
        fit()
        any_changed = any_changed or freeze_insignificant_to_catalog(roi, PWNRegion.get_catalog(), exclude_names=[name], min_ts=9)
        fit() 
        any_changed = any_changed or fix_bad_cutoffs(roi, exclude_names=[name])
        if not any_changed:
            break

    # second fit necessary after these fixes, which change around sources.
    fit() 

    if localize:
        try:
            if localization_emin is not None and localization_emin != emin: 
                roi.change_binning(localization_emin,emax)

            print 'About to Grid localize'
            grid=GridLocalize(roi,which=name,
                              update=True,
                              size=0.5, pixelsize=0.1)
            print_summary()

            paranoid_localize(roi, name, update=True)
        except Exception, ex:
            print 'ERROR localizing pointlike: ', ex
            traceback.print_exc(file=sys.stdout)
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

            roi.fit_extension(which=name)
            paranoid_localize(roi, name, update=True)

        except Exception, ex:
            print 'ERROR extension fitting pointlike: ', ex
            traceback.print_exc(file=sys.stdout)
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
        p['extension_upper_limit']=roi.extension_upper_limit(which=name, confidence=0.95, spatial_model=Gaussian)

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


def gtlike_analysis(roi, name, hypothesis, 
                    seddir='seds', datadir='data', plotdir='plots',
                    upper_limit=False, cutoff=False, seds=False):
    print 'Performing Gtlike crosscheck for %s' % hypothesis

    for dir in [seddir, datadir, plotdir]: 
        if not os.path.exists(dir): os.makedirs(dir)

    gtlike=Gtlike(roi)
    global like
    like=gtlike.like

    emin, emax = get_full_energy_range(like)

    paranoid_gtlike_fit(like)

    like.writeXml("%s/srcmodel_gtlike_%s_%s.xml"%(datadir, hypothesis, name))

    r=sourcedict(like, name)

    if upper_limit:
        r['upper_limit'] = powerlaw_upper_limit(like, name, emin=emin, emax=emax, cl=.95, delta_log_like_limits=10)

    if all_energy(emin,emax):
        bf = BandFitter(like, name, bin_edges=one_bin_per_dec(emin,emax))
        r['bands'] = bf.todict()

    def sed(kind,**kwargs):
        print 'Making %s SED' % kind
        sed = SuperSED(like, name, always_upper_limit=True, **kwargs)
        sed.plot('%s/sed_gtlike_%s_%s.png' % (seddir,kind,name)) 
        sed.save('%s/sed_gtlike_%s_%s.yaml' % (seddir,kind,name))

    if seds:
        if all_energy(emin,emax):
            sed('1bpd_%s' % hypothesis,bin_edges=one_bin_per_dec(emin,emax))
            sed('2bpd_%s' % hypothesis,bin_edges=two_bin_per_dec(emin,emax))
            sed('4bpd_%s' % hypothesis,bin_edges=four_bin_per_dec(emin,emax))
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
            traceback.print_exc(file=sys.stdout)

    return r
    
def save_results(results, name): 
    open('results_%s.yaml' % name,'w').write(
        yaml.dump(tolist(results)))

def import_module(filename):
    """ import a python module from a pathname. """
    import imp
    return imp.load_source('module',filename)


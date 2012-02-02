
""" This file contains various function which I have found useful. """
import pprint
from math import ceil
import traceback
import sys

import pylab as P
import numpy as np
import pyfits as pf

from mpl_toolkits.axes_grid1 import AxesGrid

from uw.like.roi_analysis import ROIAnalysis
from uw.like.roi_extended import ExtendedSource
from uw.like.Models import Model,PowerLaw,ExpCutoff,DefaultModelValues
from uw.like.roi_state import PointlikeState

from lande_toolbag import tolist
from SED import SED
from LikelihoodState import LikelihoodState

import lande_units as units


def gtlike_or_pointlike(f_gtlike, f_pointlike, like_or_roi, *args, **kwargs):

    from BinnedAnalysis import BinnedAnalysis

    if isinstance(like_or_roi, BinnedAnalysis):
        f=f_gtlike
    elif isinstance(like_or_roi, ROIAnalysis):
        f=f_pointlike
    else:
        raise Exception("like_or_roi must be of type BinnedAnalysis or ROIAnalysis")
    return f(like_or_roi, *args, **kwargs)


def gtlike_get_full_energy_range(like): return like.energies[[0,-1]]
def pointlike_get_full_energy_range(roi): return roi.bin_edges[[0,-1]]

def paranoid_gtlike_fit(like, covar=True):
    """ Perform a sepctral fit in gtlike in
        a paranoid manner. 
        
        See here for description of method:
            http://fermi.gsfc.nasa.gov/ssc/data/analysis/documentation/Cicerone/Cicerone_Likelihood/Fitting_Models.html
    """
    saved_state = LikelihoodState(like)
    try:
        print 'First, fitting with minuit'
        like.fit(optimizer="MINUIT",covar=covar)
    except Exception, ex:
        print 'Minuit fit failed with optimizer=MINUIT, Try again with DRMNFB + NEWMINUIT!', ex
        traceback.print_exc(file=sys.stdout)
        saved_state.restore()

        try:
            saved_state = LikelihoodState(like)
            print 'Refitting, first with DRMNFB'
            like.fit(optimizer='DRMNFB', covar=False)
            print 'Refitting, second with NEWMINUIT'
            like.fit(optimizer='NEWMINUIT', covar=covar)
        except Exception, ex:
            print 'ERROR spectral fitting with DRMNFB + NEWMINUIT: ', ex
            traceback.print_exc(file=sys.stdout)
            saved_state.restore()
            try:
                saved_state = LikelihoodState(like)
                print 'Refitting with LBFGS'
                like.fit(optimizer='LBFGS', covar=covar)
            except Exception, ex:
                print 'ERROR spectral fitting with LBFGS', ex
                traceback.print_exc(file=sys.stdout)


def pointlike_spectrum_to_dict(model, errors=False):

    d = dict(name = model.name)
    default = DefaultModelValues.simple_models[model.name]
    for k,v in default.items():
        if k == '_p': continue
        elif k == 'param_names': 
            for p in v: 
                d[p]=model[p]
                d['%s_err' % p]=model.error(p)
        else: 
            d[k]=getattr(model,k)

    return tolist(d)




def gtlike_flux_dict(like,name,emin=None,emax=None,flux_units='erg', error=True):

    if emin is None and emax is None: 
        emin, emax = get_full_energy_range(like)

    ce=lambda e: units.convert(e,'MeV',flux_units)
    f=dict(flux=like.flux(name,emin=emin,emax=emax),
           eflux=ce(like.energyFlux(name,emin=emin,emax=emax)),
           flux_units='ph/cm^2/s',
           eflux_units='%s/cm^2/s' % flux_units,
           emin=emin,
           emax=emax)

    if error:
        try:
            # incase the errors were not calculated
            f['flux_err']=like.fluxError(name,emin=emin,emax=emax)
            f['eflux_err']=ce(like.energyFluxError(name,emin=emin,emax=emax))
        except Exception, ex:
            print 'ERROR calculating flux error: ', ex
            traceback.print_exc(file=sys.stdout)
            f['flux_err']=-1
            f['eflux_err']=-1
    return f

def gtlike_sourcedict(like, name, emin=None, emax=None, flux_units='erg'):
    from pyLikelihood import ParameterVector

    if emin is None and emax is None:
        emin, emax = get_full_energy_range(like)

    d=dict(
        TS=like.Ts(name,reoptimize=True),
        logLikelihood=like.logLike.value()
    )

    d['flux']=gtlike_flux_dict(like,name,emin,emax,flux_units)

    source = like.logLike.getSource(name)
    spectrum = source.spectrum()

    d['model']=spectrum_to_dict(spectrum, errors=True)

    # Save out gal+iso values.
    # Warning: this implementation is fragile in that
    # (a) the galacitc must have 'gal' in it and the isotropic
    #     must have 'iso' in it 
    # (b) all other sources cannot have 'gal' or 'iso' in them.
    # (c) gal must be scaled by a powerlaw, iso must be scaled by a constant

    def get(sourcename,param):
        source = like.logLike.getSource(sourcename)
        spectrum = source.spectrum()
        p = spectrum.getParam(param)
        return dict(value=p.getTrueValue(),
                    error=p.error()*p.getScale())

    def get_full_name(substr):
        all_sources=np.char.lower(like.sourceNames())
        f = np.char.find(all_sources,substr) != -1
        if not np.any(f): return None
        index = np.where(f)[0][0]
        return like.sourceNames()[index]

    d['diffuse'] = f = {}

    galname = get_full_name('galactic')
    if galname is None: galname = get_full_name('ring')
    if galname is not None: 
        f['galnorm'] = get(galname,'Prefactor')
        f['galindex'] = get(galname,'Index')

    isoname = get_full_name('isotropic')
    if isoname is None: isoname = get_full_name('extragalactic')
    if isoname is not None: 
        f['isonorm'] = get(isoname,'Normalization')

    return d


def pointlike_flux_dict(roi,which,emin=None,emax=None,flux_units='erg', error=True):

    if emin is None and emax is None:
        emin, emax = get_full_energy_range(roi)

    model=roi.get_model(which)
    ce=lambda e: units.convert(e,'MeV',flux_units)
    f=dict()
    if error:
        f['flux'],f['flux_err']=model.i_flux(emin=emin,emax=emax,error=True)
        ef,ef_err=model.i_flux(emin=emin,emax=emax,e_weight=1,error=True)
        f['eflux'],f['eflux_err']=ce(ef),ce(ef_err)
    else:
        f['flux']=model.i_flux(emin=emin,emax=emax,error=False)
        ef=model.i_flux(emin=emin,emax=emax,e_weight=1,error=False)
        f['eflux']=ce(ef)

    f['flux_units']='ph/cm^2/s'
    f['eflux_units']='%s/cm^2/s' % flux_units
    f['emin'],f['emax']=emin,emax
    return f


def pointlike_sourcedict(roi, name, emin, emax, flux_units='erg'):
    d={}

    if emin is None and emax is None:
        emin, emax = get_full_energy_range(roi)

    source=roi.get_source(name)
    model=roi.get_model(name)

    old_quiet = roi.quiet; roi.quiet=True
    d['TS'] = roi.TS(name,quick=False)
    roi.quiet = old_quiet

    d['logLikelihood']=-roi.logLikelihood(roi.parameters())

    d['flux']=pointlike_flux_dict(roi,name,emin,emax,flux_units)

    d['model']=spectrum_to_dict(model, errors=True)

    # Source position
    d['gal'] = [source.skydir.l(),source.skydir.b()]
    d['equ'] = [source.skydir.ra(),source.skydir.dec()]

    f = d['spatial_model'] = dict()
    if isinstance(source,ExtendedSource):
        # Extended Source parameters
        spatial_model = source.spatial_model
        for param in spatial_model.param_names:
            f[param]=spatial_model[param]
            f[param + '_err']=spatial_model.error(param)

    # add elliptical error, if they exist.
    # N.B. If no localization performed, this will return
    # an empty dictionary.
    # N.B. This method will do the wrong thing if you have recently relocalized
    # another source. This is rarely the case.
    f.update(roi.get_ellipse())

    return d


def gtlike_upper_limit(like, name, cl, emin=None, emax=None, 
                       flux_units='erg', **kwargs):

    print 'Calculating gtlike upper limit'

    saved_state = LikelihoodState(like)
    source = like.logLike.getSource(name)

    try:
        import IntegralUpperLimit

        if emin is None and emax is None: 
            emin, emax = get_full_energy_range(like)

        # First, freeze all parameters in model (helps with convergence)
        for i in range(len(like.model.params)):
            like.freeze(i)

        like.thaw(like.par_index(name, 'Prefactor'))

        like.syncSrcParams(name)

        flux_ul, results = IntegralUpperLimit.calc_int(like, name, 
                                                       freeze_all=True,
                                                       cl=cl,
                                                       emin=emin, 
                                                       emax=emax, 
                                                       **kwargs)

        prefactor=like[like.par_index(name, 'Prefactor')]
        pref_ul = results['ul_value']*prefactor.getScale()
        prefactor.setTrueValue(pref_ul)

        flux_ul = like.flux(name,emin,emax)
        flux_units_string = 'ph/cm^2/s'

        eflux_ul = units.convert(like.energyFlux(name,emin,emax), 'MeV', flux_units)
        eflux_units_string = '%s/cm^2/s' % flux_units

        ul = dict(
            emin=emin, emax=emax,
            flux_units=flux_units_string, flux=flux_ul, 
            eflux_units=eflux_units_string, eflux=eflux_ul)

    except Exception, ex:
        print 'ERROR gtlike upper limit: ', ex
        traceback.print_exc(file=sys.stdout)
        ul = None
    finally:
        saved_state.restore()

    return tolist(ul)


def gtlike_powerlaw_upper_limit(like, name, powerlaw_index, cl, emin=None, emax=None, 
                                flux_units='erg',
                                **kwargs):
    """ Wrap up calculating the flux upper limit for a powerlaw
        source.  This function employes the pyLikelihood function
        IntegralUpperLimit to calculate a Bayesian upper limit.

        The primary benefit of this function is that it replaces the
        spectral model automatically with a PowerLaw spectral model
        and fixes the index to -2. It then picks a better scale for the
        powerlaw and gives the upper limit calculation a more reasonable
        starting value, which helps the convergence.
    """
    print 'Calculating gtlike power-law upper limit'

    saved_state = LikelihoodState(like)
    source = like.logLike.getSource(name)
    old_spectrum = source.spectrum()

    if emin is None and emax is None: 
        emin, emax = get_full_energy_range(like)

    e = np.sqrt(emin*emax)

    # assume a canonical dnde=1e-11 at 1GeV index 2 starting value
    dnde = PowerLaw(norm=1e-11, index=2,e_scale=1e3)

    like.setSpectrum(name,'PowerLaw')

    # fix index to 0
    index=like[like.par_index(name, 'Index')]
    index.setTrueValue(-1*powerlaw_index)

    # good starting guess for source
    prefactor=like[like.par_index(name, 'Prefactor')]
    prefactor.setScale(dnde(e))
    prefactor.setValue(1)
    # unbound the prefactor since the default range 1e-2 to 1e2 may not be big enough
    # in small phase ranges.
    prefactor.setBounds(1e-10,1e10)

    scale=like[like.par_index(name, 'Scale')]
    scale.setScale(1)
    scale.setValue(e)

    like.syncSrcParams(name)

    results = gtlike_upper_limit(like, name, cl, emin, emax, flux_units, **kwargs)
    results['powerlaw_index']=powerlaw_index

    like.setSpectrum(name,old_spectrum)
    saved_state.restore()

    return results

def pointlike_upper_limit(roi, name, cl, emin=None, emax=None, flux_units='erg', **kwargs):

    if emin is None and emax is None:
        emin, emax = get_full_energy_range(roi)

    try:
        flux_ul = roi.upper_limit(which=name, confidence=cl, emin=emin, emax=emax, **kwargs)

        flux_units_string = 'ph/cm^2/s'

        ul = dict(
            emin=emin, emax=emax,
            flux_units=flux_units_string, 
            flux=flux_ul)

    except Exception, ex:
        print 'ERROR pointlike upper limit: ', ex
        traceback.print_exc(file=sys.stdout)
        ul = None

    return tolist(ul)


def pointlike_powerlaw_upper_limit(roi, name, powerlaw_index, cl, emin=None, emax=None, 
                                   flux_units='erg', **kwargs):
    print 'Calculating pointlike upper limit'

    saved_state = PointlikeState(roi)

    """ Note keep old flux, because it is important to have
        the spectral model pushed into the upper_limit
        code reasonably close to the best fit flux. This
        is because initial likelihood (ll_0) is used to scale
        the likelihood so it has to be reasonably close to 
        the best value. """
    roi.modify(which=name, model=PowerLaw(index=powerlaw_index), keep_old_flux=True)

    ul = pointlike_upper_limit(roi, name, cl, emin, emax, flux_units, **kwargs)
    ul['powerlaw_index']=powerlaw_index

    saved_state.restore()

    return ul


def pointlike_test_cutoff(roi, which, flux_units='erg'):
    print 'Testing cutoff in pointlike'
    emin,emax=get_full_energy_range(roi)
    d = {}

    saved_state = PointlikeState(roi)

    print 'these are probably not good startin values!'
    old_flux = roi.get_model(which).i_flux(emin,emax)
    m=PowerLaw(norm=1e-11, index=2, e0=np.sqrt(emin*emax))
    m.set_flux(old_flux,emin,emax)
    roi.modify(which=which, model=m,keep_old_flux=False)

    fit = lambda: roi.fit(estimate_errors=False)
    ll = lambda: -1*roi.logLikelihood(roi.parameters())
    def ts():
        old_quiet = roi.quiet; roi.quiet=True
        ts = roi.TS(which,quick=False)
        roi.quiet = old_quiet
        return ts

    spectrum = lambda: spectrum_to_dict(roi.get_model(which), errors=True)

    fit()
    d['ll_0'] = ll_0 = ll()
    d['TS_0'] = ts()
    d['model_0']=spectrum()
    d['flux_0']=pointlike_flux_dict(roi,which,emin,emax,flux_units)

    m=ExpCutoff(n0=1e-11, gamma=1, cutoff=1000, e0=1000)
    m.set_flux(old_flux,emin,emax)
    roi.modify(which=which, 
               model=m,keep_old_flux=False)

    fit()
    d['ll_1'] = ll_1 = ll()
    d['TS_1'] = ts()
    d['model_1']=spectrum()
    d['flux_1']=pointlike_flux_dict(roi,which,emin,emax,flux_units)

    d['TS_cutoff']=2*(ll_1-ll_0)

    saved_state.restore()

    return d

def gtlike_test_cutoff(like, name, flux_units='erg'):
    print 'Testing cutoff in gtlike'

    saved_state = LikelihoodState(like)
    source = like.logLike.getSource(name)
    old_spectrum = source.spectrum()

    d = {}

    try:
        emin, emax = get_full_energy_range(like)

        def fix(parname,value):
            par=like[like.par_index(name, parname)]
            par.setScale(1)
            par.setBounds(-1e100,1e100) # kind of lame, but i think this is necessary
            par.setTrueValue(value)
            par.setBounds(value,value)
            par.setFree(0)
            like.syncSrcParams(name)

        def set(parname,value,scale,lower,upper):
            """ Note, lower + upper are fractional limits if free=True. """
            par=like[like.par_index(name, parname)]
            par.setBounds(-1e100,1e100) # kind of lame, but i think this is necessary
            par.setScale(scale)
            par.setTrueValue(value)
            par.setBounds(lower,upper)
            par.setFree(1)
            like.syncSrcParams(name)

        def get_flux():
            return like.flux(name, emin, emax)

        def set_flux(flux):
            current_flux = get_flux()
            prefactor=like[like.par_index(name, 'Prefactor')]
            prefactor.setTrueValue(
                (flux/current_flux)*prefactor.getTrueValue())
            like.syncSrcParams(name)

        ll = lambda: like.logLike.value()
        ts = lambda: like.Ts(name,reoptimize=True)

        def spectrum():
            source = like.logLike.getSource(name)
            s=source.spectrum()
            return spectrum_to_dict(s, errors=True)

        old_flux = get_flux()

        like.setSpectrum(name,'PowerLaw')
        fix('Scale', np.sqrt(emin*emax))
        set('Prefactor',1e-11,1e-11, 1e-5, 1e5)
        set('Index',       -2,    1,   -5,   5)
        set_flux(old_flux)

        paranoid_gtlike_fit(like)
        d['ll_0'] = ll_0 = ll()
        d['TS_0'] = ts()
        d['model_0']=spectrum()
        d['flux_0']=gtlike_flux_dict(like,name,emin,emax,flux_units)
        
        like.setSpectrum(name,'PLSuperExpCutoff')
        set('Prefactor', 1e-9,  1e-11,   1e-5,1e5)
        set('Index1',      -1,      1,     -5,  5)
        fix('Scale',     1000)
        set('Cutoff',    1000,      1,    1e2,1e8)
        fix('Index2',       1)
        set_flux(old_flux)

        paranoid_gtlike_fit(like)

        if ll() < ll_0:
            # if fit is worse than PowerLaw fit, then
            # restart fit with parameters almost
            # equal to best fit powerlaw
            m = d['model_0']
            set('Prefactor', m['Prefactor'],  1e-11,   1e-5,1e5)
            set('Index1',        m['Index'],      1,     -5,  5)
            fix('Scale',         m['Scale'])
            set('Cutoff',               1e6,      1,    1e2,1e8)
            fix('Index2',                 1)
            paranoid_gtlike_fit(like)

        d['ll_1'] = ll_1 = ll()
        d['TS_1'] = ts()
        d['model_1']=spectrum()
        d['flux_1']=gtlike_flux_dict(like,name,emin,emax,flux_units)

        d['TS_cutoff']=2*(ll_1-ll_0)
    except Exception, ex:
        print 'ERROR gtlike test cutoff: ', ex
        traceback.print_exc(file=sys.stdout)
        d=-1
    finally:
        like.setSpectrum(name,old_spectrum)
        saved_state.restore()

    return tolist(d)

def pointlike_plot_all_seds(roi, filename=None, ncols=4, **kwargs):
    """ Create an SED of all sources in the ROI as a big plot. """
    
    sources=roi.get_sources()
    nrows = int(ceil(float(len(sources))/ncols))
    
    fig = P.figure(figsize=(2.5*ncols,2*nrows),frameon=False)
    tit=P.title("All seds of the sources included in the region.\nRed : fitted sources\nBlue : non fitted sources inside the counts map\nBlack : sources outside of the counts map")

    tit.axes.get_xaxis().set_visible(False)
    tit.axes.get_yaxis().set_visible(False)
    grid = AxesGrid(fig, 111,
                    aspect=False,
                    nrows_ncols = (nrows, ncols),
                    axes_pad = 0.1,
                    add_all=True,
                    label_mode = "L")


    from celgal import dist
    from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
    use_ergs=True
    energy_flux_unit = None
    if energy_flux_unit is None:
        energy_flux_unit = 'erg' if use_ergs else 'MeV'
    assert energy_flux_unit in ('erg', 'MeV', 'GeV', 'eV') , 'unrecognized energy flux unit'
    energy_flux_factor = dict(erg=1.602e-6, MeV=1, eV=1e6, GeV=1e-3)[energy_flux_unit]
    dir=["bottom","top","left","right"]
    for i,which in enumerate(sources):
        source=roi.get_source(which=which)
        distance=dist([source.skydir.ra(),source.skydir.dec()],[roi.sa.roi_dir.ra(),roi.sa.roi_dir.dec()])
        axis = (80, 5e5, 1e-7*energy_flux_factor,3.0e-4*energy_flux_factor)
        axes=grid[i]
        if distance<float(roi.sa.maxROI):
            if len(source.model.get_parameters())!=0:
                for axem in dir:
                    axes.spines[axem].set_color('red')
            else :
                for axem in dir:
                    axes.spines[axem].set_color('blue')
        else :
            for axem in dir:
                axes.spines[axem].set_color('black')
        at = AnchoredText("%s"%which.name,
                          prop=dict(size=8), frameon=True,
                          loc=2,
                          )
        at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
        axes.add_artist(at)
                                
            
        roi.plot_sed(which,axes=grid[i],axis=axis,title=which.name,energy_flux_unit=energy_flux_unit,**kwargs)
        
    if filename is not None: P.savefig(filename)
    

plot_all_seds = pointlike_plot_all_seds # for now
                                                                

def fit_only_prefactor(model):
    model=model.copy()
    model.free[0] = False
    model.free[1:] = False
    return model

def freeze_insignificant_to_catalog(roi,catalog,exclude_names=[], min_ts=25):
    """ Replace all insigificant 2FGL catalog sources
        with the predictions of 2FGL and 
        the spectral shape of the source frozen. """
    any_changed=False
    for source in roi.get_sources():

        if source.name in exclude_names: continue

        if np.any(source.model.free) and roi.TS(which=source)< min_ts:
            try:
                catalog_source = catalog.get_source(source.name)
            except StopIteration:
                pass
            else:
                model=fit_only_prefactor(catalog_source.model)
                print 'Freezing spectra of %s to 2FGL prediction b/c it is insignificant' % source.name
                any_changed=True
                roi.modify(which=source, model=model,keep_old_flux=False)
    return any_changed

def freeze_bad_index_to_catalog(roi,catalog,exclude_names=[], min_ts=25):
    """ Fix the spectrum of all power-law catalog sources with a bad spectral
        index to the predictions from the catalog
        with the predictions of 2FGL and 
        the spectral shape of the source frozen. """
    any_changed=False
    for source in roi.get_sources():

        if source.name in exclude_names: continue

        if isinstance(source.model,PowerLaw):
            index =source.model['index']
            if index < -5 or index > 5:
                try:
                    catalog_source = catalog.get_source(source.name)
                except StopIteration:
                    pass
                else:
                    model=fit_only_prefactor(catalog_source.model)
                    print 'Freezing spectra of %s to 2FGL prediction b/c fit index is bad' % source.name
                    any_changed=True
                    roi.modify(which=source, model=model,keep_old_flux=False)
    return any_changed

def fix_bad_cutoffs(roi, exclude_names):
    """ Loop over all sources. When ExpCutoff souce has cutoff>10TeV, convert to powerlaw. """
    any_changed=False
    for source in roi.get_sources():
        if source.name in exclude_names: continue

        model = source.model

        if np.any(model.free) and isinstance(model,ExpCutoff) and model['cutoff'] > 1e7:
            print 'Converting cutoff source %s to powerlaw because cutoff too high' % source.name
            new_model = PowerLaw(norm=model['norm'], index=model['index'], e0=model.e0)

            any_changed = True
            roi.modify(which=source, model=new_model, keep_old_flux=False)
    return any_changed

def fit_prefactor(roi, which, *args, **kwargs):
    """ Fit the prefactor of source 'which'
        without varying any other parmters.
        
        Can help if one source has a very bad 
        starting value. """
    source = roi.get_source(which)
    model = roi.get_model(which)
    name = source.name

    frozen_sources = dict()
    for other_source in roi.psm.point_sources.tolist() + roi.dsm.diffuse_sources.tolist():
        other_model = roi.get_model(other_source)
        if np.any(other_model.free) and other_source.name != name:
            frozen_sources[other_source.name]=other_model.free.copy()
            roi.modify(which=other_source,free=False)

    old_free = model.free.copy()
    new_free = np.zeros_like(model.free).astype(bool)
    new_free[0] = True
    roi.modify(which=which, free=new_free)

    roi.fit(*args, **kwargs)

    roi.modify(which=which, free=old_free)

    for other_name,other_free in frozen_sources.items():
        roi.modify(which=other_name,free=other_free)

def force_gradient(use_gradient):
    """ A kludge to force use_gradient everywhere! """
    from uw.like.roi_analysis import ROIAnalysis
    from lande_decorators import modify_defaults
    ROIAnalysis.fit=modify_defaults(use_gradient=use_gradient)(ROIAnalysis.fit)



def spectrum_to_dict(*args, **kwargs):
    return gtlike_or_pointlike(SED.spectrum_to_dict, pointlike_spectrum_to_dict, *args, **kwargs)

def get_full_energy_range(*args, **kwargs):
    return gtlike_or_pointlike(gtlike_get_full_energy_range, pointlike_get_full_energy_range, *args, **kwargs)

def flux_dict(*args, **kwargs):
    return gtlike_or_pointlike(gtlike_flux_dict, pointlike_flux_dict, *args, **kwargs)

def sourcedict(*args, **kwargs):
    return gtlike_or_pointlike(gtlike_sourcedict, pointlike_sourcedict, *args, **kwargs)

def powerlaw_upper_limit(*args, **kwargs):
    return gtlike_or_pointlike(gtlike_powerlaw_upper_limit, pointlike_powerlaw_upper_limit, *args, **kwargs)

def upper_limit(*args, **kwargs):
    return gtlike_or_pointlike(gtlike_upper_limit, pointlike_upper_limit, *args, **kwargs)

def test_cutoff(*args, **kwargs):
    return gtlike_or_pointlike(gtlike_test_cutoff, pointlike_test_cutoff, *args, **kwargs)

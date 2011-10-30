""" This file contains various function which I have found useful. """
import pprint
from math import ceil

import pylab as P
import numpy as np
import pyfits as pf

from mpl_toolkits.axes_grid1 import AxesGrid

from uw.like.roi_analysis import ROIAnalysis
from uw.like.roi_extended import ExtendedSource
from uw.like.Models import Model,PowerLaw,ExpCutoff,DefaultModelValues
from uw.like.roi_state import PointlikeState

from toolbag import tolist
from SED import SED
from LikelihoodState import LikelihoodState

def paranoid_gtlike_fit(like, covar=True):
    """ Perform a sepctral fit in gtlike in
        a paranoid manner. """
    saved_state = LikelihoodState(like)
    try:
        print 'First, fitting with minuit'
        like.fit(optimizer="MINUIT",covar=covar)
    except Exception, ex:
        print 'Minuit fit failed with optimizer=MINUIT, Try again with DRMNFB + NEWMINUIT!', ex
        # See here for description of method.
        #   http://fermi.gsfc.nasa.gov/ssc/data/analysis/documentation/Cicerone/Cicerone_Likelihood/Fitting_Models.html
        saved_state.restore()

        try:
            print 'Refitting, first with DRMNFB'
            like.fit(optimizer='DRMNFB', covar=False)
            print 'Refitting, second with NEWMINUIT'
            like.fit(optimizer='NEWMINUIT', covar=covar)
        except Exception, ex:
            print 'ERROR spectral fitting with DRMNFB + NEWMINUIT: ', ex


def pointlike_spectrum_to_dict(model):

    d = dict(name = model.name)
    default = DefaultModelValues.simple_models[model.name]
    for k,v in default.items():
        if k == '_p': continue
        elif k == 'param_names': 
            for p in v: d[p]=model[p]
        else: 
            d[k]=getattr(model,k)

    return tolist(d)

def gtlike_spectrum_to_dict(spectrum):
    from pyLikelihood import ParameterVector
    parameters=ParameterVector()
    spectrum.getParams(parameters)

    d = dict(name = spectrum.genericName())

    for p in parameters:
        d[p.getName()]= p.getTrueValue()
    return tolist(d)


def spectrum_to_dict(spectrum_or_model):
    from pyLikelihood import Function
    if isinstance(spectrum_or_model, Function):
        f=gtlike_spectrum_to_dict
    elif isinstance(spectrum_or_model, Model):
        f=pointlike_spectrum_to_dict
    else:
        raise Exception("like_or_roi must be of type BinnedAnalysis or ROIAnalysis")
    return f(spectrum_or_model)


def gtlike_sourcedict(like, name, emin=None, emax=None, flux_units='erg'):
    from pyLikelihood import ParameterVector

    if emin is None and emax is None:
        emin = like.energies[0]
        emax = like.energies[-1]

    d=dict(
        TS=like.Ts(name,reoptimize=True),
        logLikelihood=like.logLike.value()
    )

    ce=lambda e: SED.energy_from_MeV(e, flux_units)
    d['flux']=f={}
    f['flux']=like.flux(name,emin=emin,emax=emax)
    f['eflux']=ce(like.energyFlux(name,emin=emin,emax=emax))
    f['flux_units']=SED.flux_units_string()
    f['eflux_units']=SED.eflux_units_string(flux_units)
    f['emin'],f['emax']=emin,emax

    try:
        # incase the errors were not calculated
        d['flux_err']=like.fluxError(name,emin=emin,emax=emax)
        d['eflux_err']=ce(like.energyFluxError(name,emin=emin,emax=emax))
    except Exception, ex:
        print 'ERROR calculating flux error: ', ex
        d['flux_err']=-1
        d['eflux_err']=-1

    source = like.logLike.getSource(name)
    spectrum = source.spectrum()

    d['model']=spectrum_to_dict(spectrum)

    parameters=ParameterVector()
    spectrum.getParams(parameters)
    for p in parameters:
        d['model'][p.getName()+'_err']=np.abs(p.error()*p.getScale())

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


def pointlike_sourcedict(roi, name, emin, emax, flux_units='erg'):
    d={}

    if emin is None and emax is None:
        emin = roi.bin_edges[0]
        emax = roi.bin_edges[-1]

    source=roi.get_source(name)

    model=source.model

    old_quiet = roi.quiet; roi.quiet=True
    d['TS'] = roi.TS(name,quick=False)
    roi.quiet = old_quiet

    d['logLikelihood']=-roi.logLikelihood(roi.parameters())

    ce=lambda e: SED.energy_from_MeV(e, flux_units)
    d['flux']=f={}
    f['flux'],f['flux_err']=model.i_flux(emin=emin,emax=emax,error=True)
    ef,ef_err=model.i_flux(emin=emin,emax=emax,e_weight=1,error=True)
    f['eflux'],f['eflux_err']=ce(ef),ce(ef_err)
    f['flux_units']=SED.flux_units_string()
    f['eflux_units']=SED.eflux_units_string(flux_units)
    f['emin'],f['emax']=emin,emax

    d['model']=spectrum_to_dict(model)
    for param in model.param_names:
        d['model'][param + '_err']=model.error(param)

    # Source position
    d['gal'] = [source.skydir.l(),source.skydir.b()]
    d['equ'] = [source.skydir.ra(),source.skydir.dec()]

    if isinstance(source,ExtendedSource):
        # Extended Source parameters
        spatial_model = source.spatial_model
        for param in spatial_model.param_names:
            d[param]=spatial_model[param]
            d[param + '_err']=spatial_model.error(param)

    # add elliptical error, if they exist.
    # N.B. If no localization performed, this will return
    # an empty dictionary.
    # N.B. This method will do the wrong thing if you have recently relocalized
    # another source. This is rarely the case.
    d.update(roi.get_ellipse())
    return d


def sourcedict(like_or_roi, name, emin=None, emax=None):

    from BinnedAnalysis import BinnedAnalysis

    if isinstance(like_or_roi,BinnedAnalysis):
        f = gtlike_sourcedict
    elif isinstance(like_or_roi,ROIAnalysis):
        f = pointlike_sourcedict
    else:
        raise Exception("like_or_roi must be of type BinnedAnalysis or ROIAnalysis")

    return tolist(f(like_or_roi, name, emin, emax))


def gtlike_powerlaw_upper_limit(like,name, powerlaw_index, cl, emin=None, emax=None, 
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
    print 'Calculating gtlike upper limit'

    import IntegralUpperLimit

    if emin is None and emax is None: 
        emin = like.energies[0]
        emax = like.energies[-1]

    e = np.sqrt(emin*emax)

    saved_state = LikelihoodState(like)

    # First, freeze all parameters in model (helps with convergence)
    for i in range(len(like.model.params)):
        like.freeze(i)

    source = like.logLike.getSource(name)
    old_spectrum = source.spectrum()

    # assume a canonical dnde=1e-11 at 1GeV index 2 starting value
    dnde = PowerLaw(norm=1e-11, index=2,e_scale=1e3)

    like.setSpectrum(name,'PowerLaw')

    # fix index to 0
    index=like[like.par_index(name, 'Index')]
    index.setTrueValue(-1*powerlaw_index)
    index.setFree(0)

    # good starting guess for source
    prefactor=like[like.par_index(name, 'Prefactor')]
    prefactor.setScale(dnde(e))
    prefactor.setValue(1)
    # unbound the prefactor since the default range 1e-2 to 1e2 may not be big enough
    # in small phase ranges.
    prefactor.setBounds(0,1e10)

    scale=like[like.par_index(name, 'Scale')]
    scale.setScale(1)
    scale.setValue(e)

    like.syncSrcParams(name)

    flux_ul, results = IntegralUpperLimit.calc_int(like, name, 
                                                          skip_global_opt=True,
                                                          freeze_all=True,
                                                          cl=cl,
                                                          emin=emin, 
                                                          emax=emax, 
                                                          **kwargs)

    prefactor=like[like.par_index(name, 'Prefactor')]
    pref_ul = results['ul_value']*prefactor.getScale()
    prefactor.setTrueValue(pref_ul)

    flux_ul = like.flux(name,emin,emax)
    flux_units_string = SED.flux_units_string()

    eflux_ul = SED.energy_from_MeV(like.energyFlux(name,emin,emax), flux_units)
    eflux_units_string = SED.eflux_units_string(flux_units)

    ul = dict(
        emin=emin, emax=emax,
        flux_units=flux_units_string, flux=flux_ul, 
        eflux_units=eflux_units_string, eflux=eflux_ul)

    like.setSpectrum(name,old_spectrum)
    saved_state.restore()
    return tolist(ul)

def pointlike_powerlaw_upper_limit(roi, name, powerlaw_index, cl, emin, emax, **kwargs):
    print 'Calculating pointlike upper limit'

    saved_state = PointlikeState(roi)

    roi.modify(which=name, model=PowerLaw(index=powerlaw_index))

    if emin is None and emax is None: 
        emin = roi.bin_edges[0]
        emax = roi.bin_edges[-1]

    ul = roi.upper_limit(which=name, confidence=cl, emin=emin, emax=emax, **kwargs)
    saved_state.restore()

    return ul

def powerlaw_upper_limit(like_or_roi, name, powerlaw_index=2, cl=0.95, **kwargs):
    from BinnedAnalysis import BinnedAnalysis
    if isinstance(like_or_roi, BinnedAnalysis):
        f=gtlike_powerlaw_upper_limit
    elif isinstance(like_or_roi, ROIAnalysis):
        f=pointlike_powerlaw_upper_limit
    else:
        raise Exception("like_or_roi must be of type BinnedAnalysis or ROIAnalysis")
    return f(like_or_roi, name, powerlaw_index, cl, **kwargs)



def pointlike_test_cutoff(roi, which):
    print 'Testing cutoff in pointlike'
    d = {}

    saved_state = PointlikeState(roi)

    print 'these are probably not good startin values!'
    emin,emax=roi.bin_edges[0],roi.bin_edges[-1]
    old_flux = roi.get_model(which).i_flux(emin,emax)
    m=PowerLaw(norm=1e-11, index=2, e0=1e3)
    m.set_flux(old_flux,emin,emax)
    roi.modify(which=which, model=m,keep_old_flux=False)

    fit = lambda: roi.fit(estimate_errors=False)
    ll = lambda: -1*roi.logLikelihood(roi.parameters())
    def ts():
        old_quiet = roi.quiet; roi.quiet=True
        ts = roi.TS(which,quick=False)
        roi.quiet = old_quiet
        return ts

    spectrum = lambda: spectrum_to_dict(roi.get_model(which))

    fit()
    d['ll_0'] = ll_0 = ll()
    d['TS_0'] = ts()
    d['model_0']=spectrum()

    m=ExpCutoff(n0=1e-11, gamma=1, cutoff=1000, e0=1000)
    m.set_flux(old_flux,emin,emax)
    roi.modify(which=which, 
               model=m,keep_old_flux=False)

    fit()
    d['ll_1'] = ll_1 = ll()
    d['TS_1'] = ts()
    d['model_1']=spectrum()

    d['TS_cutoff']=2*(ll_1-ll_0)

    saved_state.restore()

    return d

def gtlike_test_cutoff(like, name):
    print 'Testing cutoff in gtlike'
    d = {}

    saved_state = LikelihoodState(like)

    def fix(parname,value):
        par=like[like.par_index(name, parname)]
        par.setScale(1)
        par.setTrueValue(value)
        par.setBounds(value,value)
        par.setFree(0)
        like.syncSrcParams(name)

    def set(parname,value,scale,lower,upper):
        """ Note, lower + upper are fractional limits if free=True. """
        par=like[like.par_index(name, parname)]
        par.setScale(scale)
        par.setTrueValue(value)
        par.setBounds(lower,upper)
        par.setFree(1)
        like.syncSrcParams(name)

    def get_flux():
        return like.flux(name, like.energies[0],like.energies[1])
    def set_flux(flux):
        current_flux = like.flux(name, like.energies[0],like.energies[1])
        prefactor=like[like.par_index(name, 'Prefactor')]
        prefactor.setTrueValue(
            (flux/current_flux)*prefactor.getTrueValue())
        like.syncSrcParams(name)

    ll = lambda: like.logLike.value()
    ts = lambda: like.Ts(name,reoptimize=True)
    def spectrum():
        source = like.logLike.getSource(name)
        s=source.spectrum()
        return spectrum_to_dict(s)

    source = like.logLike.getSource(name)
    old_flux = get_flux()
    old_spectrum = source.spectrum()

    like.setSpectrum(name,'PowerLaw')
    fix('Scale', 1e3)

    set('Prefactor',1e-11,1e-11,      0,1e10)
    set('Index',       -2,    1,  -1e10,1e10)
    set_flux(old_flux)

    plaw_flux = like.flux(name,like.energies[0],like.energies[-1])

    paranoid_gtlike_fit(like)
    d['ll_0'] = ll_0 = ll()
    d['TS_0'] = ts()
    d['model_0']=spectrum()
    
    like.setSpectrum(name,'PLSuperExpCutoff')
    set('Prefactor', 1e-9,   1e-9,     0,1e10)
    set('Index1',      -1,      1, -1e10,1e10)
    fix('Scale',     1000)
    set('Cutoff',    1000,   1000,     0,1e10)
    fix('Index2',       1)
    set_flux(old_flux)

    paranoid_gtlike_fit(like)
    d['ll_1'] = ll_1 = ll()
    d['TS_1'] = ts()
    d['model_1']=spectrum()

    d['TS_cutoff']=2*(ll_1-ll_0)

    like.setSpectrum(name,old_spectrum)
    saved_state.restore()

    return d

def test_cutoff(like_or_roi, name):
    from BinnedAnalysis import BinnedAnalysis
    if isinstance(like_or_roi, BinnedAnalysis):
        f=gtlike_test_cutoff
    elif isinstance(like_or_roi, ROIAnalysis):
        f=pointlike_test_cutoff
    else:
        raise Exception("like_or_roi must be of type BinnedAnalysis or ROIAnalysis")
    return f(like_or_roi, name)




def pointlike_plot_all_seds(roi, filename=None, ncols=4, **kwargs):
    """ Create an SED of all sources in the ROI as a big plot. """

    sources=roi.get_sources()
    nrows = int(ceil(float(len(sources))/ncols))

    fig = P.figure(figsize=(2.5*ncols,2*nrows))

    grid = AxesGrid(fig, 111, 
                    aspect=False,
                    nrows_ncols = (nrows, ncols),
                    axes_pad = 0.1,
                    add_all=True,
                    label_mode = "L")

    for i,which in enumerate(sources):
        roi.plot_sed(which,axes=grid[i],**kwargs)

    if filename is not None: P.savefig(filename)

plot_all_seds = pointlike_plot_all_seds # for now


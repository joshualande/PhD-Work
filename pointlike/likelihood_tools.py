""" This file contains various function which I have found useful. """
import numpy as np
import pprint
import pyfits as pf
from uw.like.roi_analysis import ROIAnalysis
from uw.like.roi_extended import ExtendedSource
from uw.like.Models import Model,PowerLaw,LogParabola,DefaultModelValues

from toolbag import tolist
from PointlikeState import PointlikeState


from SED import SED
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

def gtlike_spectrum_to_dict(model):
    import pyLikelihood
    parameters=pyLikelihood.ParameterVector()
    spectrum.getParams(parameters)

    d = dict(name = spectrum.genericName())

    for p in parameters:
        d[p.getName()]= p.getTrueValue()
    return tolist(d)


def spectrum_to_dict(model):
    from pyLikelihood import Function
    if isinstance(model, Function):
        f=gtlike_spectrum_to_dict
    elif isinstance(model, Model):
        f=pointlike_spectrum_to_dict
    else:
        raise Exception("like_or_roi must be of type BinnedAnalysis or ROIAnalysis")
    return f(model)


def gtlike_sourcedict(like, name, emin, emax):

    from pyLikelihood import ParameterVector

    d=dict(
        ts=like.Ts(name,reoptimize=True),
        flux=like.flux(name,emin=emin,emax=emax),
        flux_err=like.fluxError(name,emin=emin,emax=emax),
        logLikelihood=like.logLike.value()
    )

    spectralparameters=ParameterVector()
    like.model[name]['Spectrum'].getParams(spectralparameters)
    for p in spectralparameters:
        d[p.getName()]=p.getTrueValue()
        d[p.getName()+'_err']=p.error()*p.getScale()
    return d


def pointlike_sourcedict(roi, name, emin, emax):
    d={}

    source=roi.get_source(name)

    model=source.model

    old_quiet = roi.quiet; roi.quiet=True
    d['TS'] = roi.TS(name,quick=False)
    roi.quiet = old_quiet

    d['logLikelihood']=-roi.logLikelihood(roi.parameters())

    d['flux'],d['flux_err']=model.i_flux(emin=emin,emax=emax,error=True)
    for param in model.param_names:
        d[param]=model[param]
        d[param + '_err']=model.error(param)

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


def sourcedict(like_or_roi, name, emin=100, emax=100000):

    from BinnedAnalysis import BinnedAnalysis

    if isinstance(like_or_roi,BinnedAnalysis):
        f = gtlike_sourcedict
    elif isinstance(like_or_roi,ROIAnalysis):
        f = pointlike_sourcedict
    else:
        raise Exception("like_or_roi must be of type BinnedAnalysis or ROIAnalysis")

    return tolist(f(like_or_roi, name, emin, emax))


def gtlike_powerlaw_upper_limit(like,name, powerlaw_index, cl, emin=None, emax=None, **kwargs):
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

    from LikelihoodState import LikelihoodState
    import IntegralUpperLimit

    if emin is None and emax is None: 
        emin = like.energies[0]
        emax = like.energies[-1]

    e = np.sqrt(emin*emax)

    saved_state = LikelihoodState(like)

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
    prefactor.setBounds(1e-10,1e10)

    scale=like[like.par_index(name, 'Scale')]
    scale.setScale(1)
    scale.setValue(e)

    like.syncSrcParams(name)

    ul_scipy, results_scipy = IntegralUpperLimit.calc_int(like, name, 
                                                          freeze_all=True,
                                                          cl=cl,
                                                          emin=emin, 
                                                          emax=emax, 
                                                          **kwargs)

    like.setSpectrum(name,old_spectrum)
    saved_state.restore()
    return ul_scipy

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
    roi.modify(which=which, model=PowerLaw(norm=1e-11, index=2, e0=1e3))

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

    roi.modify(which=which, 
               model=LogParabola(norm=1e-9, index=1, beta=2, e_break=300))

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
    raise Exception('not ready...')

    saved_state = LikelihoodState(like)

    # go powerlaw fit
    source = like.logLike.getSource(name)

    def set(**kwargs):
        for k,v in kwargs:
            index=like[like.par_index(name, k)]
            index.setScale(v)
            index.setValue(1)
            prefactor.setBounds(1e-10,1e10)

    fit = lambda: like.fit(covar=False)
    ll = lambda: like.logLike.value()
    ts = lambda: Ts(name,reoptimize=True)
    spectrum = lambda: spectrum_to_dict(roi.get_model(which))

    like.setSpectrum(name,'PowerLaw')
    set(Prefactor=1e-11, Index=-2, Scale=1e3)

    fit()
    d['ll_0'] = ll_0 = ll()
    d['TS_0'] = ts()
    d['model_0']=spectrum()
    


    d['model_1']=spectrum_to_string(roi.get_model(which))
    like.setSpectrum(name,'LogParabola')
    set(norm=1e-9, alpha=1, beta=2, Eb=300)

    fit()
    d['ll_1'] = ll_1 = ll()
    d['TS_1'] = ts()
    d['model_1']=spectrum()

    d['TS_cutoff']=2*(ll_1-ll_0)

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



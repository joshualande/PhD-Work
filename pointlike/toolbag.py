""" This file contains various function which I have found useful. """
import numpy as np
import pyfits as pf

def tolist(x):
    """ convenience function that takes in a 
        nested structure of lists and dictionaries
        and converst all

        (a) numpy arrays into python lists
        (b) numpy strings into python scrings.

        which is conveneint for duming a file to yaml.
    """
    if isinstance(x,list):
        return map(tolist,x)
    elif isinstance(x,dict):
        return dict((tolist(k),tolist(v)) for k,v in x.items())
    elif isinstance(x,np.ndarray) or \
            isinstance(x,np.number):
        return x.tolist()
    elif isinstance(x,np.str):
        return str(x)
    else:
        return x

def sourcedict(like_or_roi, name, extra='', emin=100, emax=100000):

    from BinnedAnalysis import BinnedAnalysis
    from pyLikelihood import ParameterVector
    from uw.like.roi_analysis import ROIAnalysis
    from uw.like.roi_extended import ExtendedSource

    d={}

    if isinstance(like_or_roi,BinnedAnalysis):
        like = like_or_roi

        d['ts' + extra] = like.Ts(name,reoptimize=True)
        d['flux' + extra]=like.flux(name,emin=emin,emax=emax)
        d['flux_err' + extra]=like.fluxError(name,emin=emin,emax=emax)
        d['logLikelihood']=like.logLike.value()

        spectralparameters=ParameterVector()
        like.model[name]['Spectrum'].getParams(spectralparameters)
        for p in spectralparameters:
            d[p.getName() + extra]=p.getTrueValue()
            d[p.getName()+'_err' + extra]=p.error()*p.getScale()

    elif isinstance(like_or_roi,ROIAnalysis):
        roi=like_or_roi

        source=roi.get_source(name)

        model=source.model

        old_quiet = roi.quiet; roi.quiet=True
        d['ts' + extra] = roi.TS(name,quick=False)
        roi.quiet = old_quiet

        d['logLikelihood']=-roi.logLikelihood(roi.parameters())

        d['flux' + extra],d['flux_err' + extra]=model.i_flux(emin=emin,emax=emax,error=True)
        for param in model.param_names:
            d[param + extra]=model[param]
            d[param + '_err' + extra]=model.error(param)

        # Source position
        d['gal'] = [source.skydir.l(),source.skydir.b()]
        d['equ'] = [source.skydir.ra(),source.skydir.dec()]

        if isinstance(source,ExtendedSource):
            # Extended Source parameters
            spatial_model = source.spatial_model
            for param in spatial_model.param_names:
                d[param + extra]=spatial_model[param]
                d[param + '_err' + extra]=spatial_model.error(param)

        # add elliptical error, if they exist.
        # N.B. If no localization performed, this will return
        # an empty dictionary.
        # N.B. This method will do the wrong thing if you have recently relocalized
        # another source. This is rarely the case.
        d.update(roi.get_ellipse())


    else:
        raise Exception("like_or_roi must be of type BinnedAnalysis or ROIAnalysis")

    return tolist(d) # convert to floats 


def mixed_linear(min,max,num):
    """ Just like np.linspace but the numbers are mixed up
        using the Van der Corput sequence. Handy for getting
        a reasonable sample quickly.
        
        Use the http://en.wikipedia.org/wiki/Van_der_Corput_sequence
        to mix up the numbers. """
    from csc import util
    x=util.sampling_sequence(min,max)
    return np.asarray([x.next() for i in range(num)])

def mixed_log(min,max,num):
    return 10**mixed_linear(np.log10(min),np.log10(max),num)


def powerlaw_upper_limit(like,name, powerlaw_index=-2, **kwargs):
    """ Wrap up calculating the flux upper limit for a powerlaw
        source.  This function employes the pyLikelihood function
        IntegralUpperLimit to calculate a Bayesian upper limit.

        The primary benefit of this function is that it replaces the
        spectral model automatically with a PowerLaw spectral model
        and fixes the index to -2. It then picks a better scale for the
        powerlaw and gives the upper limit calculation a more reasonable
        starting value, which helps the convergence.
    """
    from LikelihoodState import LikelihoodState
    import IntegralUpperLimit

    emin = like.energies[0]
    emax = like.energies[-1]
    e = np.sqrt(emin*emax)

    saved_state = LikelihoodState(like)

    source = like.logLike.getSource(name)
    old_spectrum = source.spectrum()

    # assume a canonical dnde=1e-11 at 1GeV index 2 starting value
    dnde = lambda e: 1e-11*(e/1e3)**-2

    like.setSpectrum(name,'PowerLaw')

    # fix index to 0
    index=like[like.par_index(name, 'Index')]
    index.setTrueValue(powerlaw_index)
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
                                                          emin=emin, 
                                                          emax=emax, 
                                                          **kwargs)

    like.setSpectrum(name,old_spectrum)
    saved_state.restore()
    return ul_scipy

def expand_fits(pf,factor,hdu=0):
    """ Create a new fits file where
        each pixel is divided into factor**2
        more pixels all of equal value. 
        
        I am not an expert on Fits files and
        I only think this code works. Also,
        I have no idea if it would work with 3D data (?).
        As a rule of thumb, if you use this function,
        you should probably open the before/after
        in ds9 and blink them for a while to convince
        yourself the function worked.
    """

    h=pf[hdu].header
    d=pf[hdu].data

    h['CDELT1']/=factor
    h['CDELT2']/=factor

    h['NAXIS1']*=factor
    h['NAXIS2']*=factor

    h['CRPIX1']=h['CRPIX1']*factor - factor/2.0 + 0.5
    h['CRPIX2']=h['CRPIX2']*factor - factor/2.0 + 0.5

    larger=list(d.shape)
    larger[0]*=factor
    larger[1]*=factor
    #larger_array = np.empty(larger,dtype=d.dtype)
    larger_array = np.zeros(larger,dtype=d.dtype)
    for i in range(factor):
        for j in range(factor):
            larger_array[i::factor,j::factor] = d

    pf[hdu].data=larger_array



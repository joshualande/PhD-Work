""" This file contains various function which I have found useful. """
import numpy as np
import pyfits as pf
from uw.like.roi_analysis import ROIAnalysis
from uw.like.roi_extended import ExtendedSource
from uw.pulsar.phase_range import PhaseRange

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
    elif isinstance(x,PhaseRange):
        return x.tolist(dense=True)
    else:
        return x



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

def pointlike_powerlaw_upper_limit(roi, name, powerlaw_index, cl, **kwargs):
    old_model = roi.get_model(name).copy()
    roi.modify(which=name, model=PowerLaw(index=powerlaw_index))


    if emin is None and emax is None: 
        emin = roi.bin_edges[0]
        emax = roi.bin_edges[-1]

    ul = roi.upper_limit(which=name, confidence=cl, emin=emin, emax=emax, **kwargs)
    roi.modify(which=name, model=old_model)
    return ul

def powerlaw_upper_limit(like_or_roi, name, powerlaw_index=2, cl=0.95, **kwargs):
    from BinnedAnalysis import BinnedAnalysis
    if isinstance(like_or_roi, ROIAnalysis):
        f=gtlike_powerlaw_upper_limit
    elif isinstance(like_or_roi, ROIAnalysis):
        f=pointlike_powerlaw_upper_limit
    else:
        raise Exception("like_or_roi must be of type BinnedAnalysis or ROIAnalysis")
        return f(like_or_roi, name, powerlaw_index, cl, **kwargs)

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



# Taken form http://stackoverflow.com/questions/4126348/how-do-i-rewrite-this-function-to-implement-ordereddict
import collections
class OrderedDefaultdict(collections.OrderedDict):
    def __init__(self, *args, **kwargs):
        newdefault = None
        newargs = ()
        if len(args):
            newdefault = args[0]
            if not callable(newdefault) and newdefault != None:
                raise TypeError('first argument must be callable or None')
            newargs = args[1:]
        self.default_factory = newdefault
        super(OrderedDefaultdict, self).__init__(*newargs, **kwargs)

    def __missing__ (self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value


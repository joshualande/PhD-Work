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

    d={}

    if isinstance(like_or_roi,BinnedAnalysis):
        like = like_or_roi

        d['ts' + extra] = like.Ts(name,reoptimize=True)
        d['flux' + extra]=like.flux(name,emin=emin,emax=emax)
        d['flux_err' + extra]=like.fluxError(name,emin=emin,emax=emax)

        spectralparameters=ParameterVector()
        like.model[name]['Spectrum'].getParams(spectralparameters)
        for p in spectralparameters:
            d[p.getName() + extra]=p.getTrueValue()
            d[p.getName()+'_err' + extra]=p.error()*p.getScale()

    elif isinstance(like_or_roi,ROIAnalysis):
        roi=like_or_roi

        source=roi.get_source(name)
        model=source.model

        d['ts' + extra] = roi.TS(name,quick=False)
        d['flux' + extra],d['flux_err' + extra]=model.i_flux(emin=emin,emax=emax,error=True)
        for param in model.param_names:
            d[param + extra]=model['index']
            d[param + '_err' + extra]=model.error('index')

    else:
        raise Exception("like_or_roi must be of type BinnedAnalysis or ROIAnalysis")

    return d


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


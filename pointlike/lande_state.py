""" Classes to save the state of fit parameters.
    
    Works like LikelihoodState with the added advantage that
    
    (a) it will change back spectral models that have changed
        This is useful if you are trying out a new spectral model or something

    (b) Allows the parameter like to be passed into restore to
        restore into a new like object.

"""
import pyLikelihood
from LikelihoodState import _Parameter

class LandeState(object):
    def __init__(self, like):
        self.like = like
        self.sources = dict()

        all_names = like.sourceNames()

        for name in all_names:

            spectrum = like[name].src.spectrum()

            parameters=pyLikelihood.ParameterVector()
            spectrum.getParams(parameters)

            type = spectrum.genericName()
            self.sources[name] = dict(type = type, parameters=dict())
            for p in parameters:
                self.sources[name]['parameters'][p.getName()] = _Parameter(p)

    def restore(self, like=None):
        if like is None: like = self.like

        for sname,v in self.sources.items():

            type = v['type']
            parameters = v['parameters']

            like.setSpectrum(sname,type)

            for pname,pcache in parameters.items():
                index = self.like.par_index(sname, pname)
                like_par = self.like.params()[index]
                pcache.setDataMembers(like_par)

        self.like.syncSrcParams()

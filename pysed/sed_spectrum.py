""" Code relateded to defining a base spectrum
    class that can be subclassed.

    Author: Joshua Lande <joshualande@gmail.com>
"""
from abc import abstractmethod
from operator import add

import numpy as np
import pylab as P
import sympy

import sed_units as u

class Spectrum(object):
    """ A base class which represents some
        physical quanity as a function of energy. """

    @staticmethod
    def logspace_unit(emin,emax, npts):
        """ Convenience function to compute
            an array of points between
            emin and emax when emin and emax
            are united and have the same units.
            
            Example:

            >>> Spectrum.logspace_unit(1*u.cm,1e3*u.cm,4)
            [0.01*m, 0.1*m, 1.0*m, 10.0*m]
        """
        # make sure numbers have same units
        val = lambda x: x.as_two_terms()[0]
        unit = lambda x: x.as_two_terms()[1]

        assert(unit(emin)==unit(emax))

        units = unit(emin)
        emin,emax = val(emin), val(emax)

        return u.tosympy(np.logspace(np.log10(float(emin)),
                                     np.log10(float(emax)), npts),units)
                    
    def loglog(self, 
               x_units_string,
               y_units_string,
               emin=None, emax=None, 
               e_weight=0, # weight the function by energy raised to this power
               scale=1, # scale
               npts=1000,
               x_label=None,
               y_label=None,
               filename=None, fignum=None, 
               axes=None, **kwargs):
        """ Plots the energy spectrum. 

            emin and emax be in energy units.
            
            x_units_string and y_units_string must be strings suitable
            for plotting on the matplotlib axes. """

        if axes is None:
            fig = P.figure(fignum,figsize=(5.5,4.5))
            P.clf()
            fig.subplots_adjust(left=0.18,bottom=0.13,right=0.95,top=0.95)
            axes = fig.add_subplot(111)

        if emin is None: emin=self.emin*u.erg
        if emax is None: emax=self.emax*u.erg

        x = Spectrum.logspace_unit(emin,emax,npts)
        y = scale*self(x)
        for i in range(e_weight): y=y.multiply_elementwise(x)

        x=u.tonumpy(x,u.fromstring(x_units_string))
        y=u.tonumpy(y,u.fromstring(y_units_string))

        axes.loglog(x,y, **kwargs)

        if x_label is None: x_label = x_units_string
        if y_label is None: y_label = ('E$^%s$' % e_weight if e_weight>0 else '') + 'dN/dE (%s)' % y_units_string

        axes.set_xlabel(x_label)
        axes.set_ylabel(y_label)

        if filename is not None: P.savefig(filename)
        return axes

    @classmethod                                                                                                                                                            
    def units(cls):                                                                                                                                                         
        """ Returns the units that __call__ is assumed to be in. """                                                                                                        
        return u.fromstring(cls.units_string())                                                                                                                             

    def __call__(self, energy, units=True):
        """ Returns number of particles per unit energy [1/energy]. 
        
            This function vectorized the output if a numpy array
            or Sympy Matix of energies is passed """

        if isinstance(energy,np.ndarray) and units==False:
            if self.vectorized:
                return self.spectrum(energy)
            else:
                return np.asarray([self(i) for i in energy])

        if isinstance(energy,sympy.Matrix) and units==True:
            if self.vectorized:
                energy = u.tonumpy(energy,u.erg)
                return u.tosympy(self.spectrum(energy),self.units())
            else:
                return sympy.Matrix([self(i) for i in energy]).transpose()

        if units: energy = float(energy/u.erg)
        spectrum=self.spectrum(energy)
        return spectrum*(self.units() if units else 1)


class CompositeSpectrum(Spectrum):
    def __init__(*spectra):
        self.spectra == spectra

        def all_same(items): return len(set(items))==1

        if not all_same([s.units_string() for u in self.spectra]):
            raise Exception('Error in CompositeSpectrum: all spectra must have the same units.')
        
        def __call__(self, *args, **kwargs):
            return reduce(add,[s(*args,**kwargs) for s in self.spectra])

        def units_string(self,*args,**kwargs): return self.spectra[0].units_string(*args,**kwargs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()


""" sed_thermal.py

    Author: Joshua Lande <joshualande@gmail.com>
"""
import numpy as np

from sed_spectrum import Spectrum
import sed_units as u

class ThermalSpectrum(Spectrum):

    vectorized = True

    def __init__(self, **kwargs):
        """ A blackbody thermal spectrum
            for a given temperature kT [energy]. 

            Input can be either 'kT' in energy units or
            'T' in temperature units.
            
            This formula is on the top of page 208 in R&L """
        if kwargs.has_key('kT'): self.kT = kwargs.pop('kT')
        elif kwargs.has_key('T'): self.kT = u.boltzmann*kwargs.pop('T')
        else: raise Exception("Either kT or T must be passed into ThermalSpectrum")
        if len(kwargs)>0: raise Exception("Invalid argument(s) to ThermalSpectrum: %s" % str(kwargs))

        self.kT = float(self.kT/u.erg)

        # function is essentially 0 outside of this energy range.
        self.emin=1e-3*self.kT
        self.emax=1e2*self.kT

        self.pref = 8*np.pi/(u.planck**3*u.speed_of_light**3)
        self.pref = float(self.pref/(u.erg**-3*u.cm**-3))

    @staticmethod
    def occupation_number(x):
        """ This is equation 1.49 in R&L. """
        return 1/(np.exp(x)-1)

    def spectrum(self, energy):
        """ Return the energy density in units of 1/energy/Volume."""
        return self.pref*energy**2*self.occupation_number(energy/self.kT)

    @staticmethod                                                                                                                                                           
    def units_string(): return '1/erg/cm^3'

    def integral(self, emin=0*u.erg, emax=np.inf*u.erg, units=True, e_weight=0):

        """ Integrate the thermal spectrum from emin to emax.
            
            Integrand is in units of energy/volume
        
            Implementation note: integrate with energy measured in units of kT

        """
        if units:
            if emin not in [0, -np.inf, np.inf]: emin = float(emin/u.erg)
            if emax not in [0, -np.inf, np.inf]: emax = float(emax/u.erg)

        raise Exception("Fix")
        return self.pref**self.kT**(3+e_weight)*integrate.quad(lambda x: x**(2+e_weight)*self.occupation_number(x), 0, np.inf)[0]

class CMB(ThermalSpectrum):
    def __init__(self): super(CMB,self).__init__(T=2.725*u.kelvin)




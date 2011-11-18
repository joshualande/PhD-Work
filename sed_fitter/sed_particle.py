from sed_spectrum import Spectrum
import numpy as np

import sed_units as u
from sed_integrate import logsimps

class ParticleSpectrum(Spectrum):
    """ This class to represents a spectrum of particles with total energy total_energy. 
    
        __call__ returns dn/de, the number of particles per unit energy (in units of 1/erg)
    """
    per_decade=10

    def __init__(self,total_energy, emin, emax, *args, **kwargs):
        """ Normalize total energy output. """
        self.emin = float(emin/u.erg)
        self.emax = float(emax/u.erg)
        self.norm = 1

        self.init(*args,**kwargs)

        self.norm=float(total_energy/self.integral(units=True, e_weight=1))

    def integral(self, units=True, e_weight=0):
        integral=logsimps(lambda e: e**(e_weight)*self(e, units=False),
                          self.emin,self.emax,per_decade=self.per_decade)
        return integral*(u.erg**(e_weight+1)*self.units() if units else 1)

    @staticmethod                                                                                                                                                           
    def units_string(): return '1/erg'

class PowerLaw(ParticleSpectrum):

    def init(self, index, e_scale=u.GeV):
        self.index = index
        self.e_scale = float(e_scale/u.erg)

    def spectrum(self, energy):
        """ Returns number of particles per unit energy [1/erg]. """
        return self.norm*(energy/self.e_scale)**(-self.index)


class PowerLawCutoff(ParticleSpectrum):

    def init(self, index, e_cutoff, e_scale=u.GeV):

        self.index = index
        self.e_cutoff = float(e_cutoff/u.erg)
        self.e_break = float(e_break/u.erg)
        self.e_scale = float(e_scale/u.erg)

    def spectrum(self, energy):
        """ Returns number of particles per unit energy [1/erg]. """
        return self.norm*(energy/self.e_scale)**(-self.index)*np.exp(-energy/self.e_cutoff)


class SmoothBrokenPowerLaw(ParticleSpectrum):
    """ A smoothed broken power-law particle distribution.

        This formula is taken from the fermi-LAT publication
        on W51C: http://arxiv.org/abs/0910.0908
    """
    def init(self, index1, index2, e_scale, e_break):
        self.index = index
        self.e_cutoff = float(e_cutoff/u.erg)                                                                                                                               
        self.e_break = float(e_break/u.erg)                                                                                                                                 
        self.e_scale = float(e_scale/u.erg)                                                                                                                                 

    def spectrum(self, energy):
        """ Returns number of particles per unit energy [1/erg]. """
        return self.norm*(energy/self.e_scale)**(-self.index1)*(1 + (energy/self.e_break)**beta)*(-(index2-index1)/beta)

class BrokenPowerLawCutoff(ParticleSpectrum):

    def init(self, index1, index2, e_cutoff, e_break):
        self.index1 = index1
        self.index2 = index2
        self.e_cutoff = float(e_cutoff/u.erg)
        self.e_break = float(e_break/u.erg)
        self.e_scale = float(u.eV/u.erg)

    def spectrum(self, energy):
        """ Return number of particles per unit energy [1/erg]. """
        return self.norm*((energy/self.e_scale)**-self.index1)/(1.+(energy/self.e_break)**(-self.index1+self.index2))*np.exp(-energy/self.e_cutoff)


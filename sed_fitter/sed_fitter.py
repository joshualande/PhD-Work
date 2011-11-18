""" sed_fitter.py

    Code to compute SEDs. This code differs from other SED packages in
    valuing human readability over computational efficiency. 


    Notes: 
        * R&L is Rybicki and Lightman "Radiative Processes in Astrophysics


    This file is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Author: Joshua Lande
"""

import math
from abc import abstractmethod

import pylab as P
import numpy as np
from sed_integrate import logsimps
from scipy import integrate
from scipy import special

import sympy

import lande_units as u

class Spectrum(object):
    """ A spectrum is a base class which represents some
        physical quanity as a function of energy. """

    def loglog(self, emin, emax, e_weight=0, npts=1000, x_units='erg', y_units=None, 
               filename=None, fignum=None, axes=None, **kwargs):
        """ Plots the energy spectrum. 

            emin and emax must have sympy units.
            
            x_units and y_units must be strings suitable
            for plotting on the matplotlib axes. """

        if y_units is None: 
            if e_weight>0:
                y_units = '%s^%s*%s' % ('erg',e_weight,self.units_string())
            else:
                y_units = '%s' % self.units_string()

        if axes is None:
            fig = P.figure(fignum,figsize=(5.5,4.5))
            P.clf()
            fig.subplots_adjust(left=0.18,bottom=0.13,right=0.95,top=0.95)
            axes = fig.add_subplot(111)

        x = np.logspace(np.log10(float(emin/u.erg)), np.log10(float(emax/u.erg)), npts)

        # y is in units of self.units()
        y = x**(e_weight)*self(x, units=False)

        x=u.convert(x,u.erg, u.fromstring(x_units))
        y=u.convert(y,u.erg**(e_weight)*self.units(), u.fromstring(y_units))

        axes.loglog(x,y, **kwargs)
        axes.set_xlabel(x_units)
        axes.set_xlim(x[0],x[-1])

        if e_weight > 0:
            axes.set_ylabel(r'E$^%s$ dN/dE (%s)' % (e_weight,y_units))
        else:
            axes.set_ylabel('dN/dE (%s)' % y_units)
        if filename is not None: P.savefig(filename)
        return axes

    @abstractmethod
    def __call__(self, energy): 
        """ Returns dN/dE. Energy must be in erg. """
        pass

    @classmethod                                                                                                                                                            
    def units(cls):                                                                                                                                                         
        """ Returns the units that __call__ is assumed to be in. """                                                                                                        
        return u.fromstring(cls.units_string())                                                                                                                             

    def __call__(self, energy, units=True):
        """ Returns number of particles per unit energy [1/energy]. """
        if units: energy = float(energy/u.erg)
        spectrum=self.spectrum(energy)
        return spectrum*(self.units() if units else 1)



class ParticleSpectrum(Spectrum):
    """ class to represent a spectrum of particles with total energy total_energy. 
    
        __call__ returns dn/de, the number of particles per unit energy (in units of 1/erg)
    """
    per_decade=10


    def integral(self, units=True, e_weight=0):

        integral=logsimps(lambda e: e**(e_weight)*self(e, units=False),self.emin,self.emax,per_decade=self.per_decade)

        return integral*(u.erg**(e_weight+1)*self.units() if units else 1)


    def __init__(self,total_energy, emin, emax, *args, **kwargs):
        """ Normalize total energy output. """
        self.emin = float(emin/u.erg)
        self.emax = float(emax/u.erg)
        self.norm = 1

        self.init(*args,**kwargs)

        self.norm=float(total_energy/self.integral(units=True, e_weight=1))

    @staticmethod                                                                                                                                                           
    def units_string(): return '1/erg'

class PowerLaw(ParticleSpectrum):

    def init(self, index, e_scale=u.GeV):
        self.index = index
        self.e_scale = float(e_scale/u.erg)

    def spectrum(self, energy):
        """ Returns number of particles per unit energy [1/energy]. """
        return self.norm*(energy/self.e_scale)**(-self.index)


class PowerLawCutoff(ParticleSpectrum):

    def init(self, index, e_cutoff, e_scale=u.GeV):

        self.index = index
        self.e_cutoff = float(e_cutoff/u.erg)
        self.e_break = float(e_break/u.erg)
        self.e_scale = float(e_scale/u.erg)

    def spectrum(self, energy):
        """ Returns number of particles per unit energy [1/energy]. """
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
        """ Returns number of particles per unit energy [1/energy]. """
        return self.norm*(energy/self.e_scale)**(-self.index1)*(1 + (energy/self.e_break)**beta)*(-(index2-index1)/beta)

class BrokenPowerLawCutoff(ParticleSpectrum):

    def init(self, index1, index2, e_cutoff, e_break):
        self.index1 = index1
        self.index2 = index2
        self.e_cutoff = float(e_cutoff/u.erg)
        self.e_break = float(e_break/u.erg)
        self.e_scale = float(u.eV/u.erg)

    def spectrum(self, energy):
        """ Return number of particles per unit energy [1/energy]. """
        return self.norm*((energy/self.e_scale)**-self.index1)/(1.+(energy/self.e_break)**(-self.index1+self.index2))*np.exp(-energy/self.e_cutoff)

class ThermalSpectrum(Spectrum):
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

        self.pref = 8*math.pi/(u.planck**3*u.speed_of_light**3)
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




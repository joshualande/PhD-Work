""" sed_fitter.py

    Code to compute SEDs. This code differs
    from other SED packages in valuing readability
    over efficiency. Anything that is supposed
    to be fast should probably be rewritten in c.


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

from math import pow
from abc import abstractmethod

import pylab as P
import numpy as np
from scipy import integrate 
from scipy import special

import lande_units as u


class Spectrum(object):
    """ A spectrum is a base class which represents some
        physical quanity as a function of energy. """

    def loglog(self, emin, emax, e_weight=0, npts=1000, x_units=None, y_units=None, 
               filename=None, fignum=None, axes=None, **kwargs):
        """ Plots the energy spectrum. 

            emin and emax must have sympy units.
            
            x_units and y_units must be strings suitable
            for plotting on the matplotlib axes. """

        if x_units is None: x_units = 'erg'
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

        x = np.logspace(np.log10(float(emin/u.erg)),
                        np.log10(float(emax/u.erg)), npts)

        # y is in units of self.units()
        y = np.asarray(map(self,x))

        x=u.tosympy(x,u.erg)
        y=u.tosympy(y,self.units())
        for i in range(e_weight): 
            y=y.multiply_elementwise(x)

        x = u.tonumpy(x,u.fromstring(x_units))
        y = u.tonumpy(y,u.fromstring(y_units))

        axes.loglog(x,y, **kwargs)
        axes.set_xlabel(x_units)

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

    @staticmethod
    @abstractmethod
    def units_string():
        """ Returns a string of the units of the output. """
        pass

    @classmethod
    def units(cls):
        """ Returns the units that __call__ is assumed to be in. """
        return u.fromstring(cls.units_string())

    def __call__(self,*args,**kwargs): self(*args,**kwargs)


class ParticleSpectrum(Spectrum):
    """ class to represent a spectrum of particles with total energy total_energy. 
    
        __call__ returns dn/de, the number of particles per unit energy (in units of 1/erg)
    """

    def __init__(self,total_energy):
        self.norm = 1

        # Normalize total energy output
        power = integrate.quad(lambda e: e*self(e), 0, np.inf)[0]
        self.norm= float(total_energy/self.energy())

    def energy(self, emin=0*u.erg, emax=np.inf*u.erg):
        integral=integrate.quad(lambda e: e*self(e), float(emin/u.erg), float(emax/u.erg))[0]
        return integral*u.erg**2*self.units()
        
    @staticmethod
    def units_string(): return '1/erg'


class PowerLawCutoff(ParticleSpectrum):

    def __init__(self, total_energy, index, e_cutoff):
        self.index = index
        self.e_cutoff = float(e_cutoff/u.erg)
        self.e_break = float(e_break/u.erg)
        self.e_scale = float(u.GeV/u.erg)
        super(PowerLawCutoff,self).__init__(total_energy)

    def __call__(self, energy):
        return self.norm*(energy/self.e_scale)**(-self.index)*np.exp(-energy/self.e_cutoff)

class SmoothBrokenPowerLaw(ParticleSpectrum):
    """ A smoothed broken power-law particle distribution.

        This formula is taken from the fermi-LAT publication
        on W51C: http://arxiv.org/abs/0910.0908
    """
    def __init__(self, total_energy, index1, index2, e_scale, e_break):
        self.index = index
        self.e_cutoff = float(e_cutoff/u.erg)
        self.e_break = float(e_break/u.erg)
        self.e_scale = float(e_scale/u.erg)
        super(PowerLawCutoff,self).__init__(total_energy)

    def __call__(self, energy):
        return self.norm*(energy/self.e_scale)**(-self.index1)*(1 + (energy/self.e_break)**beta)*(-(index2-index1)/beta)

class BrokenPowerLawCutoff(ParticleSpectrum):

    def __init__(self, total_energy, index1, index2, e_cutoff, e_break):

        self.index1 = index1
        self.index2 = index2
        self.e_cutoff = float(e_cutoff/u.erg)
        self.e_break = float(e_break/u.erg)
        super(BrokenPowerLawCutoff,self).__init__(total_energy)

    def __call__(self, energy):
        """ Return number of particles per unit enert [1/erg]. """
        return self.norm*(energy**-self.index1)/(1.+(energy/self.e_break)**(-self.index1+self.index2))*np.exp(-energy/self.e_cutoff)

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

        self.pref = 8*np.pi/(u.planck**3*u.speed_of_light**3)

    @staticmethod
    def occupation_number(x):
        """ This is equation 1.49 in R&L. """
        return 1/(np.exp(x)-1)

    def __call__(self, energy):
        """ Return the energy density in units of 1/energy/Volume."""
        return self.pref*energy**2*ThermalSpectrum.occupation_number(float(energy/self.kT))

    def integrate(self, emin, emax, e_weight=0):
        """ Integrate the thermal spectrum from emin to emax.
            
            Integrand is in units of energy/volume
        
            Implementation note: integrate after performing
            the change of variables (x = energy/kT)

            # note the E^3 dE -> kT^3 x^2 dx
        """
        xmin,xmax = float(emin/self.kT), float(emax/self.kT)

        return self.pref*self.kT**(3+e_weight)*integrate.quad(lambda x: x**(2+e_weight)**ThermalSpectrum.occupation_number(x), xmin, xmax)[0]

class CMB(ThermalSpectrum):
    def __init__(self): super(CMB,self).__init__(T=2.725*u.kelvin)


class SingleElectronSynchrotron(Spectrum):
    """ Assuming that there is a single electron of energy gamma
        in a magnetic field B, 

        computes the power synchrotron radiation dissipation
        by this electron.

        This treatment follows section 6.2 in R&L and especially  
        the formulas 6.17c, 6.18, and 6.31c
    
        The spectrum is in unit of energy per unit time
        per unit frequency emitted by a single electron.
        """

    """ This is equation 6.31 in R&L. """

    # for some reason, special.kv(5/3,1e10) is NaN, not 0 ???
    # for now, just clip the function above 1e5 to be 0
    @np.vectorize
    def F(x):
        if x>1e5: return 0
        return x*integrate.quad(lambda j: special.kv(5./3,j),x,np.inf)[0]
    
    def __init__(self, electron_energy, magnetic_field):

        gamma = electron_energy/(u.electron_mass*u.speed_of_light**2)
        q = u.electron_charge
        B = magnetic_field
        sin_alpha = 1 # ?
        m = u.electron_mass
        c = u.speed_of_light
        # This is the R&L prefactor (power/unit frequency)
        self.pref = (np.sqrt(3)/(2*np.pi))*(q**3*B*sin_alpha)/(u.electron_mass*c**2)

        # convert to (power/unit energy)
        self.pref /= u.planck
        self.pref = float(self.pref/(u.erg/u.s/u.erg))

        self.omega_c = 3*gamma**2*q*B*sin_alpha/(2*m*c)
        self.omega_c = float(self.omega_c/u.hz)

    @staticmethod
    def units_string(): 
        return '1/s/erg'

    @staticmethod
    def energy_erg_to_angular_frequency_hz(energy_in_erg):
        """ Formula is from http://en.wikipedia.org/wiki/Photon. """
        conversion_factor = float((u.erg/u.planck)/u.hz)
        return energy_in_erg*conversion_factor

    def __call__(self,energy):
        omega = self.energy_erg_to_angular_frequency_hz(energy)
        
        # return photons radiated per unit energy per unit time
        # by a single electron
        return (self.pref/energy)*self.F(omega/self.omega_c)

class Synchrotron(Spectrum):
    """ Calculates the syncrotron radiation
        from an electron spectrum in a magnetic field. """

    def __init__(self, electron_spectrum, magnetic_field):

        self.electron_spectrum = electron_spectrum
        self.magnetic_field = magnetic_field

        print 'not sure what the prefactor should be yet'

    def __call__(self, energy):
        """ Returns number per unit energy dN/dE. """
        photon_energy = energy

        # return total power per unit energy by convolving energy per electron
        # by the electron spectrum.

        def integrand(electron_energy):
            single_electron=SingleElectronSynchrotron(
                electron_energy = electron_energy*u.erg, 
                magnetic_field = self.magnetic_field)

            # return [ph/s/photon energy/electron energy] = 
            #             [ph/s/electron/photon energy]*[number of electrons/electron energy]
            return single_electron(photon_energy)*self.electron_spectrum(electron_energy)

        # integrate [ph/s/photon energy/electron energy] over electron energies
        # Returns the photon flux per unit time per unit photon energy
        return integrate.quad(integrand,0,np.inf)[0]

    @staticmethod
    def units_string():
        return '1/s/erg'


class InverseCompton(Spectrum):

    @staticmethod
    def f(x): 
        """ This is 7.27 in R&L -- from Blumenthal and Gold, 1970. """
        return 2*x*np.log(x) + x + 1 - 2*x**2

    def __init__(self, enenergy_spectrum, photon_spectrum):
        """ The inverse compton radiation an electron spectrum
            and photon spectrum. """
        pass

    def __call__(self, energy):
        photon_energy = energy

        def integrand(electron_energy):
            pass

if __name__ == '__main__':

    # all the code below is for testing out the main code.

    def plot_sed(synch,distance):
        """ Plot the synchotron + inverse compton SED. """

        emin=1e-7*u.eV
        emax=1e15*u.eV

        x = np.logspace(np.log10(float(emin/u.erg)), np.log10(float(emax/u.erg)), 100)

        # y is in units of self.units()
        y = np.asarray(map(synch,x))

        x=u.tosympy(x,u.erg)

        y=u.tosympy(y,synch.units())
        y=y.multiply_elementwise(x).multiply_elementwise(x)
        y /= (4*np.pi*distance**2)

        x_units = u.eV
        y_units = u.eV/u.cm**2/u.s
        x = u.tonumpy(x,x_units)
        y = u.tonumpy(y,y_units)

        fig = P.figure(None,figsize=(5.5,4.5))
        P.clf()
        fig.subplots_adjust(left=0.18,bottom=0.13,right=0.95,top=0.95)
        axes = fig.add_subplot(111)

        axes.loglog(x,y)
        axes.set_xlabel('Energy (eV)')
        axes.set_ylabel(r'E$^2$ dN/dE (eV cm$^{-2}$ s$^{-1}$)')
        axes.set_xlim(float(emin/x_units),float(emax/x_units))
        axes.set_ylim(1e-08,1e-1)

        P.savefig('sed.png')

    def stefan_hess_j1813():
        electron_spectrum = BrokenPowerLawCutoff(
                total_energy = 2e48*u.erg,
                index1 = 2.0,
                index2 = 3.0,
                e_break = 1e7*u.eV,
                e_cutoff = 1.e14*u.eV)

        print 'total energy %s erg' % float(electron_spectrum.energy()/u.erg)
        emin=1e-7*u.eV
        emax=1e15*u.eV

        electron_spectrum.loglog(emin=emin, emax=emax, 
                   e_weight=2, x_units='eV', y_units='eV', 
                   filename='ElectronSpectrum.png')

        syn = SingleElectronSynchrotron(electron_energy=1e3*u.MeV,
                                        magnetic_field=3e-6*u.gauss)

        synch = Synchrotron(electron_spectrum=electron_spectrum,
                          magnetic_field=3e-6*u.gauss)

        plot_sed(synch,distance=4.2*u.kpc)


    stefan_hess_j1813()

    def test_thermal_spectrum():
        cmb=CMB()
        print 'kt=',cmb.kT
        print 'dnde=',cmb(cmb.kT)
        total_energy_density = cmb.integrate(0,np.inf*u.eV, e_weight=1)
        print 'total',total_energy_density
        print total_energy_density/(u.eV*u.m**-3)
        print '%.2e eV/m^3' % float(total_energy_density/(u.eV*u.m**-3))
        print 'cmb = 2.60e5 eV/m^3'

    #test_thermal_spectrum()

    def yasunobu_w51c():

        pass

    """
    def test():
        #electron_spectrum.loglog(emin=1e-6*u.eV, emax=1e16*u.eV, filename='test.png')

        syn = SingleElectronSynchrotron(electron_energy=1*u.eV,
                                        magnetic_field=3e-4*u.gauss)

        print 'bb4',y_units
        syn.loglog(emin=1e-12*u.eV, emax=1e9*u.eV, 
                   x_units='eV', y_units='eV', 
                   filename='Single.png')

        single_electron=SingleElectronSynchrotron(
            electron_energy = 1e3*u.erg, 
            magnetic_field = 3e-4*u.gauss)

        #syn.loglog(emin=u.eV, emax=u.TeV, 
        #           x_units='MeV', y_units='MeV/s/hz', 
        #           filename='Synchrotron.png')


    def plot_f():
        x = np.linspace(0,4,1000)
        y = SingleElectronSynchrotron.F(x)
        P.plot(x,y)
        P.savefig('test.png')
    """

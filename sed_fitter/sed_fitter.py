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
from scipy import integrate 
from scipy import special

import sympy

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

    def __call__(self,*args,**kwargs): self(*args,**kwargs)


def uintegrate(func, xmin, xmax, x_units, y_units, e_weight=0):
    """ Hide the ungliness of not being able to compute
        integrals of functions with units.

        Here, we assume that func takes in a value with units x_units
        and returns a number iwth untis y_units. We integrate from
        xmin to xmax, which both have units x_units and the integral
        is performed while weighting the function by a weight e_weight. """
    if xmin not in [0,-np.inf,np.inf]: xmin=float(xmin/x_units)
    if xmax not in [0,-np.inf,np.inf]: xmax=float(xmax/x_units)
    f=lambda x: x**e_weight*float(func(x*x_units)/y_units)
    return (x_units**(e_weight+1)*y_units)*\
            integrate.quad(f, xmin, xmax)[0]

def ulogspace(emin, emax, num, units):
    x=np.logspace(np.log10(float(emin/units)), 
                  np.log10(float(emax/units)), 
                  num),
    return u.tosympy(x,units)


class ParticleSpectrum(Spectrum):
    """ class to represent a spectrum of particles with total energy total_energy. 
    
        __call__ returns dn/de, the number of particles per unit energy (in units of 1/erg)
    """

    def __init__(self,total_energy):
        """ Normalize total energy output. """
        self.norm = 1
        self.norm= total_energy/uintegrate(self, 0*u.erg, np.inf*u.erg, x_units=u.erg, y_units=1, e_weight=1)

    def integrate(self, emin=0, emax=np.inf, **kwargs):
        return uintegrate(self, emin, emax, x_units=u.erg, y_units=1/u.erg, **kwargs)

class PowerLawCutoff(ParticleSpectrum):

    def __init__(self, total_energy, index, e_cutoff):
        self.index = index
        self.e_cutoff = e_cutoff
        self.e_break = e_break
        self.e_scale = u.GeV
        super(PowerLawCutoff,self).__init__(total_energy)

    def __call__(self, energy):
        """ Returns number of particles per unit energy [1/energy]. """
        return self.norm*(energy/self.e_scale)**(-self.index)*sympy.exp(-energy/self.e_cutoff)

class SmoothBrokenPowerLaw(ParticleSpectrum):
    """ A smoothed broken power-law particle distribution.

        This formula is taken from the fermi-LAT publication
        on W51C: http://arxiv.org/abs/0910.0908
    """
    def __init__(self, total_energy, index1, index2, e_scale, e_break):
        self.index = index
        self.e_cutoff = e_cutoff
        self.e_break = e_break
        self.e_scale = e_scale
        super(PowerLawCutoff,self).__init__(total_energy)

    def __call__(self, energy):
        """ Returns number of particles per unit energy [1/energy]. """
        return self.norm*(energy/self.e_scale)**(-self.index1)*(1 + (energy/self.e_break)**beta)*(-(index2-index1)/beta)

class BrokenPowerLawCutoff(ParticleSpectrum):

    def __init__(self, total_energy, index1, index2, e_cutoff, e_break):

        self.index1 = index1
        self.index2 = index2
        self.e_cutoff = e_cutoff
        self.e_break = e_break
        self.e_scale = u.eV
        super(BrokenPowerLawCutoff,self).__init__(total_energy)

    def __call__(self, energy):
        """ Return number of particles per unit energy [1/energy]. """
        return self.norm*((energy/self.e_scale)**-self.index1)/(1.+(energy/self.e_break)**(-self.index1+self.index2))*sympy.exp(-energy/self.e_cutoff)

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

        self.pref = 8*math.pi/(u.planck**3*u.speed_of_light**3)

    @staticmethod
    def occupation_number(x):
        """ This is equation 1.49 in R&L. """
        return 1/(sympy.exp(x)-1)

    def __call__(self, energy):
        """ Return the energy density in units of 1/energy/Volume."""
        return self.pref*energy**2*self.occupation_number(energy/self.kT)

    def integrate(self, emin, emax, **kwargs):
        """ Integrate the thermal spectrum from emin to emax.
            
            Integrand is in units of energy/volume
        
            Implementation note: integrate with energy measured in units of kT

            # note the E^3 dE -> kT^3 x^2 dx
        """
        return uintegrate(self,emin,emax,x_units=self.kT, y_units=self.pref*self.kT**2, **kwargs)

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

    @np.vectorize
    def F(x):
        """ for some reason, special.kv(5/3,1e10) is NaN, not 0 ???
            for now, just clip the function above 1e5 to be 0. """
        if x>1e5: return 0
        return x*integrate.quad(lambda j: special.kv(5./3,j),x,np.inf)[0]
    
    def __init__(self, electron_energy, magnetic_field):

        gamma = electron_energy/(u.electron_mass*u.speed_of_light**2)
        q = u.electron_charge
        B = magnetic_field
        sin_alpha = 1 # ?
        m = u.electron_mass
        c = u.speed_of_light

        # This is the prefactor from R&L (eq 6.18) - power/unit frequency
        self.pref = (math.sqrt(3)/(2*math.pi))*(q**3*B*sin_alpha)/(u.electron_mass*c**2)

        # convert to (power/unit energy)
        self.pref /= u.planck

        self.omega_c = 3*gamma**2*q*B*sin_alpha/(2*m*c)
        self.energy_c = u.hbar*self.omega_c

    def __call__(self,energy):
        """ return photons radiated per unit energy for a single
            electron [ph/s/photon energy]. """
        power_per_energy = self.pref*self.F(float(energy/self.energy_c))
        photons_per_energy = power_per_energy/energy
        return photons_per_energy

class Synchrotron(Spectrum):
    """ Calculates the syncrotron radiation
        from an electron spectrum in a magnetic field. """

    def __init__(self, electron_spectrum, magnetic_field):

        self.electron_spectrum = electron_spectrum
        self.magnetic_field = magnetic_field

    def __call__(self, photon_energy):
        """ Returns number per unit energy dN/dE. """

        """ return total power per unit energy by convolving energy per electron
            by the electron spectrum. """

        def integrand(electron_energy):
            single_electron=SingleElectronSynchrotron(
                electron_energy = electron_energy, 
                magnetic_field = self.magnetic_field)

            # return [ph/s/photon energy/electron energy] = 
            #             [ph/s/electron/photon energy]*[number of electrons/electron energy]
            return single_electron(photon_energy)*self.electron_spectrum(electron_energy)

        # integrate [ph/s/photon energy/electron energy] over electron energies
        # Returns the photon flux per unit time per unit photon energy [1/s/energy**2]
        return uintegrate(integrand,0,np.inf, x_units=u.erg, y_units=1/u.seconds/u.erg**2)

class SingleElectronInverseCompton(Spectrum):
    """ The inverse compton radiation an electron spectrum
        and photon spectrum. """

    def __init__(self, electron_energy, photon_spectrum):
        self.electron_energy = electron_energy
        self.photon_spectrum = photon_spectrum

    @staticmethod
    def f(q,gamma_e):
        """ This is equation 2.48 in Blumenthal & Gould. """
        return 2*q*sympy.log(q)+(1+2*q)*(1-q) + 0.5*(gamma_e*q)**2*(1-q)/(1+gamma_e*q)

    def __call__(self, scattered_photon_energy):
        """ Calculates the inverse compton spectrum expected
            from a sinle electron and an arbitrary photon spectrum. """

        mc2 = u.electron_mass*u.speed_of_light**2

        def integrand(target_photon_energy):

            ee = self.electron_energy

            # forbidden by kinematic concerns

            minmum_photon_energy = .5*(scattered_photon_energy + \
                  sympy.sqrt(scattered_photon_energy**2+ \
                             scattered_photon_energy*(mc2)**2/target_photon_energy))

            if ee < minmum_photon_energy: return 0

            gamma_e = 4*target_photon_energy*ee/(mc2)**2
            q=scattered_photon_energy/(ee*gamma_e*(1-scattered_photon_energy/ee))

            return 2*math.pi*u.r0**2*u.speed_of_light*\
                    (mc2/target_photon_energy)*\
                    self.photon_spectrum(target_photon_energy)*\
                    self.f(q,gamma_e)
                    
        # integrate over the photon field
        return uintegrate(integrand,0,np.inf, x_units=u.eV, y_units=1/u.seconds/u.eV)

class InverseCompton(Spectrum):

    def __init__(self, electron_spectrum, photon_spectrum):
        self.electron_spectrum = electron_spectrum
        self.photon_spectrum = photon_spectrum

    def __call__(self, photon_energy):
        """ Returns number per unit energy dN/dE. """

        def integrand(electron_energy):
            single_electron=SingleElectronInverseCompton(
                electron_energy = electron_energy, 
                photon_spectrum = self.photon_spectrum)

            return single_electron(photon_energy)*self.electron_spectrum(electron_energy)

        # integrate over all electrons
        return uintegrate(integrand,0,np.inf, x_units=u.eV, y_units=1/u.seconds/u.eV**2)




if __name__ == '__main__':

    # all the code below is for testing out the main code.

    def plot_sed(synch,distance,
                 x_units = u.eV,
                 y_units = u.eV/u.cm**2/u.s,
                ):
        """ Plot the synchotron + inverse compton SED. """

        emin=1e-7*u.eV
        emax=1e15*u.eV

        x = ulogspace(emin, emax, 100, u.eV)

        print 'min',synch(emin)
        print 'max',synch(emax)

        # y is in units of self.units()
        y = sympy.Matrix(map(synch,x)).transpose()
        y=y.multiply_elementwise(x).multiply_elementwise(x)

        y /= (4*math.pi*distance**2)

        fig = P.figure(None,figsize=(5.5,4.5))
        P.clf()
        fig.subplots_adjust(left=0.18,bottom=0.13,right=0.95,top=0.95)
        axes = fig.add_subplot(111)

        x = u.tonumpy(x,x_units)
        y = u.tonumpy(y,y_units)
        axes.loglog(x,y)

        axes.set_xlim(1e-7,1e15)
        axes.set_ylim(1e-08,1e-1)

        axes.set_xlabel('Energy (eV)')
        axes.set_ylabel(r'E$^2$ dN/dE (eV cm$^{-2}$ s$^{-1}$)')

        P.savefig('sed.png')

    def stefan_hess_j1813():
        electron_spectrum = BrokenPowerLawCutoff(
                total_energy = 2e48*u.erg,
                index1 = 2.0,
                index2 = 3.0,
                e_break = 1e7*u.eV,
                e_cutoff = 1.e14*u.eV)

        print 'total electron energy %s' % u.repr(electron_spectrum.integrate(e_weight=1),'erg')
        emin=1e-7*u.eV
        emax=1e15*u.eV

        #electron_spectrum.loglog(emin=emin, emax=emax, 
        #           e_weight=2, x_units='eV', y_units='eV', 
        #           filename='ElectronSpectrum.png')

        syn = SingleElectronSynchrotron(electron_energy=1e3*u.MeV,
                                        magnetic_field=3e-6*u.gauss)

        synch = Synchrotron(electron_spectrum=electron_spectrum,
                          magnetic_field=3e-6*u.gauss)

        cmb=CMB()

        #ic = InverseCompton(electron_spectrum=electron_spectrum,
        #                    photon_spectrum = cmb)

        ic = SingleElectronInverseCompton(electron_energy=u.TeV,
                                          photon_spectrum = cmb)


        plot_sed(ic,distance=4.2*u.kpc)


    stefan_hess_j1813()

    def test_thermal_spectrum():
        cmb=CMB()
        print 'kt=',cmb.kT
        print 'dnde=',cmb(cmb.kT)
        total_energy_density = cmb.integrate(e_weight=1)
        print 'total',total_energy_density
        print 'computed = ', u.repr(total_energy_density,'eV/m^3')
        print 'from stefan = 2.60e5 eV/m^3'

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

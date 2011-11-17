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


def logsimps(f,xmin,xmax, per_decade):
    """ Perform the simpson integral of a function f(x)
        from xmin to xmax evaluationg the function
        unifomrly in log space.

        Note: int f(x) dx = int f(x) x dlog(x). """

    npts = per_decade*(np.log10(xmax)-np.log10(xmin))
    x = np.logspace(np.log(xmin),np.log(xmax), npts)
    y = f(x) * x
    log_x = np.log(x)
    return integrate.simps(y=y, x=log_x)

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


class Synchrotron(Spectrum):
    """ Calculates the syncrotron power radiated
        by a spectrum of electrons in a magnetic field. 

        This treatment follows section 6.2 in R&L and especially  
        the formulas 6.17c, 6.18, and 6.31c
    
        The spectrum is in unit of energy per unit time
        per unit frequency emitted by a single electron.
        """

    """ This is equation 6.31 in R&L. """

    per_decade = 10

    @np.vectorize
    def F(x):
        """ for some reason, special.kv(5/3,1e10) is NaN, not 0 ???
            for now, just clip the function above 1e5 to be 0. 

            N.B very important to always return a float since the type of
            the entire return array returned when a vector is passed in
            is decided by the type of the first number that is returned.

            See http://docs.scipy.org/doc/numpy-1.6.0/reference/generated/numpy.vectorize.html """
        if x>1e5: return float(0)
        return x*integrate.quad(lambda j: special.kv(5./3,j),x,np.inf)[0]

    def __init__(self, electron_spectrum, magnetic_field):

        self.electron_spectrum = electron_spectrum

        q = u.electron_charge
        B = magnetic_field
        sin_alpha = 1 # ?
        print 'what to do about sin(alpha)'
        m = u.electron_mass
        c = u.speed_of_light


        # This is the prefactor from R&L (eq 6.18) - power/unit frequency
        self.pref = (math.sqrt(3)/(2*math.pi))*(q**3*B*sin_alpha)/(u.electron_mass*c**2)
        # convert from (power/frequency) to (power/energy) in units of erg/s/erg (or 1/s)
        self.pref /= u.planck
        self.pref = float(self.pref/(u.erg*u.second**-1*u.erg**-1))

        # This is formula 6.17 in R&L except for the gamma**2
        omega_c = 3*q*B*sin_alpha/(2*m*c)
        self.energy_c_pref = float(u.hbar*omega_c/u.erg)

        self.mc2 = m*c**2
        self.mc2_in_erg = float(self.mc2/u.erg)

    def spectrum(self, photon_energy):
        """ return total power per emitted per unit energy by
            the spectrum of electrons.
            
            Integrate the power by a single electron over the spectrum of electrons. """

        def integrand(electron_energy):
            """ Integrate over electron gamma: unitless =). """
            electron_gamma = electron_energy/self.mc2_in_erg
            

            energy_c = electron_gamma**2*self.energy_c_pref


            # power_per_energy in units of erg/s/erg
            power_per_energy = self.pref*self.F(photon_energy/energy_c)
            # divide by photon energy to get photons/energy for a single
            # electron (in units of ph/erg/s)
            photons_per_energy = power_per_energy/photon_energy

            # return [ph/s/photon energy/electron energy] = 
            #             [ph/s/electron/photon energy]*[number of electrons/electron energy]
            return photons_per_energy*self.electron_spectrum(electron_energy, units=False)

        # integrate [ph/s/photon energy/electron energy] over electron energies
        # Returns is photon flux per energy per time [1/erg/s]
        emin = self.electron_spectrum.emin
        emax = self.electron_spectrum.emax
        return logsimps(integrand,emin, emax, per_decade=self.per_decade)

    @staticmethod
    def units_string(): return '1/erg/s'

class SingleElectronInverseCompton(Spectrum):
    """ The inverse compton radiation an electron spectrum
        and photon spectrum. """

    def __init__(self, electron_spectrum, photon_spectrum):
        self.electron_spectrum = electron_spectrum
        self.photon_spectrum = photon_spectrum

    @staticmethod
    def f(q,gamma_e):
        """ This is equation 2.48 in Blumenthal & Gould. """
        return 2*q*np.log(q)+(1+2*q)*(1-q) + 0.5*(gamma_e*q)**2*(1-q)/(1+gamma_e*q)

    def __call__(self, scattered_photon_energy):
        """ Calculates the inverse compton spectrum expected
            from a sinle electron and an arbitrary photon spectrum. """

        mc2 = u.electron_mass*u.speed_of_light**2

        def integrand(electron_energy, target_photon_energy):

            ee = self.electron_energy

            # forbidden by kinematic concerns

            minmum_photon_energy = .5*(scattered_photon_energy + \
                  np.sqrt(scattered_photon_energy**2+ \
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


    def __call__(self, photon_energy):
        """ Returns number per unit energy dN/dE. """

        def integrand(electron_energy):
            single_electron=SingleElectronInverseCompton(
                electron_energy = electron_energy, 
                photon_spectrum = self.photon_spectrum)

            return single_electron(photon_energy)*self.electron_spectrum(electron_energy)

        # integrate over all electrons
        return uintegrate(integrand,0,np.inf, x_units=u.eV, y_units=1/u.seconds/u.eV**2)


def plot_sed(synch,
             distance,
             x_units = 'eV',
             y_units = 'eV/cm^2/s^1',
            ):
    """ Plot the synchotron + inverse compton SED. """

    emin=1e-7*u.eV
    emax=1e15*u.eV

    x = sympy.Matrix(u.erg*np.logspace(
        np.log10(float(emin/u.erg)), np.log10(float(emax/u.erg)), 100))
    # y is in units of self.units()
    y = sympy.Matrix(map(synch,x)).transpose()


    y=y.multiply_elementwise(x).multiply_elementwise(x)
    y /= (4*math.pi*distance**2)


    fig = P.figure(None,figsize=(5.5,4.5))
    P.clf()
    fig.subplots_adjust(left=0.18,bottom=0.13,right=0.95,top=0.95)
    axes = fig.add_subplot(111)

    x = u.tonumpy(x,u.fromstring(x_units))
    y = u.tonumpy(y,u.fromstring(y_units))
    axes.loglog(x,y)

    axes.set_xlabel('Energy (%s)' % x_units)
    axes.set_ylabel(r'E$^2$ dN/dE (%s)' % y_units)

    #axes.set_ylim(ymin=1e-5)

    P.savefig('sed.png')


if __name__ == '__main__':

    # all the code below is for testing out the main code.

    def test_spectra():
        p = PowerLaw(total_energy = 2e48*u.erg, index=2.6,
                     emin=1e-6*u.eV,emax=1e14*u.eV)
        #ax=p.loglog(u.keV,u.MeV, e_weight=2, filename='sed.png')
        print 'total electron energy,',u.repr(p.integral(e_weight=1,units=True),'erg')
    #test_spectra()

    def stefan_hess_j1813():
        electron_spectrum = BrokenPowerLawCutoff(
                total_energy = 2e48*u.erg,
                index1 = 2.0,
                index2 = 3.0,
                e_break = 1e7*u.eV,
                e_cutoff = 1.e14*u.eV,

                emin=1e-6*u.eV,
                emax=1e17*u.eV)

        print 'total electron energy %s' % u.repr(electron_spectrum.integral(e_weight=1,units=True),'erg')
        emin=1e-7*u.eV
        emax=1e15*u.eV

        electron_spectrum.loglog(emin=emin, emax=emax, 
                   e_weight=2, x_units='eV', y_units='eV', 
                   filename='ElectronSpectrum.png')

        synch = Synchrotron(electron_spectrum=electron_spectrum,
                            magnetic_field=3e-6*u.gauss)

        cmb=CMB()

        #ic = InverseCompton(electron_spectrum=electron_spectrum,
        #                    photon_spectrum = cmb)

        #ic = SingleElectronInverseCompton(electron_energy=u.TeV,
        #                                  photon_spectrum = cmb)


        plot_sed(synch,distance=4.2*u.kpc)


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
    #yasunobu_w51c()


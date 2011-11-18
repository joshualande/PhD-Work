import numpy as np

from sed_spectrum import Spectrum
import sed_units as u

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
        print 'what to do about sin(alpha)???'
        m = u.electron_mass
        c = u.speed_of_light


        # This is the prefactor from R&L (eq 6.18) - power/unit frequency
        self.pref = (np.sqrt(3)/(2*np.pi))*(q**3*B*sin_alpha)/(u.electron_mass*c**2)
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

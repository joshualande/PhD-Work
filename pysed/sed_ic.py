import numpy as np

from sed_spectrum import Spectrum

class InverseCompton(Spectrum):
    """ The inverse compton radiation an electron spectrum
        and photon spectrum. """

    per_decade = 10

    def __init__(self, electron_spectrum, photon_spectrum):
        self.electron_spectrum = electron_spectrum
        self.photon_spectrum = photon_spectrum

    @staticmethod
    def F(q,gamma_e):
        """ This is equation 2.48 in Blumenthal & Gould. """
        return 2*q*np.log(q)+(1+2*q)*(1-q) + 0.5*(gamma_e*q)**2*(1-q)/(1+gamma_e*q)

    def spectrum(self, scattered_photon_energy):
        """ Calculates the inverse compton spectrum expected
            from a sinle electron and an arbitrary photon spectrum. 
            
            Returns [ph/s/scattered photon energy]. """

        mc2 = float(u.electron_mass*u.speed_of_light**2/u.erg)

        def integrand(electron_energy, target_photon_energy):
            """ return [ph/s/incident photon energy/scattered photon energy] 
                for a single electron
                
                in units [1/s/erg^2]
            """

            ee = electron_energy
            c = u.speed_of_light
            m = u.electron_mass

            electron_gamma = target_photon_energy/mc2

            gamma_e = 4*target_photon_energy*ee/(mc2)**2
            q=scattered_photon_energy/(ee*gamma_e*(1-scattered_photon_energy/ee))

            # this formula is basically 7.28a in R&L with the difference that

            # C => photon_spectrum
            # v(energy) => 

            # prefactor has units cm^3*s^-1*erg^-1
            pref = 2*np.pi*u.r0**2*c*electron_gamma**-2*(target_photon_energy*u.erg)**-1
            
            pref = float(pref/(u.cm**3*u.second**-1*u.erg**-1))

            # Note, photon_spectrum has units 'ph/erg/cm^3'
            # F is unitless
            # so pref*photon_spectrum*F has units ph/erg/cm^3 * cm^3*s^-1*erg^-1 = ph s^-1 erg^-2
            return pref*\
                    self.photon_spectrum(target_photon_energy, units=False)*\
                    self.F(q,gamma_e)

        def integrate_over_electron(target_photon_energy):
            """ Integrate the InverseCompton spectrum over the photon electron distribution.
            
                returns [ph/s/incident photon energy/scattered photon energy] """
            
            f=lambda electron_energy: integrand(electron_energy,target_photon_energy)*\
                    self.electron_spectrum(electron_energy, units=False)

            emin = self.electron_spectrum.emin
            emax = self.electron_spectrum.emax

            return logsimps(f,emin,emax,self.per_decade)
        # would be nice to vectorize both integrals =(
        integrate_over_electron = np.vectorize(integrate_over_electron)


        emin = self.photon_spectrum.emin
        emax = self.photon_spectrum.emax

        return logsimps(integrate_over_electron,emin,emax,self.per_decade)

    @staticmethod
    def units_string(): return '1/erg/s'


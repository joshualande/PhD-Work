""" Calculates the gamma ray emisison predicted
    by pi0 decay.
    for a given electron and photon spectrum.
    

    Author: Joshua Lande <joshualande@gmail.com>
"""
import numpy as np

from sed_spectrum import Spectrum
from sed_integrate import logsimps
import sed_units as u

class PPCrossSection(object):
    """ Module wraps the ugliness of cparamlib 
        for computing the proton-proton corss seciton
        to decay into gammas.

        To install this module, please visit this page:

            http://homepages.spa.umn.edu/~nkarlsson/cparamlib/
    
    """

    def __init__(self):
        # module to calculate Pi0 cross section
        from cparamlib.cparamlib import ID_GAMMA
        from cparamlib.ParamModel import ParamModel

        self.param = ParamModel(Tp=0,particle=ID_GAMMA)

        self.erg_to_gev = float(u.erg/u.GeV)
        self.millibarn_to_cm2 = float(u.millibarn/u.cm**2)

    def __call__(self, proton_energy,photon_energy):
        """ Computes the proton proton cross section to decay into a gamma.

            proton_energy is the energy of the incident proton, in units of erg
            photon_energy is the energy of the resultant gamma, in units of erg

            The return cross section is d(sigma)/dE where E is the photon energy,
            sigma is in units of cm**2, and E is in units of erg.

            Implementation Note:

                Sigma_incl_tot returns the photon spectrum including all
                processes.

                sigma_incl_tot returns dsigma/dlog(E) in units of mb.
                The two inputs must be in units of GeV and dlog(E) is
                calculated (I assume) in units of GeV
        """

        photon_energy_gev = photon_energy*self.erg_to_gev
        proton_energy_gev = proton_energy*self.erg_to_gev

        dsigmadloge = self.param.sigma_incl_tot(photon_energy_gev, proton_energy_gev)

        # convert from cross section per log(energy) in units of millibarn
        # to cross section per(energy) in units of cm^2

        dsigmade = self.millibarn_to_cm2*dsigmadloge*(1/photon_energy)
        return dsigmade



class Pi0Decay(Spectrum):
    """ Computes the Pi0 decay flux
        for a spectrum of protons
        hitting a density of particles. """

    # default energy range = all energies
    emin,emax = 0,np.inf
    vectorized = False
    per_decade = 10

    def __init__(self,
                 proton_spectrum, 
                 target_density,
                 scaling_factor):
        """ 
        
            proton_spectrum:  differental number of protons.
            target_density: density that input spectrum is hitting
        
            Scaling factor: to account for healium and heavy nuclei 
                For W51C, was set to 1.85 (http://arxiv.org/abs/0910.0908)

        """
        print 'The Pi0-decay code needs to be validated and the formulas inspected + documented'


        self.cross_section = PPCrossSection()

        self.proton_spectrum = proton_spectrum

        self.scaling_factor = scaling_factor

        self.target_density = target_density

        self.prefactor = self.scaling_factor*self.target_density*u.speed_of_light
        self.prefactor = float(self.prefactor/(u.cm**-2*u.seconds**-1))

    def _spectrum(self,photon_energy):
        """ Return spectrum in units of s^-1 erg^-1. """

        def integrand(proton_energy):

            # Units: (s^-1 erg^-2) = (cm^-2 s^-1) x (protons erg^-1) x (cm^2 erg^-1)
            return self.prefactor*self.proton_spectrum(proton_energy, units=False)*self.cross_section(proton_energy, photon_energy)

        integrand = np.vectorize(integrand) # right now, cparamlib not vectorized

        emin = self.proton_spectrum.emin
        emax = self.proton_spectrum.emax
        return logsimps(integrand, emin, emax, self.per_decade)

    @staticmethod
    def units_string(): return '1/s/erg'

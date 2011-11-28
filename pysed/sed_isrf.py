""" This file provides a class for parsing the GALPROP 
    Interstellar Radiation Field (ISRF) for computing
    the photon fields important for Inverse Compton
    of photons in astrophysical objects.

    Author: Joshua Lande <joshualande@gmail.com>
"""
import pyfits
import numpy as np

from . import sed_units as u

class ISRF(object):

    def __init__(self, isrf):
        """ isrf is the GALPROP ISRF fits mapcube.

            The file I am using is 
                
                MilkyWay_DR0.5_DZ0.1_DPHI10_RMAX20_ZMAX5_galprop_format.fits.gz

            and can be found at 

                http://galprop.stanford.edu/resources.php?option=data
        """

        self.isrf = pyfits.open(isrf)[0]


        for number, line in [
            [18,'Units micron eV cm^-3 micron^-1'],
            [19,"R:z:log10(wavelength):component"],
            [20,"kpc:kpc:log10(micron):integer"],
            [21,"Component 1 = optical"],
            [22,"Component 2 = infrared"],
            [23,"Component 3 = CMB"]]:

            if self.isrf.header[number] != line: raise Exception("Unrecognized header for ISRF.")

    def R_to_index(self, R):
        R_internal = float(R/u.kpc)

        h = self.isrf.header
        start, delt, num = h['CRVAL1'], h['CDELT1'], h['NAXIS1']

        index = (R_internal - start)/delt
        return index
        

    def z_to_index(self, z):
        z_internal = float(z/u.kpc)

        h = self.isrf.header
        start, delt, num = h['CRVAL2'], h['CDELT2'], h['NAXIS2']
        
        index = (z_internal - start)/delt
        return index

    def get_wavelength(self):
        """ Get the wavelengths in the mapcube. """

        h = self.isrf.header
        start, delt, num = h['CRVAL3'], h['CDELT3'], h['NAXIS3']

        wavelength = 10**(start + delt*np.arange(num))
        return u.tosympy(wavelength, u.micron)

    def get_energy(self):
        wavelength = self.get_wavelength()
        
        f=wavelength.applyfunc(lambda w: u.planck*u.speed_of_light/w)

        return wavelength.applyfunc(lambda w: u.planck*u.speed_of_light/w)


    def get(self, component, R, z):
        """ Get the ISRF for a given compoenent and a given galactic position. """

        R_index = self.R_to_index(R)
        z_index = self.z_to_index(z)

        print 'for now, clip. This is BAD. Should be an interpolation.'
        R_index = int(R_index)
        z_index = int(z_index)

        radiation = self.isrf.data[component,:,z_index,R_index]

        return u.tosympy(radiation,u.eV*u.cm**-3)

        
    def get_optical(self, *args, **kwargs): 
        """ Get the optical ISRF. """
        return self.get(0, *args, **kwargs)

    def get_infrared(self, *args, **kwargs): 
        """ Get the infrared ISRF. """
        return self.get(1, *args, **kwargs)

    def get_CMB(self, *args, **kwargs): 
        """ Get the CMB ISRF. """
        return self.get(2, *args, **kwargs)


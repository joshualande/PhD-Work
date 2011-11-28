""" Plots the ISRF as calculated by GALPROP

    Typical reference for GALPROP: Moskalenko et al 2006 (arXiv:astro-ph/0511149v2)

    Author: Joshua Lande <joshualande@gmail.com>
"""
import pylab as P
from pysed.sed_isrf import ISRF
import pysed.sed_units as u

if __name__ == '__main__':

    # load in ISRF
    isrf = ISRF('MilkyWay_DR0.5_DZ0.1_DPHI10_RMAX20_ZMAX5_galprop_format.fits.gz')

    # define position in galaxy
    kwargs=dict(R=5*u.kpc,z=0)

    # get data form mapcube
    energy = isrf.get_energy()
    infrared=isrf.get_infrared(**kwargs)
    cmb=isrf.get_CMB(**kwargs)
    optical=isrf.get_optical(**kwargs)

    # convert to unitless quanitites + plot
    energy = u.tonumpy(energy, u.eV)
    infrared = u.tonumpy(infrared, u.eV*u.cm**-3)
    cmb = u.tonumpy(cmb, u.eV*u.cm**-3)
    optical = u.tonumpy(optical, u.eV*u.cm**-3)

    P.loglog(energy, infrared, label='infrared')
    P.loglog(energy, cmb, label='CMB')
    P.loglog(energy, optical, label='optical')

    P.legend(loc=3)

    P.xlabel('energy (eV')
    P.ylabel('intensity (eV/cm^3)')

    P.savefig('isrf.pdf')

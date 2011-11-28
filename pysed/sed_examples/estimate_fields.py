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
    infrared = u.tonumpy(infrared, u.cm**-3*u.eV**-1)
    cmb = u.tonumpy(cmb, u.cm**-3*u.eV**-1)
    optical = u.tonumpy(optical, u.cm**-3*u.eV**-1)

    P.loglog(energy, infrared, color='red', label='infrared')
    P.loglog(energy, cmb, color='blue', label='CMB')
    P.loglog(energy, optical, color='green', label='optical')


    # now, overlay estimated quantities
    infared_est = isrf.estimate_infrared(**kwargs)
    plot_kwargs = dict(x_units_string = 'eV', y_units_string='ph/cm^3/eV', dashes=[5,2])
    infared_est.loglog(color='red', **plot_kwargs)

    P.legend(loc=3)

    P.xlabel('energy (eV)')
    P.ylabel('intensity (ph/cm^3/eV)')

    P.savefig('estimate_fields.pdf')

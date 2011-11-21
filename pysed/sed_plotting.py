""" Code related to plotting SEDs.

    Author: Joshua Lande <joshualande@gmail.com>
"""
import numpy as np
import pylab as P

import sympy

import sed_units as u

def plot_sed(spectra,
             distance,
             x_units_string = 'eV',
             y_units_string = 'eV/cm^2/s^1',
             emin=1e-7*u.eV,
             emax=1e15*u.eV,
             npts=1000,
             filename=None
            ):
    """ Plot an E^2 dN/dE SED with multiple componets.
    
        Spectra is a dictionary:

        E.G:
            spectra = {'Synchrotron': sed_synch.Synctrotron(...),
                       'Inverse Compton': sed_ic.InverseCompton(...)}
    """


    fig = P.figure(None,figsize=(5.5,4.5))
    P.clf()
    fig.subplots_adjust(left=0.18,bottom=0.13,right=0.95,top=0.95)
    axes = fig.add_subplot(111)

    for k,v in spectra.items():
        print k,v
        v.loglog(emin=emin, emax=emax,
                 x_units_string = x_units_string,
                 y_units_string = y_units_string,
                 e_weight=2,
                 scale=1/(4*np.pi*distance**2),
                 npts=npts,
                 axes=axes,
                 label=k)

    axes.set_xlabel('Energy (%s)' % x_units_string)
    axes.set_ylabel(r'E$^2$ dN/dE (%s)' % y_units_string)

    if filename is not None: P.savefig(filename)
    return axes

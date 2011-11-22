""" Code related to plotting SEDs.

    Author: Joshua Lande <joshualande@gmail.com>
"""
import numpy as np
import pylab as P

import sympy

import sed_units as u

class SEDPlotter(object):
    """ Plot an E^2 dN/dE SED with multiple componets.
    
        Spectra is a dictionary:

        E.G:
            spectra = {'Synchrotron': sed_synch.Synctrotron(...),
                       'Inverse Compton': sed_ic.InverseCompton(...)}
    """

    def __init__(self, 
                 distance,
                 x_units_string = 'eV',
                 y_units_string = 'eV/cm^2/s^1',
                 emin=1e-7*u.eV,
                 emax=1e15*u.eV,
                 npts=1000,
                 axes=None, 
                 fignum=None, 
                 figsize=(5.5,4.5)):

        self.distance=distance
        self.x_units_string = x_units_string
        self.x_units = u.fromstring(x_units_string)
        self.y_units_string = y_units_string 
        self.y_units = u.fromstring(y_units_string)
        self.emin = emin
        self.emax = emax
        self.npts = npts

        self.scale = 1/(4*np.pi*distance**2)

        # Here, define the axes
        if axes is None:
            fig = P.figure(fignum,figsize)
            P.clf()
            fig.subplots_adjust(left=0.18,bottom=0.13,right=0.95,top=0.95)
            self.axes = fig.add_subplot(111)

            # Format the axes
            self.axes.set_xlabel('Energy (%s)' % x_units_string)
            self.axes.set_ylabel(r'E$^2$ dN/dE (%s)' % y_units_string)

            self.axes.set_xlim(xmin=float(emin/self.x_units), ymax=float(emax/self.x_units))
        else:
            self.axes = axes

    def plot(self, spectra, **kwargs):

        spectra.loglog(emin=self.emin, emax=self.emax,
                 x_units_string = self.x_units_string,
                 y_units_string = self.y_units_string,
                 e_weight=2,
                 scale=self.scale,
                 npts=self.npts,
                 axes=self.axes,
                 **kwargs)

    def save(self, filename):
        self.axes.figure.savefig(filename)

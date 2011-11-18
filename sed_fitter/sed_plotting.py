import numpy as np
import pylab as P

import sympy

import sed_units as u

def plot_sed(synch,
             distance,
             x_units = 'eV',
             y_units = 'eV/cm^2/s^1',
            ):
    """ Plot the synchotron + inverse compton SED. """

    emin=1e-7*u.eV
    emax=1e15*u.eV

    x = u.tosympy(np.logspace(np.log10(float(emin/u.erg)), np.log10(float(emax/u.erg)), 100),u.erg)
    # y is in units of self.units()
    y = sympy.Matrix(map(synch,x)).transpose()


    y=y.multiply_elementwise(x).multiply_elementwise(x)
    y /= (4*np.pi*distance**2)


    fig = P.figure(None,figsize=(5.5,4.5))
    P.clf()
    fig.subplots_adjust(left=0.18,bottom=0.13,right=0.95,top=0.95)
    axes = fig.add_subplot(111)

    x = u.tonumpy(x,u.fromstring(x_units))
    y = u.tonumpy(y,u.fromstring(y_units))
    axes.loglog(x,y)

    axes.set_xlabel('Energy (%s)' % x_units)
    axes.set_ylabel(r'E$^2$ dN/dE (%s)' % y_units)

    #axes.set_ylim(ymin=1e-8)

    P.savefig('sed.png')
    return axes

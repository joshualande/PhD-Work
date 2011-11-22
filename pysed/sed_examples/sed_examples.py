""" A series of examples to demonstrate the power
    of this SED package.

    Author: Joshua Lande <joshualande@gmail.com>
"""
import numpy as np
import pylab as P

from pysed.sed_particle import BrokenPowerLawCutoff,SmoothBrokenPowerLaw
from pysed.sed_ic import InverseCompton
from pysed.sed_synch import Synchrotron
from pysed.sed_plotting import SEDPlotter
from pysed.sed_thermal import CMB,ThermalSpectrum
import pysed.sed_units as u

def plot_sychrotron_function():
    """ Reproduce Figure 6.6 from R&L, which
        plots equation 6.31c from R&L.
        This is the characteristic formula for synchrotron
        radiation. """
    x=np.linspace(0,4)
    y=Synchrotron.F(x)
    P.plot(x,y)
    P.ylabel('F(x)')
    P.xlabel('x')
    P.savefig('synchrotron_function')



def test_spectra():
    p = PowerLaw(total_energy = 2e48*u.erg, index=2.6,
                 emin=1e-6*u.eV,emax=1e14*u.eV)
    #ax=p.loglog(u.keV,u.MeV, e_weight=2, filename='sed.png')
    print 'total electron energy,',u.repr(p.integrate(e_weight=1,units=True),'erg')

def plot_CMB_spectra():
    cmb=CMB()
    emin=1e-3*cmb.kT*u.erg
    emax=1e2*cmb.kT*u.erg
    cmb.loglog(e_weight=2, x_units='2.725*kelvin*boltzmann', filename='cmb.png')

def stefan_hess_j1813():
    """ Calculates the SED Stefan gave me of HESS J1813. """
    electron_spectrum = BrokenPowerLawCutoff(
            total_energy = 2e48*u.erg,
            index1 = 2.0,
            index2 = 3.0,
            e_break = 1e7*u.eV,
            e_cutoff = 1.e14*u.eV,
            emin=1e-6*u.eV,
            emax=1e17*u.eV)

    print 'total electron energy %s' % u.repr(electron_spectrum.integrate(e_weight=1,units=True),'erg')
    emin=1e-7*u.eV
    emax=1e15*u.eV

    electron_spectrum.loglog(e_weight=2, x_units_string='eV', y_units_string='eV', 
                             filename='electrons.png')

    synch = Synchrotron(electron_spectrum=electron_spectrum,
                        magnetic_field=3e-6*u.gauss)

    cmb=CMB()

    ic = InverseCompton(electron_spectrum=electron_spectrum,
                        photon_spectrum = cmb)


    #plot_sed(synch,distance=4.2*u.kpc)
    spectra = dict()
    spectra['Synchrotron']=synch
    spectra['Inverse Compton']=ic

    axes=plot_sed(
        spectra,
        distance=4.2*u.kpc,
        )
    axes.set_ylim(ymin=1e-8)
    P.savefig(filename='HESS_J1813_sed.png')


def test_thermal_spectrum():
    cmb=CMB()
    print 'kt=',cmb.kT
    print 'dnde=',cmb(cmb.kT)
    total_energy_density = cmb.energy_density()
    print 'total',total_energy_density
    print 'computed = ', u.repr(total_energy_density,'eV/m^3')
    print 'from stefan = 2.60e5 eV/m^3'

if __name__ == '__main__':


    plot_sychrotron_function()
    test_spectra()
    test_thermal()
    test_thermal_spectrum()
    stefan_hess_j1813()

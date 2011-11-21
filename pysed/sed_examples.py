""" A series of examples to demonstrate the power
    of this SED package.

    Author: Joshua Lande <joshualande@gmail.com>
"""
import numpy as np
import pylab as P

from sed_particle import BrokenPowerLawCutoff,SmoothBrokenPowerLaw
from sed_ic import InverseCompton
from sed_synch import Synchrotron
from sed_plotting import plot_sed
from sed_thermal import CMB,ThermalSpectrum
import sed_units as u

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
    print 'total electron energy,',u.repr(p.integral(e_weight=1,units=True),'erg')

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

    print 'total electron energy %s' % u.repr(electron_spectrum.integral(e_weight=1,units=True),'erg')
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


def w51C_yasunobu_ic():
    """ Compute the SED of W51C using parameters from
        http://arxiv.org/abs/0910.0908

        SED for for hypothesis (c) InverseCompton
    """

    # SmoothBrokenPowerLaw formula is equation 1 in text

    # Electron distribution parameters taken from Table 1 in text
    electrons = SmoothBrokenPowerLaw(
        total_energy=11e50*u.erg,
        index1 = 1.5, # p10 in text
        index2 = 1.5 + 1.4, # index2 = index1 + delta_s
        e_break = 20*u.GeV,
        e_scale = 1*u.GeV, # p10 in text
        beta = 2,
        emin = 10*u.MeV, # from footnote to table 1
        emax = 100*u.TeV, # I hope this is large enough
        )

    electrons.loglog(
        e_weight = 2,
        x_units_string='MeV', y_units_string='MeV', 
        filename='w51c_electrons.png')

    B = 2*u.microgauss

    # Photon fields take from table 1
    cmb = CMB()
    infrared = ThermalSpectrum(kT=3e-3*u.eV)
    optical = ThermalSpectrum(kT=0.25*u.eV)

    def plot_photon_fields():
        kwargs = dict(x_units_string='eV',y_units_string='eV/cm^3', e_weight=2)
        axes = cmb.loglog(label='cmb',**kwargs)
        infrared.loglog(label='infrared',axes=axes,**kwargs)
        optical.loglog(label='optical',axes=axes,**kwargs)
        P.legend()
        P.savefig('w51c_photon_fields.png')
    plot_photon_fields()

    print 'Energy Density: \n\tCMB=%s, \n\tinfrared=%s, \n\toptical=%s' % \
        (u.repr(cmb.energy_density(),'eV*cm^-3'),
         u.repr(infrared.energy_density(),'eV*cm^-3'),
         u.repr(optical.energy_density(),'eV*cm^-3'))

    synch = Synchrotron(electron_spectrum=electron_spectrum,
                        magnetic_field=3e-6*u.gauss)

    spectra = dict()
    spectra['Synchrotron']=synch
    #spectra['Inverse Compton']=ic

    axes=plot_sed(
        spectra,
        distance=distance,
        x_units='eV',
        y_units_string='erg*cm^-2*s^-1',
        )
    #axes.set_ylim(ymin=1e-8)
    P.savefig(filename='w51c_photon_fields.png')

if __name__ == '__main__':


    w51C_yasunobu_ic()

    if False:
        plot_sychrotron_function()
        test_spectra()
        test_thermal()
        test_thermal_spectrum()
        stefan_hess_j1813()

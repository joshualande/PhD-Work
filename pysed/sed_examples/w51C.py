""" Compute the SED of W51C using parameters from
    http://arxiv.org/abs/0910.0908

    SED for for hypothesis (c) InverseCompton

    Author: Joshua Lande <joshualande@gmail.com>
"""
import pylab as P
import numpy as np
from mpl_toolkits.axes_grid1 import AxesGrid

from pysed.sed_particle import SmoothBrokenPowerLaw
from pysed.sed_ic import InverseCompton
from pysed.sed_pi0 import Pi0Decay
from pysed.sed_synch import Synchrotron
from pysed.sed_spectrum import CompositeSpectrum
from pysed.sed_plotting import SEDPlotter
from pysed.sed_thermal import CMB,ThermalSpectrum
import pysed.sed_units as u

np.seterr(all='ignore')


def ic_dominated(axes):
    """ Compute the SED for W51C in the IC hypothesis
        (c) in table 1 Fig.4 of the text. """

    # SmoothBrokenPowerLaw formula is equation 1 in text
    # Electron distribution parameters taken from Table 1 in text
    # for model (c) InverseCompton
    electrons = SmoothBrokenPowerLaw(
        total_energy=11e50*u.erg,
        index1 = 1.5, # p10 in text
        index2 = 1.5 + 2.3, # index2 = index1 + delta_s
        e_break = 20*u.GeV,
        e_scale = 1*u.GeV, # p10 in text
        beta = 2,
        emin = 10*u.MeV, # from footnote to table 1
        emax = 100*u.TeV, # I hope this is large enough
        )

    distance = 6*u.kiloparsec # from page 8 in text

    # Plot the electron spectrum
    electrons.loglog(
        e_weight = 2,
        x_units_string='MeV', y_units_string='MeV', 
        filename='w51C_electrons.png')

    magnetic_field = 2*u.microgauss # From table 1 in text for (c) Inverse Compton

    # Photon fields take from table 1 for (c) Inverse Compton
    cmb = CMB()
    infrared = ThermalSpectrum(kT=3e-3*u.eV, energy_density=0.9*u.eV*u.cm**-3)
    optical = ThermalSpectrum(kT=0.25*u.eV, energy_density=0.84*u.eV*u.cm**-3)
    photon_fields = CompositeSpectrum(cmb, infrared, optical)

    def plot_photon_fields():
        """ Conveniene function to plot the photon fields. """
        kwargs = dict(x_units_string='eV',y_units_string='eV/cm^3', e_weight=2)
        axes = cmb.loglog(label='cmb',color='red',**kwargs)
        infrared.loglog(label='infrared',axes=axes,color='blue',**kwargs)
        optical.loglog(label='optical',axes=axes,color='green',**kwargs)
        photon_fields.loglog(label='sum',axes=axes,color='orange',**kwargs)
        P.legend(loc=3)
        P.savefig('w51C_photon_fields.png')
    plot_photon_fields()

    # Sanity check, calculate energy density of photon fields
    plot_field = lambda i: 'kT=%s, E=%s' % (u.repr(i.kT*u.erg,'eV'), u.repr(i.integrate(e_weight=1),'eV*cm^-3'))
    print 'Photon Fields: \n\tCMB: %s \n\tinfrared: %s \n\toptical: %s' % \
        (plot_field(cmb),plot_field(infrared),plot_field(optical))

    # Create the synchrotron radiation
    synch = Synchrotron(electron_spectrum=electrons,
                        magnetic_field=magnetic_field)

    # Create the inverse compton radiation
    ic = InverseCompton(electron_spectrum=electrons,
                        photon_spectrum=photon_fields)

    # Plot the SED. Try to make a figure like fig 4 from the text
    sed = SEDPlotter(
        emin=9e-7*u.eV, 
        emax=2e12*u.eV,
        distance=distance,
        x_units_string='eV',
        y_units_string='erg*cm^-2*s^-1',
        axes=axes)

    # Overlay the Synchrotron and Inverse Compton radiation
    sed.plot(synch, color='red', label='Synchrotron')
    sed.plot(ic, color='blue', label='Inverse Compton')




def pi0_dominated(axes):
    """ Compute the SED for W51C in the Pi0-decay dominated hypothesis
        (a) in table 1 Fig.4 of the text. """

    electrons = SmoothBrokenPowerLaw(
        total_energy=0.13e50*u.erg,
        index1 = 1.5, # p10 in text
        index2 = 1.5 + 1.4, # index2 = index1 + delta_s
        e_break = 15*u.GeV,
        e_scale = 1*u.GeV,
        beta = 2,
        emin = 10*u.MeV, # from footnote to table 1
        emax = 100*u.TeV,
        )

    protons = SmoothBrokenPowerLaw(
        total_energy=5.2e50*u.erg,
        index1 = 1.5, # p10 in text
        index2 = 1.5 + 1.4, # index2 = index1 + delta_s
        e_break = 15*u.GeV,
        e_scale = 1*u.GeV,
        beta = 2,
        emin = 10*u.MeV, # from footnote to table 1
        emax = 100*u.TeV,
        )

    magnetic_field = 40*u.microgauss # From table 1 in text for (a) Pi0-decay

    distance = 6*u.kiloparsec # from page 8 in text

    target_density = 10*u.cm**-3 # From table 1 for (a) Pi0-decay

    synch = Synchrotron(electron_spectrum=electrons, magnetic_field=magnetic_field)

    pi0 = Pi0Decay(proton_spectrum=protons, 
                   target_density = target_density,
                   scaling_factor = 1.85 # p10 in the text
                  )

    sed = SEDPlotter(
        emin=9e-7*u.eV, 
        emax=2e12*u.eV,
        distance=distance,
        x_units_string='eV',
        y_units_string='erg*cm^-2*s^-1',
        axes=axes,
        )

    # Overlay the Synchrotron and Inverse Compton radiation
    sed.plot(synch, color='red', label='Synchrotron')
    sed.plot(pi0, color='blue', label=r'$\pi^0$ Decay')




fig = P.figure(None,(7,6))
grid=AxesGrid(fig, 111,
              nrows_ncols = (3, 1),
              axes_pad = 0.1,
              aspect=False,
              share_all=True)

# Setup up the axes to be the same as figure 4 in the publiation
for axes in grid:
    axes.xaxis.set_ticks([1e-6,1e-3, 1e-0, 1e3, 1e6, 1e9, 1e12])
    axes.yaxis.set_ticks([1e-12, 1e-11, 1e-10])

    axes.set_xlabel(r'E [eV]')
    axes.set_ylabel(r'$\nu f_\nu$ [erg cm$^{-2}$ s$^{-1}$]')

    axes.set_xscale('log')
    axes.set_yscale('log')

    axes.set_ylim(ymin=2e-13, ymax=2e-10)
    axes.set_xlim(xmin=9e-7, xmax=2e12)

pi0_dominated(grid[0])
ic_dominated(grid[2])


fig.savefig('w51C_sed.png')

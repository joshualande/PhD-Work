""" Compute the SED of W51C using parameters from
    http://arxiv.org/abs/0910.0908

    SED for for hypothesis (c) InverseCompton

    Author: Joshua Lande <joshualande@gmail.com>
"""
import pylab as P

from pysed.sed_particle import SmoothBrokenPowerLaw
from pysed.sed_ic import InverseCompton
from pysed.sed_synch import Synchrotron
from pysed.sed_spectrum import CompositeSpectrum
from pysed.sed_plotting import SEDPlotter
from pysed.sed_thermal import CMB,ThermalSpectrum
import pysed.sed_units as u


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
    filename='w51c_electrons.png')

# From table 1 in text for (c) Inverse Compton
B = 2*u.microgauss

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
    P.savefig('w51c_photon_fields.png')
plot_photon_fields()

# Sanity check, calculate energy density of photon fields
plot_field = lambda i: 'kT=%s, E=%s' % (u.repr(i.kT*u.erg,'eV'), u.repr(i.integrate(e_weight=1),'eV*cm^-3'))
print 'Photon Fields: \n\tCMB: %s \n\tinfrared: %s \n\toptical: %s' % \
    (plot_field(cmb),plot_field(infrared),plot_field(optical))

# Create the synchrotron radiation
synch = Synchrotron(electron_spectrum=electrons,
                    magnetic_field=3e-6*u.gauss)

# Create the inverse compton radiation
ic = InverseCompton(electron_spectrum=electrons,
                    photon_spectrum=photon_fields)

# Plot the SED
sed = SEDPlotter(
    emin=9e-6*u.eV, 
    emax=2e12*u.eV,
    distance=distance,
    x_units_string='eV',
    y_units_string='erg*cm^-2*s^-1',
    figsize=(7,2))

# Overlay the Synchrotron and Inverse Compton radiation
sed.plot(synch, color='red', label='Synchrotron')
sed.plot(ic, color='blue', label='Inverse Compton')

#sed.axes.set_ylim(ymin=2e-13, ymax=2e-10)
sed.save(filename='w51c_sed.png')


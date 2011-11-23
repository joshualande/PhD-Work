""" This module is like sympy.physics.units but defines
    new units and physical constants relevant to astrophysics.

    This module it defined charge and magnetic field in terms of 
    cm, g, and s to be consistent with CGS and typical 
    astrophysics text.

    This mode also defines some helper functions for dealing
    with quantities that have units.
    
    Author: Joshua Lande <joshualande@gmail.com>
"""
import sympy
import sympy.physics
from sympy.physics import units

class UnitsException(Exception): pass

# define new energy units
units.keV = 1e3*units.eV
units.MeV = 1e6*units.eV
units.GeV = 1e9*units.eV
units.TeV = 1e12*units.eV
units.erg = units.g*units.cm**2/units.s**2
units.ph = 1 # photons don't have units =)


# More physical constants
one_half = sympy.sympify('1/2')

units.statcoulomb = units.erg**one_half*units.cm**one_half
units.electron_charge = 4.80320425e-10*units.statcoulomb

units.electron_mass = 9.10938188e-28*units.grams

# 1 Gauss written in terms of cm, g,s is taken from
# http://en.wikipedia.org/wiki/Gaussian_units
units.gauss = units.cm**-one_half*units.g**one_half*units.s**-1
units.microgauss = 1e-6*units.gauss

units.tesla = 1e4*units.gauss

units.pc = units.parsec = 3.08568025e18*units.cm
units.kpc = units.kiloparsec = 1e3*units.parsec

# see http://en.wikipedia.org/wiki/Barn_(unit)
units.barn = 1e-24*units.cm**2
units.millibarn = 1e-3*units.barn

# classical electron radius
units.r0=units.electron_charge**2/(units.electron_mass*units.speed_of_light**2)

# convert from a string to units
fromstring=lambda string: sympy.sympify(string, sympy.physics.units.__dict__)

# Convert numpy array to sympy array with desired units
tosympy=lambda array,units: sympy.Matrix(array)*units

# Convert sympy array to numpy array with desired units.
def tonumpy(array,units):
    try:
        return sympy.list2numpy(array/units).astype(float)
    except:
        raise UnitsException("Unable to convert array %s to units %s." % (array,units))

# Convert from one unit to another
def convert(x, from_units, to_units):
    try:
        return x*float(fromstring(from_units)/fromstring(to_units))
    except:
        raise UnitsException("Unable to convert %s from %s to %s." % (x, from_units, to_units))

# Print out a quanitiy with nice units
repr=lambda value,unit_string,format='%.2e': format % float(value/fromstring(unit_string)) + ' ' + unit_string

from sympy.physics.units import *

"""
    This module is like sympy.physics.units but defines
    new units relevant to astrophysics.
"""
import numpy as np
import sympy
import sympy.physics
from sympy.physics import units

# define new energy units
units.keV = 1e3*units.eV
units.MeV = 1e6*units.eV
units.GeV = 1e9*units.eV
units.TeV = 1e12*units.eV
units.erg = units.g*units.cm**2/units.s**2
units.ph = 1 # photons don't have units


from sympy.physics.units import *


# convenience function
fromstring=lambda string: sympy.sympify(string,locals=sympy.physics.units.__dict__)

# Convert numpy array to sympy array with desired units
tosympy=lambda array,units: sympy.Matrix(array)*units

# Convert sympy array to numpy array with desired units.
tonumpy=lambda array,units: sympy.list2numpy(array/units).astype(float)

# Convert from one unit to another
convert=lambda x, from_units, to_units: x*float(fromstring(from_units)/fromstring(to_units))


# More physical constants
one_half = sympy.sympify('1/2')

statcoulomb = erg**one_half*cm**one_half
electron_charge = 4.80320425e-10*statcoulomb



electron_mass = 9.10938188e-28*grams

# 1 Gauss written in terms of cm, g,s is taken from
# http://en.wikipedia.org/wiki/Gaussian_units
gauss = cm**(-one_half)*g**(one_half)*s**(-1)

tesla = 1e4*gauss

pc = parsec = 3.08568025e18*cm
kpc = 1e3*parsec


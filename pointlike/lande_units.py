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
convert=lambda x, from_units, to_units: float((x*fromstring(from_units))/fromstring(to_units))


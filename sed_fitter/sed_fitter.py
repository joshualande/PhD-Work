""" sed_fitter.py

    Code to compute SEDs. This code differs from other SED packages in
    valuing human readability over computational efficiency. 


    Notes: 
        * R&L is Rybicki and Lightman "Radiative Processes in Astrophysics


    This file is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Author: Joshua Lande
"""

import math
from abc import abstractmethod

import pylab as P
import numpy as np
from sed_integrate import logsimps
from scipy import integrate
from scipy import special

import sympy

import lande_units as u


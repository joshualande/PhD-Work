#!/usr/bin/env python
from os.path import expandvars,join

import pylab as P

from uw.utilities.makerec import fitsrec

recname = expandvars(join('$fitdiffdata','v1','cached.fits'))

r = fitsrec(recname)

print r['galnorm']
print r['galnorm_err']
print r['isonorm']
print r['isonorm_err']

print r['difftype']
print r['location']

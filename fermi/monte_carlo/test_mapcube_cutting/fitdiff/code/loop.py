#!/usr/bin/env python
from collections import OrderedDict
from lande.utilities.simbuilder import SimBuilder

params=OrderedDict()
params['difftype']=['galactic', 'isotropic', 'sreekumar']
params['location']=['highlat','lowlat', 'galcenter']
params[('emin','emax')]=[[1e2,1e5],[1e4,1e5]]

j = SimBuilder(savedir='$fitdiffdata/v8',
               code='$fitdiffcode/simulate.py',
               num=10,
               params=params)
j.build()

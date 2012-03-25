#!/usr/bin/env python
from collections import OrderedDict
from lande.utilities.simtools import SimBuilder

# version 1 - new
# version 2 - Primary difference: 8bins per decade
# version 3 - Primary difference: gtlike, new sreekumar code
# version 4: Primary difference: fix l,b cut
# version 5: Primary difference: diffuse_pad=10, energy_pad=2
# version 6: Primary difference: ?
# version 7: Primary difference: ?
#params=OrderedDict()
#params['difftype']=['galactic', 'isotropic', 'sreekumar']
#params['location']=['highlat','lowlat', 'galcenter']
#params[('emin','emax')]=[[1e2,1e5],[1e4,1e5]]
#
#j = SimBuilder(savedir='$fitdiffdata/v8',
#               code='$fitdiffcode/simulate.py',
#               num=10,
#               params=params)
#j.build()


# version 8: 
#params=OrderedDict()
#params['difftype']=['sreekumar']
#params['position']=['allsky']
#params['time']=['2fgl']
#params[('emin','emax')]=[[1e2,1e5]]
#
#j = SimBuilder(savedir='$fitdiffdata/v8',
#               code='$fitdiffcode/simulate.py',
#               num=10,
#               params=params)
#j.build()

# version 9: unbinned
params=OrderedDict()
params['difftype']=['galactic', 'isotropic', 'sreekumar']
params['position']=['highlat','lowlat', 'galcenter']
params[('emin','emax')]=[[1e2,1e5],[1e4,1e5]]
params['time']=['2fgl']

j = SimBuilder(savedir='$fitdiffdata/v9',
               code='$fitdiffcode/simulate.py',
               num=10,
               params=params)
j.build()

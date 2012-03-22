from lande.utilities.simtools import SimBuilder
from collections import OrderedDict

#params=OrderedDict()
#params['time']=['1day']
#params['flux']=[1e-2, 1e-3]
#params['position']=['allsky']
#params['emin']=[1e2]
#params['emax']=[1e5]
#
#b = SimBuilder(
#    savedir='$simpsdata/v1',
#    code='$simpscode/simulate.py',
#    num=100,
#    params=params)
#b.build()


# v2
#params=OrderedDict()
##params[('time','flux')]=[('1day',1e-2), ('2years',1e-4), ('2fgl',1e-4)]
#params['time']=['1day']
#params['flux']=[1e-2]
#params['position']=['allsky']
#params['emin']=[1e2]
#params['emax']=[1e5]
#
#b = SimBuilder(
#    savedir='$simpsdata/v2',
#    code='$simpscode/simulate.py',
#    num=100,
#    params=params)
#b.build()


# v3
b = SimBuilder(
    savedir='$simpsdata/v3',
    code='$simpscode/simulate.py',
    num=100,
    params=dict(time='1day', flux=1e-2, position='allsky', 1e2, 1e5))
b.build()

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
#b = SimBuilder(
#    savedir='$simpsdata/v3',
#    code='$simpscode/simulate.py',
#    num=1000,
#    params=dict(time='1day', flux=1e-2, position='allsky', emin=1e2, emax=1e5))
#b.build()

# v4
#b = SimBuilder(
#    savedir='$simpsdata/v4',
#    code='$simpscode/simulate.py',
#    num=1000,
#    params=dict(time='1day', flux=1e-2, position='allsky', emin=1e2, emax=1e5, phibins=[0,5,9]))
#b.build()

# v5
#b = SimBuilder(
#    savedir='$simpsdata/v5',
#    code='$simpscode/simulate.py',
#    num=100,
#    params=dict(time='1day', flux=1e-2, position='allsky', emin=1e2, emax=1e5, phibins=[0,9]))
#b.build()

# v6
#b = SimBuilder(
#    savedir='$simpsdata/v6',
#    code='$simpscode/simulate.py',
#    num=1000,
#    #params=dict(time='1day', flux=1e-2, position=['galcenter', 'pole', 'bad'], emin=1e2, emax=1e5, phibins=[0,9]))
#    params=dict(time='1day', flux=1e-2, position=['allsky'], emin=1e2, emax=1e5, phibins=9))
#b.build()

# v7 - try unbinned
#b = SimBuilder(
#    savedir='$simpsdata/v7',
#    code='$simpscode/simulate.py',
#    num=100,
#    params=dict(time='1day', flux=1e-2, position=['allsky'], emin=1e2, emax=1e5, phibins=9),
#    extra='--savedata')
#b.build()

# v8 - in ltcube generation, dcostheta=0.025, binsz=0.25
#b = SimBuilder(
#    savedir='$simpsdata/v8',
#    code='$simpscode/simulate.py',
#    num=100,
#    params=dict(time='1day', flux=1e-2, position=['allsky'], emin=1e2, emax=1e5, phibins=9),
#    )
#b.build()

# v9 - binned, regular ltcube, galactic coordsystem
#b = SimBuilder(
#    savedir='$simpsdata/v9',
#    code='$simpscode/simulate.py',
#    num=100,
#    params=dict(time='1day', flux=1e-2, position=['allsky'], emin=1e2, emax=1e5, phibins=9),
#    )
#b.build()

# v10 - Using HEAD version of science tools
#b = SimBuilder(
#    savedir='$simpsdata/v10',
#    code='$simpscode/simulate.py',
#    num=100,
#    params=dict(time='1day', flux=1e-2, position=['allsky'], emin=1e2, emax=1e5, phibins=9),
#    )
#b.build()

# v11 - Using HEAD version of science tools, point+extended source, smaller flux
# note, 2 years/1 day=730
b = SimBuilder(
    savedir='$simpsdata/v11',
    code='$simpscode/simulate.py',
    num=100,
    params=dict(time='2fgl', flux=[1e-6], position=['allsky'], emin=1e2, emax=1e5, phibins=0, spatial=['point','extended']),
    )
b.build()

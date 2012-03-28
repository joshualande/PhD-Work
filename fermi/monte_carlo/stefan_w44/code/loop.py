from lande.utilities.simtools import SimBuilder

params=dict(spectrum=[ 'SmoothBrokenPowerLaw', 'DoubleBrokenSmoothPowerlaw'])
j = SimBuilder(savedir='$stefan_w44_data/v1',
               code='$stefan_w44_code/simulate.py',
               num=10,
               params=params)
j.build()


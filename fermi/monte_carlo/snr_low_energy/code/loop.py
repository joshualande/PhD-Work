
from lande.utilities.jobtools import JobBuilder

# v1
#params=dict(name=['IC443','W44','W51C'])
#params['conv-type']=[0,-1,1]
#
#b=JobBuilder(
#    params=params,
#    savedir='$snr_low_energy_data/v1',
#    code='$snr_low_energy_code/analysis.py')
#b.build()



params=dict(name=['IC443','W44','W51C'], test=True)
params['conv-type']=0

b=JobBuilder(
    params=params,
    savedir='$snr_low_energy_data/test2',
    code='$snr_low_energy_code/analysis.py')
b.build()


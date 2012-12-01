from os.path import join
from textwrap import dedent
from itertools import product

from lande.utilities.save import loaddict

from lande.fermi.pipeline.pwncat2.analysis.builder import PipelineBuilder

####################################################################################################

"""
radiopsr_data='$gamma_quiet_psrs_data/gamma_quiet_psrs_data.yaml'
names=loaddict(radiopsr_data).keys()
bigfile='$lat2pc/BigFile/Pulsars_BigFile_v20121002103223.fits'

params=dict(name=names, 
            bigfile=bigfile)
params['radiopsr-data']=radiopsr_data
b = PipelineBuilder(
    savedir='$gamma_quiet_psrs_analysis/v1/fits',
    code='$gamma_quiet_psrs_pipeline/main.py',
    params=params,
    short_folder_names=True,
)
b.build()
b.build_followup(
    code = '$gamma_quiet_psrs_pipeline/followup.py',
    hypotheses=['at_pulsar','point','extended'],
    followups=['gtlike','plots','tsmaps']
)
"""

####################################################################################################

radiopsr_data='$gamma_quiet_psrs_data/gamma_quiet_psrs_data.yaml'
names=loaddict(radiopsr_data).keys()
bigfile='$lat2pc/BigFile/Pulsars_BigFile_v20121127171828.fits'

params=dict(name=names, 
            bigfile=bigfile)
params['no-point']=True
params['no-extended']=True
params['radiopsr-data']=radiopsr_data
b = PipelineBuilder(
    savedir='$gamma_quiet_psrs_analysis/v2/fits',
    code='$gamma_quiet_psrs_pipeline/main.py',
    params=params,
    short_folder_names=True,
)
b.build()
b.build_followup(
    code = '$gamma_quiet_psrs_pipeline/followup.py',
    hypotheses=['at_pulsar'],
    followups=['gtlike','plots','tsmaps']
)

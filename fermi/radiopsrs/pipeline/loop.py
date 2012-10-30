
from lande.utilities.save import loaddict
from lande.utilities.jobtools import JobBuilder

radiopsr_data='$radiopsrs_data/radiopsrs_data.yaml'
names=loaddict(radiopsr_data).keys()
bigfile='$lat2pc/BigFile/Pulsars_BigFile_v20121002103223.fits'

params=dict(name=names, 
            bigfile=bigfile)
params['radiopsr-data']=radiopsr_data
b = JobBuilder(
    savedir='$radiopsrs_analysis/v1',
    code='$radiopsrs_pipeline/main.py',
    params=params,
    short_folder_names=True,
    )
b.build()


from lande.utilities.save import loaddict
from lande.utilities.jobtools import JobBuilder

superfile='$superfile/snrdata.yaml'

snrs=loaddict(superfile).keys()
params=dict(name=snrs,
            snrdata='$superfile/snrdata.yaml',
            latdata='$snrlimcode/snrlatdata.yaml')


b = JobBuilder(
    savedir='$snrlimdata/v1',
    params=params,
    code='$snrlimcode/run.py',
    short_folder_names=True)
b.build()

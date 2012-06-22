import yaml
from os.path import expandvars
from lande.utilities.jobtools import JobBuilder

"""
pwndata='$pwncode/pwndata/pwncat2_data_lande.yaml'
names=yaml.load(open(expandvars(pwndata))).keys()
params=dict(pwncat1phase="$pwncode/pwndata/pwncat1_phase.yaml",
            pwndata=pwndata,
            name=names)

b = JobBuilder(
    savedir='$pwndata/off_peak/off_peak_bb/pwncat2/v5/analysis',
    code='$pwncode/lande/off_peak/off_peak_bb.py',
    params=params,
    short_folder_names=True)
b.build()
"""


pwndata='$pwncode/pwndata/pwncat2_data_lande.yaml'
names=yaml.load(open(expandvars(pwndata))).keys()
params=dict(pwncat1phase="$pwncode/pwndata/pwncat1_phase.yaml",
            pwndata=pwndata,
            name=names)

b = JobBuilder(
    savedir='$pwndata/off_peak/off_peak_bb/pwncat2/v6/analysis',
    code='$pwncode/lande/off_peak/off_peak_bb.py',
    params=params,
    short_folder_names=True)
b.build()

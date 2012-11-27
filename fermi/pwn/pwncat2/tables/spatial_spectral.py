from lande.fermi.pipeline.pwncat2.table.spatial_spectral import spatial_spectral_table

from lande.utilities.table import get_table_type
table_type=get_table_type()

spatial_spectral_table(
    pwndata='$pwndata/pwncat2_data_lande.yaml',
    phase_shift='/nfs/farm/g/glast/u55/pulsar/2ndPulsarcatalog/psue/General/josh_dicts.pickle',
    fitdir='$pwnpipeline/v36/analysis',
    savedir='$pwnpipeline/v36/tables',
    filebase='off_peak_spatial_spectral',
    table_type=table_type,
    pwn_classification='$pwnclassify/manual_classifications.yaml',
    bigfile_filename='$lat2pc/BigFile/Pulsars_BigFile_v20121108102909.fits')

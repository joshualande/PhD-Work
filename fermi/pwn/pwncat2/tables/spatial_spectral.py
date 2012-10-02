from lande.fermi.pipeline.pwncat2.table.spatial_spectral import spatial_spectral_table

from lande.utilities.table import get_table_type
table_type=get_table_type()

spatial_spectral_table(
    pwndata='$pwndata/pwncat2_data_lande.yaml',
    phase_shift='/u/gl/kerrm/pulsar/share/python/checklist.py',
    fitdir='$pwnpipeline/v35/analysis',
    savedir='$pwnpipeline/v35/tables',
    filebase='off_peak_spatial_spectral',
    table_type=table_type,
    pwn_classification='$pwnclassify/manual_classifications.yaml',
)

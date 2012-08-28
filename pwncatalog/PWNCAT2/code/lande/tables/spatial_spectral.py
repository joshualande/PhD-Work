from lande.pipeline.pwncat2.table.spatial_spectral import spatial_spectral_table

from lande.utilities.table import get_table_type
table_type=get_table_type()

spatial_spectral_table(
    pwndata='$pwncode/data/pwncat2_data_lande.yaml',
    fitdir='$pwndata/spectral/v29/analysis',
    savedir='$pwndata/spectral/v29/tables',
    filebase='off_peak_spatial_spectral',
    table_type=table_type,
    pwn_classification='$pwndata/spectral/v29/classify/automatic_classifications.yaml',
)

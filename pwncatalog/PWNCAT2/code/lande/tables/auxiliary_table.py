from lande.pipeline.pwncat2.table.auxiliary import auxiliary_table

auxiliary_table(
    pwndata='$pwncode/data/pwncat2_data_lande.yaml',
    fitdir='$pwndata/spectral/v29/analysis',
    filename='$pwndata/spectral/v29/tables/auxiliary_table.fits',
    pwn_classification='$pwndata/spectral/v29/classify/automatic_classifications.yaml',
)

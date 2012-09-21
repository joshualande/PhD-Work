from lande.fermi.pipeline.pwncat2.table.auxiliary import auxiliary_table

"""
auxiliary_table(
    pwndata='$pwncode/data/pwncat2_data_lande.yaml',
    fitdir='$pwndata/spectral/v29/analysis',
    filename='$pwndata/spectral/v29/tables/auxiliary_table.fits',
    pwn_classification='$pwndata/spectral/v29/classify/automatic_classifications.yaml',
)
"""

auxiliary_table(
    pwndata='$pwndata/pwncat2_data_lande.yaml',
    pwnphase='$pwndata/pwncat2_phase_lande.yaml',
    fitdir='$pwnpipeline/v35/analysis',
    filename='$pwnpipeline/v35/tables/auxiliary_table.fits',
    pwn_classification='$pwnclassify/manual_classifications.yaml'
)

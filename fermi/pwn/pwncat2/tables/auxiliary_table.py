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
    phase_shift='/nfs/farm/g/glast/u55/pulsar/2ndPulsarcatalog/psue/General/josh_dicts.pickle',
    fitdir='$pwnpipeline/v37/analysis',
    filename='$pwnpipeline/v37/tables/off_peak_auxiliary_table.fits',
    pwn_classification='$pwnclassify/manual_classifications.yaml'
)

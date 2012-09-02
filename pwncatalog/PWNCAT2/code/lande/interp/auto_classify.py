from lande.utilities.save import savedict
from lande.fermi.pipeline.pwncat2.interp.classify import auto_classify

classifications=auto_classify(pwndata='$pwncode/data/pwncat2_data_lande.yaml', 
                              fitdir='$pwndata/spectral/v29/analysis/')

savedict('$pwndata/spectral/v29/classify/automatic_classifications.yaml',
         classifications,
         yaml_kwargs=dict(default_flow_style=False))

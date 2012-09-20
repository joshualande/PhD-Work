from lande.pipeline.pwncat2.interp.classify import auto_classify
from lande.utilities.save import savedict

pwndata="$pwncode/data/pwncat2_data_lande.yaml"
fitdir='$pwndata/spectral/v29/analysis'
c=auto_classify(pwndata, fitdir)
savedict(c,'$pwndata/spectral/v29/classify/automatic_classifications.yaml')

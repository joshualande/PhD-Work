from lande.fermi.pipeline.pwncat2.interp.classify import auto_classify, make_manual_classify
from lande.utilities.save import savedict

"""
pwndata="$pwndata/pwncat2_data_lande.yaml"
fitdir='$pwnpipeline/v35/analysis'
c=auto_classify(pwndata, fitdir)
savedict(c,'$pwnpipeline/v35/classify/automatic_classifications.yaml')
"""

#import sys;sys.exit(1)
c=make_manual_classify(
    pwndata="$pwndata/pwncat2_data_lande.yaml", 
    fitdir='$pwnpipeline/v35/analysis'
)
savedict(c,'$pwnclassify/v35/manual_classifications.yaml')

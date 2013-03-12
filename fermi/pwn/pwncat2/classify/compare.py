from lande.fermi.pipeline.pwncat2.interp.classify import compare_classifications

pwndata="$pwndata/pwncat2_data_lande.yaml"
fitdir='$pwnpipeline/v37/analysis'
pwn_classification='$pwnclassify/manual_classifications.yaml'
compare_classifications(pwndata,fitdir,pwn_classification)

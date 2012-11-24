from lande.fermi.pipeline.pwncat2.interp.classify import PWNAutomaticClassifier
from lande.utilities.save import savedict

if True:
    """
    pwndata="$pwndata/pwncat2_data_lande.yaml"
    fitdir='$pwnpipeline/v35/analysis'
    c=PWNAutomaticClassifier.get_automatic_classify(pwndata, fitdir)
    print c
    savedict(c,'$pwnpipeline/v35/classify/automatic_classifications.yaml')
    """

    pwndata="$pwndata/pwncat2_data_lande.yaml"
    fitdir='$pwnpipeline/v36/analysis'
    c=PWNAutomaticClassifier.get_automatic_classify(pwndata, fitdir)
    print c
    savedict(c,'$pwnpipeline/v36/classify/automatic_classifications.yaml')


if False:
    pass
    """
    # don't run again
    c=make_manual_classify(
        pwndata="$pwndata/pwncat2_data_lande.yaml", 
        fitdir='$pwnpipeline/v35/analysis')
    savedict(c,'$pwnclassify/manual_classifications.yaml')
    """


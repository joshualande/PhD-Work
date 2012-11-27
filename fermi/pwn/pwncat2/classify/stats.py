import numpy as np

from lande.fermi.pipeline.pwncat2.interp.classify import PWNManualClassifier,PWNClassifierException
from lande.fermi.pipeline.pwncat2.interp.loader import PWNResultsLoader

loader = PWNResultsLoader(
    pwndata="$pwndata/pwncat2_data_lande.yaml",
    fitdir="$pwnpipeline/v35/analysis"
)
print loader.pwndata
print loader.fitdir

pwnlist = loader.get_pwnlist()

classifier=PWNManualClassifier(
    loader=loader, 
    pwn_classification='$pwnclassify/manual_classifications.yaml'
)

npsr = 0
psrs = []

npwn = 0
pwne = []

ndetect = 0

nconfused = 0
confused = []

n_actually_extended = 0

n_formally_extended = 0
formally_extended = []

n_formally_extended_pulsars = 0
formally_extended_pulsars = []


n_formally_extended_confused = 0
formally_extended_confused = []

all_tsvar = []

for pwn in pwnlist:
    try:
        c = classifier.get_classification(pwn)

        res = classifier.get_results(pwn)

        all_tsvar.append(res['ts_var'])

        if c['spatial_model'] == 'Extended':
            n_actually_extended +=1

        if 'ts_ext' in res and res['ts_ext'] >= 16:
            n_formally_extended +=1
            formally_extended.append(pwn)

            if c['source_class'] == 'Pulsar':
                n_formally_extended_pulsars +=1
                formally_extended_pulsars.append(pwn)

            if c['source_class'] == 'Confused':
                n_formally_extended_confused +=1
                formally_extended_confused.append(pwn)

        if c['source_class'] == 'Pulsar':
            npsr += 1
            ndetect += 1
            psrs.append(pwn)
        elif c['source_class'] == 'PWN':
            npwn += 1
            ndetect += 1
            pwne.append(pwn)
        elif c['source_class'] == 'Confused':
            nconfused += 1
            ndetect += 1
            confused.append(pwn)
        elif c['source_class'] == 'Upper_Limit':
            pass
        else:
            raise Exception()

    except PWNClassifierException:
        print 'Skipping %s' % pwn

print 'Number of pulsars = %s' % npsr
print 'Pulsars', psrs

print 'Number of PWNe = %s' % npwn
print 'PWNe', pwne

print 'Number of UNIDs = %s' % nconfused
print 'UNID', confused

print 'Number of Detected = %s' % ndetect
print 'Number of Actually Extended = %s' % n_actually_extended

print 'Number of Formally Extended = %s' % n_formally_extended
print 'Formally Extended = ', formally_extended

print 'Number of Formally Extended Pulsars = %s' % n_formally_extended_pulsars
print 'Formally Extended Pulsars = ', formally_extended_pulsars

print 'Number of Formally Extended Confused = %s' % n_formally_extended_confused
print 'Formally Extended Confused = ', formally_extended_confused


print 'ALL TS_Var',np.sort(all_tsvar).tolist()

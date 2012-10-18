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
n_should_be_extended = 0
should_be_extended = []

for pwn in pwnlist:
    try:
        c = classifier.get_classification(pwn)

        res = classifier.get_results(pwn)

        if c['spatial_model'] == 'Extended':
            n_actually_extended +=1

        if 'ts_ext' in res and res['ts_ext'] >= 16:
            n_should_be_extended +=1
            should_be_extended.append(pwn)

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
print 'Number of Should Be Extended = %s' % n_should_be_extended
print 'Should Be Extended = ', should_be_extended



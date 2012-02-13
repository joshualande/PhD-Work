import yaml
from os.path import expandvars, join, exists

# useful discussion of TSvar
#   https://confluence.slac.stanford.edu/display/SCIGRPS/How+to+-+Variability+test

pwnlist = yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_data_lande.yaml')))

def get_ts_var():
    folder = '/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/spectral/v10/variability/v3'

    ts_var = []
    for pwn in pwnlist.keys():

        results = join(folder,pwn,'results_%s.yaml' % pwn)

        assert exists(results)

        f=yaml.load(open(results))

        ts_var.append(f['TS_var']['gtlike'])

    return ts_var

#def get_ts_point():
#    folder = '/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/spectral/v10/analysis_plots/'
#
#    ts_point = []
#    for pwn in pwnlist.keys():
#
#        results = join(folder,pwn,'results_%s.yaml' % pwn)
#
#        assert exists(results)
#
#        f=yaml.load(open(results))
#        print pwn,f['at_pulsar']['gtlike'],f['at_pulsar']['gtlike']['TS']
#
#        ts_point.append(f['at_pulsar']['gtlike']['TS'])
#

ts_var = get_ts_var()
#ts_point = get_ts_point()

d = dict(
#    ts_point=ts_point
    ts_var=ts_var
    )

open('ts_var.yaml','w').write(
    yaml.dump(d)
)


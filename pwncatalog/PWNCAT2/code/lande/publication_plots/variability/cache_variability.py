import yaml
from os.path import expandvars, join, exists

# useful discussion of TSvar
#   https://confluence.slac.stanford.edu/display/SCIGRPS/How+to+-+Variability+test

pwnlist = yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_data_lande.yaml')))

folder = '/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/spectral/v13/variability/v1'

def get_ts():
    ts_point = []
    ts_var = []
    for pwn in pwnlist.keys():

        results = join(folder,pwn,'results_%s.yaml' % pwn)

        assert exists(results)

        f=yaml.load(open(results))

        ts_var.append(f['TS_var']['gtlike'])
        ts_point.append(f['all_time']['gtlike']['TS'])

    return ts_point,ts_var


ts_point,ts_var = get_ts()

d = dict(
    ts_point=ts_point,
    ts_var=ts_var,
    )

open('ts_var.yaml','w').write(
    yaml.dump(d)
)


import yaml
from os.path import expandvars, join, exists
from lande.utilities.save import savedict

# useful discussion of TSvar
#   https://confluence.slac.stanford.edu/display/SCIGRPS/How+to+-+Variability+test

pwnlist = yaml.load(open(expandvars('$pwncode/data/pwncat2_data_lande.yaml')))

base = '$pwndata/spectral/v24/'
folder = expandvars(join(base, 'analysis'))
outdir = expandvars(join(base, 'plots'))

def get_ts():
    ts_point = []
    ts_var = []
    names = []
    for pwn in pwnlist.keys():

        var_results = join(folder,pwn, 'results_%s_variability_point.yaml' % pwn)
        gtlike_results = join(folder,pwn, 'results_%s_gtlike_point.yaml' % pwn)

        if not exists(var_results) or not exists(gtlike_results): 
            print "Skipping %s b/c results doesn't exist" % pwn
            continue
        else:
            print pwn

        f=yaml.load(open(var_results))
        g=yaml.load(open(gtlike_results))

        ts_var.append(f['point']['variability']['TS_var']['gtlike'])
        ts_point.append(g['point']['gtlike']['TS'])
        names.append(pwn)

    return ts_point,ts_var,names


ts_point,ts_var,names = get_ts()

d = dict(
    ts_point=ts_point,
    ts_var=ts_var,
    pwn=names,
    )

savedict(d,join(outdir,'ts_var.yaml'))

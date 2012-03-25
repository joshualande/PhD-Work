from os.path import join, expandvars
from glob import glob
from collections import defaultdict

import yaml

from lande.utilities.save import savedict

savedir = expandvars(join('$w44simdata/','v7'))

results = defaultdict(list)

all_results=glob(join(savedir,'*','results_*.yaml'))
l = len(all_results)

all_h = [ 'Point', 'Disk', 'Gaussian', 'EllipticalDisk', 'EllipticalRing' ]
for i,r in enumerate(all_results):
    if i%10==0: print '%s/%s' % (i,l)

    x = yaml.load(open(r))

    def all_good():
        for h in all_h:
            if not h in x.keys():
                return False
        return True
    if not all_good(): continue

    for h in all_h:
        results['ll_%s' % h].append(x[h]['gtlike']['logLikelihood'])
        results['TS_%s' % h].append(x[h]['gtlike']['TS'])
        results['flux_%s' % h].append(x[h]['gtlike']['flux']['flux'])
        results['index_%s' % h].append(x[h]['gtlike']['model']['Index'])

        if h is not 'Point': results['r68_%s' % h].append(x[h]['pointlike']['spatial_model']['r68'])

    results['ll_mc'].append(x['mc']['logLikelihood'])
    results['TS_mc'].append(x['mc']['TS'])
    results['flux_mc'].append(x['mc']['flux']['flux'])
    results['index_mc'].append(-x['mc']['model']['Index'])
    results['r68_mc'].append(x['mc']['spatial_model']['r68'])

savename = join(savedir,'merged.hdf5')
savedict(results, savename)


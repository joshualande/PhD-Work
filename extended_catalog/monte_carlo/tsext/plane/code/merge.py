from os.path import join, expandvars
from glob import glob
from collections import defaultdict

        
import yaml
from numpy.core.records import fromarrays
from uw.utilities.makerec import makefits

savedir = expandvars(join('$tsext_plane_data/','v1'))

results = defaultdict(list)

all_results=glob(join(savedir,'*','results_*.yaml'))
l = len(all_results)

for i,r in enumerate(all_results):
    if i%10==0: print '%s/%s' % (i,l)

    x = yaml.load(open(r))

    for y in x:
        results['TS_point'].append(y['point']['TS'])
        results['TS_ext'].append(y['extended']['ts_ext'])
        results['flux'].append(y['mc']['flux']['flux'])
        results['index'].append(y['mc']['model']['Index'])


rec = fromarrays(results.values(), names=results.keys())

savename = join(savedir,'merged.fits')
makefits(rec, savename, clobber=True)

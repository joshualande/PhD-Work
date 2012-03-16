from os.path import join, expandvars
from glob import glob
from collections import defaultdict
        
import h5py
import yaml

from lande.utilities.save import savedict

savedir = expandvars(join('$tsext_plane_data/','v5'))

results = defaultdict(list)

all_results=glob(join(savedir,'*','results_*.yaml'))
l = len(all_results)

for i,r in enumerate(all_results):
    if i%10==0: print '%s/%s' % (i,l)

    x = yaml.load(open(r))

    if x is not None:
        for y in x:
            results['TS_point'].append(y['point']['TS'])
            results['TS_ext'].append(y['extended']['TS_ext'])
            results['flux'].append(y['mc']['flux']['flux'])
            results['index'].append(y['mc']['model']['Index'])

savename = join(savedir,'merged.hdf5')
savedict(results, savename)

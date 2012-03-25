from os.path import join, expandvars
from glob import glob
from collections import defaultdict
import numpy as np

import yaml

from lande.utilities.save import savedict

savedir = expandvars(join('$fitdiffdata','v7'))


results = defaultdict(list)

all_results=glob(join(savedir,'*','*','results_*.yaml'))
s=len(all_results)

for i,r in enumerate(all_results):
    if i % 10==0: print '%s/%s' % (i,s)

    x = yaml.load(open(r))

    if x is None: continue

    results['difftype'].append(x['difftype'])
    results['location'].append(x['location'])
    results['pointing'].append(x['pointing'])

    results['l'].append(x['roi_dir']['gal'][0])
    results['b'].append(x['roi_dir']['gal'][1])

    results['emin'].append(x['emin'])
    results['emax'].append(x['emax'])

    p = x['pointlike']
    g = x['gtlike']

    diff = p['fit']

    if diff.has_key('isotrop_2year_P76_source_v0.txt') and \
       diff.has_key('ring_2year_P76_v0.fits'):

        results['pointlike_norm'].append(p['fit']['ring_2year_P76_v0.fits']['Scale'])
        results['pointlike_norm_err'].append(p['fit']['ring_2year_P76_v0.fits']['Scale_err'])
        results['pointlike_norm_mc'].append(p['mc']['ring_2year_P76_v0.fits']['Scale'])

        results['gtlike_norm'].append(g['fit']['ring_2year_P76_v0.fits']['Value'])
        results['gtlike_norm_err'].append(g['fit']['ring_2year_P76_v0.fits']['Value_err'])
        results['gtlike_norm_mc'].append(g['mc']['ring_2year_P76_v0.fits']['Value'])

    elif diff.has_key('isotrop_2year_P76_source_v0.txt'):

        results['pointlike_norm'].append(p['fit']['isotrop_2year_P76_source_v0.txt']['Scale'])
        results['pointlike_norm_err'].append(p['fit']['isotrop_2year_P76_source_v0.txt']['Scale_err'])
        results['pointlike_norm_mc'].append(p['mc']['isotrop_2year_P76_source_v0.txt']['Scale'])

        results['gtlike_norm'].append(g['fit']['isotrop_2year_P76_source_v0.txt']['Normalization'])
        results['gtlike_norm_err'].append(g['fit']['isotrop_2year_P76_source_v0.txt']['Normalization_err'])
        results['gtlike_norm_mc'].append(g['mc']['isotrop_2year_P76_source_v0.txt']['Normalization'])

    elif diff.has_key('Sreekumar Isotropic'):
        results['pointlike_norm'].append(p['fit']['Sreekumar Isotropic']['Norm'])
        results['pointlike_norm_err'].append(p['fit']['Sreekumar Isotropic']['Norm_err'])
        results['pointlike_norm_mc'].append(p['mc']['Sreekumar Isotropic']['Norm'])

        results['gtlike_norm'].append(g['fit']['Sreekumar Isotropic']['Prefactor'])
        results['gtlike_norm_err'].append(g['fit']['Sreekumar Isotropic']['Prefactor_err'])
        results['gtlike_norm_mc'].append(g['mc']['Sreekumar Isotropic']['Prefactor'])

    else:
        print x
        raise Exception("...")

savename = join(savedir,'cached.hdf5')
savedict(results, savename)

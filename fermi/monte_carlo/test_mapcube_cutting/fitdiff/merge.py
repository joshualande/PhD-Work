from os.path import join, expandvars
from glob import glob
from collections import defaultdict
import numpy as np

from numpy.core.records import fromarrays
import yaml

from uw.utilities.makerec import makefits

savedir = expandvars(join('$fitdiffdata','v5'))


results = defaultdict(list)

all_results=glob(join(savedir,'*','*','results_*.yaml'))
s=len(all_results)

for i,r in enumerate(all_results):
    if i % 10==0: print '%s/%s' % (i,s)

    x = yaml.load(open(r))

    results['difftype'].append(x['difftype'])
    results['location'].append(x['location'])
    results['l'].append(x['roi_dir']['gal'][0])
    results['b'].append(x['roi_dir']['gal'][1])

    results['emin'].append(x['emin'])
    results['emax'].append(x['emax'])

    p = x['pointlike']
    g = x['gtlike']

    diff = p['diffuse']

    if diff.has_key('isotrop_2year_P76_source_v0.txt') and \
       diff.has_key('ring_2year_P76_v0.fits'):

        results['pointlike_norm'].append(p['diffuse']['ring_2year_P76_v0.fits']['Scale'])
        results['pointlike_norm_err'].append(p['diffuse']['ring_2year_P76_v0.fits']['Scale_err'])
        results['pointlike_norm_mc'].append(p['mc']['ring_2year_P76_v0.fits']['Scale'])

        results['gtlike_norm'].append(g['diffuse']['ring_2year_P76_v0.fits']['Value'])
        results['gtlike_norm_err'].append(g['diffuse']['ring_2year_P76_v0.fits']['Value_err'])
        results['gtlike_norm_mc'].append(g['mc']['ring_2year_P76_v0.fits']['Value'])

    elif diff.has_key('isotrop_2year_P76_source_v0.txt'):

        results['pointlike_norm'].append(p['diffuse']['isotrop_2year_P76_source_v0.txt']['Scale'])
        results['pointlike_norm_err'].append(p['diffuse']['isotrop_2year_P76_source_v0.txt']['Scale_err'])
        results['pointlike_norm_mc'].append(p['mc']['isotrop_2year_P76_source_v0.txt']['Scale'])

        results['gtlike_norm'].append(g['diffuse']['isotrop_2year_P76_source_v0.txt']['Normalization'])
        results['gtlike_norm_err'].append(g['diffuse']['isotrop_2year_P76_source_v0.txt']['Normalization_err'])
        results['gtlike_norm_mc'].append(g['mc']['isotrop_2year_P76_source_v0.txt']['Normalization'])

    elif diff.has_key('Sreekumar Isotropic'):
        results['pointlike_norm'].append(p['diffuse']['Sreekumar Isotropic']['Norm'])
        results['pointlike_norm_err'].append(p['diffuse']['Sreekumar Isotropic']['Norm_err'])
        results['pointlike_norm_mc'].append(p['mc']['Sreekumar Isotropic']['Norm'])

        results['gtlike_norm'].append(g['diffuse']['Sreekumar Isotropic']['Prefactor'])
        results['gtlike_norm_err'].append(g['diffuse']['Sreekumar Isotropic']['Prefactor_err'])
        results['gtlike_norm_mc'].append(g['mc']['Sreekumar Isotropic']['Prefactor'])

    else:
        print x
        raise Exception("...")



rec = fromarrays(results.values(), names=results.keys())

savename = join(savedir,'cached.fits')
makefits(rec, savename, clobber=True)

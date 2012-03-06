from os.path import join, expandvars
from glob import iglob
from collections import defaultdict
import numpy as np

from numpy.core.records import fromarrays
import yaml

from uw.utilities.makerec import makefits

savedir = expandvars(join('$fitdiffdata','v2'))


results = defaultdict(list)

all_results=iglob(join(savedir,'*','*','results_*.yaml'))

for i,r in enumerate(all_results):
    if i % 10==0: print i

    x = yaml.load(open(r))

    results['difftype'].append(x['difftype'])
    results['location'].append(x['location'])
    results['l'].append(x['roi_dir']['gal'][0])
    results['b'].append(x['roi_dir']['gal'][1])

    results['emin'].append(x['emin'])
    results['emax'].append(x['emax'])

    diff = x['diffuse']
    if diff.has_key('Isotropic Diffuse (isotrop_2year_P76_source_v0.txt)') and \
       diff.has_key('Galactic Diffuse (ring_2year_P76_v0.fits)'):
        gal=diff['Galactic Diffuse (ring_2year_P76_v0.fits)']
        iso=diff['Isotropic Diffuse (isotrop_2year_P76_source_v0.txt)']

    elif diff.has_key('isotrop_2year_P76_source_v0.txt'):
        iso=diff['isotrop_2year_P76_source_v0.txt']
        gal=None

    elif diff.has_key('Sreekumar Isotropic'):
        iso = diff['Sreekumar Isotropic']
        gal = None
    else:
        print x
        raise Exception("...")


    results['galnorm'].append(gal['Norm'] if gal is not None else np.nan)
    results['galnorm_err'].append(gal['Norm_err'] if gal is not None else np.nan)

    results['galindex'].append(gal['Index'] if gal is not None else np.nan)
    results['galindex_err'].append(gal['Index_err'] if gal is not None else np.nan)

    results['isonorm'].append(iso['Scale'])
    results['isonorm_err'].append(iso['Scale_err'])


rec = fromarrays(results.values(), names=results.keys())

savename = join(savedir,'cached.fits')
makefits(rec, savename, clobber=True)

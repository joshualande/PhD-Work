from os.path import join, expandvars
from glob import glob
from collections import defaultdict

import numpy as np

import yaml

from lande.utilities.save import savedict

savedir = expandvars(join('$w44simdata/','v33'))

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
        results['index_%s' % h].append(-x[h]['gtlike']['model']['Index'])

        if h is not 'Point': 
            results['r68_%s' % h].append(x[h]['pointlike']['spatial_model']['r68'])
        if 'Elliptical' in h:
            results['angle_%s' % h].append(180+x[h]['pointlike']['spatial_model']['Pos_Angle'])

            results['eccentricity_%s' % h].append(
                np.sqrt(1-x[h]['pointlike']['spatial_model']['Minor_Axis']**2/x[h]['pointlike']['spatial_model']['Major_Axis']**2))

        if 'Ring' in h:
            results['fraction_%s' % h].append(x[h]['pointlike']['spatial_model']['Fraction'])



    results['ll_mc'].append(x['mc']['logLikelihood'])
    results['TS_mc'].append(x['mc']['TS'])
    results['flux_mc'].append(x['mc']['flux']['flux'])
    results['index_mc'].append(x['mc']['model']['Index'])
    results['r68_mc'].append(x['mc']['spatial_model']['r68'])
    results['angle_mc'].append(180+x['mc']['spatial_model']['Pos_Angle'])
    results['eccentricity_mc'].append(
        np.sqrt(1-x['mc']['spatial_model']['Minor_Axis']**2/x['mc']['spatial_model']['Major_Axis']**2))
    results['fraction_mc'].append(x['mc']['spatial_model']['Fraction'])

savename = join(savedir,'merged.hdf5')
savedict(results, savename)


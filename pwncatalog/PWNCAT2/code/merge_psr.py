import os
from os.path import join,exists
from glob import glob

import yaml
import numpy as np

from lande.utilities.tools import merge_dict,tolist

for psr in glob('PSR*'):

    os.chdir(psr)

    pointlike_results = 'results_%s_pointlike.yaml' % psr
    gtlike_results = [ 'results_%s_gtlike_%s.yaml' % (psr,i) for i in ['at_pulsar', 'point', 'extended']]
    extul_results = 'results_%s_extul_point.yaml' % psr

    all_results = [pointlike_results,extul_results]+gtlike_results
    if np.all(map(exists,all_results)):
        print 'Merging Pulsar %s' % psr

        all_dicts = [yaml.load(open(i)) for i in all_results]
        results = tolist(merge_dict(all_dicts))

        for which in ['pointlike','gtlike']:
            results['extended'][which]['ts_ext'] = \
                    2*(results['extended'][which]['logLikelihood'] - results['point'][which]['logLikelihood'])

        open('results_%s.yaml' % psr,'w').write(yaml.dump(results))
    else:
        print 'Skippign Pulsar %s (not all jobs complete)' % psr

    os.chdir('..')

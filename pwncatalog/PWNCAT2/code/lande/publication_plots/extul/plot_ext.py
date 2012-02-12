from os.path import join, exists
from glob import glob

import yaml

datadir = '/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/monte_carlo/extul/v1'

for index in [1.5, 2, 2.5, 3]:

    subdir = join(datadir,'index_%s' % index)

    for jobdir in glob(join(subdir,'?????')):
        print jobdir

        results = join(jobdir,'results.yaml')
        print results, exists(results)
        
        if exists(results):

            results = results[1]

            r = yaml.load(open(results))

            for i in r:
                print i['TS_ext']




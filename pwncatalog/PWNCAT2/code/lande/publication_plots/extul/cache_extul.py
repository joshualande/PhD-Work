from os.path import join, exists
from os import remove
from glob import glob
from collections import defaultdict

import pylab as P
import yaml

from uw.utilities.makerec import RecArray,makefits

datadir = '/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/monte_carlo/extul/v2'

rec = RecArray('flux_mc index_mc extension_mc extension_ul ts_point ts_ext'.split())

for index in [1.5, 2, 2.5, 3]:

    subdir = join(datadir,'index_%s' % index)

    jobdirs = glob(join(subdir,'?????'))

    for i,jobdir in enumerate(jobdirs):
        print '%s - %s/%s' % (jobdir, i, len(jobdirs))

        results = join(jobdir,'results.yaml')
        
        if exists(results):

            r = yaml.load(open(results))

            for i in r:

                e=i['mc']['extension']
                f=i['mc']['flux']['flux']
                e_ul=i['extension_ul']
                ts=max(i['point']['TS'],0)
                ts_ext=max(i['TS_ext'],0)

                rec.append(f,index,e,e_ul,ts,ts_ext)

rec = rec()

file='cached.fits'
if exists(file): remove(file)
makefits(rec,file)

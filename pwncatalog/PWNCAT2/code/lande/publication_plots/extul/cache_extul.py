from os.path import join, exists
from os import remove
from glob import glob
from collections import defaultdict

import pylab as P
import yaml

from uw.utilities.makerec import RecArray,makefits

datadir = '/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/monte_carlo/extul/v8'

rec = RecArray('flux_mc index_mc extension_mc extension_ul ts_point ts_ext type'.split())


subdir = join(datadir,'*_index_*')

jobdirs = glob(join(subdir,'?????'))

for i,jobdir in enumerate(jobdirs):
    print '%s - %s/%s' % (jobdir, i, len(jobdirs))

    results = join(jobdir,'results.yaml')
    
    if exists(results):

        r = yaml.load(open(results))

        if r is None: continue

        for i in r:

            e=i['mc']['extension']
            f=i['mc']['flux']['flux']
            index=i['mc']['model']['Index']
            e_ul=i['extension_ul']['extension']

            if e_ul is None: e_ul = 0

            ts=max(i['point']['TS'],0)
            ts_ext=max(i['TS_ext'],0)
            type=i['type']

            rec.append(f,index,e,e_ul,ts,ts_ext,type)

rec = rec()

file='cached.fits'
if exists(file): remove(file)
makefits(rec,file)

import yaml
import numpy
import csv
import h5py

from glob import iglob
from os.path import expandvars,join,exists,getsize
workdir = expandvars('/nfs/slac/g/ki/ki03/lande/compare_flight_mc_psf/v1')


rows=[]

counter=1

for results in iglob(join( workdir, '*', 'results_*.yaml')):

    if getsize(results) < 1:
        continue

    counter +=1
    if counter % 10 == 0: print 'n=',counter

    temp=yaml.load(open(results))
    rows += temp

results_dict={}
for key in rows[0].keys(): results_dict[key]=[float(i[key]) for i in rows]

f=h5py.File('/nfs/slac/g/ki/ki03/lande/compare_flight_mc_psf/v1/merged.hdf5','w')
for k,v in results_dict.items():
    f[k]=numpy.asarray(v)

f.close()

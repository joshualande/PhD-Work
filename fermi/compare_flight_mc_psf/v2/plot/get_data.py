import h5py
import numpy as np
from scipy.stats import chi2
import yaml


file=h5py.File('/nfs/slac/g/ki/ki03/lande/fermi/data/monte_carlo/compare_flight_mc_psf/v1/merged.hdf5')

flux=np.asarray(file['flux_mc'])
ts_ext_P7SOURCE_V4=np.asarray(file['ts_ext_P7SOURCE_V4'])
ts_ext_P7SOURCE_V6=np.asarray(file['ts_ext_P7SOURCE_V6'])
ts=np.asarray(file['ts_P7SOURCE_V6'])
ts_point = ts - ts_ext_P7SOURCE_V6
index=np.asarray(file['index_mc'])


d=dict()

for i,(irf,all_ts_ext) in enumerate([
    ['P7SOURCE_V6',ts_ext_P7SOURCE_V6],
    ['P7SOURCE_V4',ts_ext_P7SOURCE_V4]
]):

    max_ts=max(all_ts_ext) + 1

    d[irf]=dict()

    index_mc=2
    for flux_mc in [ 1e-8, 3e-8, 1e-7, 3e-7, 1e-6, 3e-6 ]:


        select = (flux==flux_mc) & (index==index_mc) & (ts_point>25)


        print 'index=%s, flux=%s, num=%s' % (index_mc,flux_mc,np.sum(select))
        print np.mean(ts_point[select])

        if np.sum(select) < 100:
            continue

        print irf, flux_mc, select
        
        ts_ext = all_ts_ext[select]

        ts_ext[ts_ext<0] = 0


        bins=np.linspace(0,max_ts,1e3)
        bin_center=bins[:-1] + (bins[1]-bins[0])/2

        binned=np.histogram(ts_ext,bins=bins)[0]

        cdf=np.cumsum(binned[::-1])[::-1]

        cdf=cdf.astype(float)/cdf[0] # normalize

        d[irf][flux_mc]=dict(ts=bin_center.tolist(), cdf=cdf.tolist())




y = chi2.sf(bins,1)/2
d['chi2']=dict(ts=bins.tolist(),cdf=y.tolist())

#print yaml.dump(d)

open('extension_test.yaml','w').write(yaml.dump(d))


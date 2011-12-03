import h5py
import numpy as np
from scipy.stats import chi2


file=h5py.File('/nfs/slac/g/ki/ki03/lande/fermi/data/monte_carlo/compare_flight_mc_psf/v1/merged.hdf5')

flux=np.asarray(file['flux_mc'])
ts_ext_P7SOURCE_V4=np.asarray(file['ts_ext_P7SOURCE_V4'])
ts_ext_P7SOURCE_V6=np.asarray(file['ts_ext_P7SOURCE_V6'])
ts=np.asarray(file['ts_P7SOURCE_V6'])
ts_point = ts - ts_ext_P7SOURCE_V6
index=np.asarray(file['index_mc'])

max_ts=max(max(ts_ext_P7SOURCE_V4),max(ts_ext_P7SOURCE_V6)) + 1

d=dict()

for i,(irf,all_ts_ext) in enumerate([
    ['P7SOURCE_V6',ts_ext_P7SOURCE_V6],
    ['P7SOURCE_V4',ts_ext_P7SOURCE_V4]
]):

    d[irf]=dict()

    index_mc=2
    for flux_mc in zip(
            reversed([ 1e-8, 3e-8, 1e-7, 3e-7, 1e-6, 3e-6 ]),
        ):


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

        if any(ts_ext>max_ts):
            print '> max: ',irf,ts_ext[np.where(ts_ext>max_ts)]

        cdf=np.cumsum(binned[::-1])[::-1]

        cdf=cdf.astype(float)/cdf[0] # normalize

        d[irf][flux_mc]=dict(x=bin_center, y=cdf)




y = chi2.sf(bins,1)/2
d['chi2']=dict(x=bins,y=y)

print d

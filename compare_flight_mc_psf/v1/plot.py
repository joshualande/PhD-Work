import h5py
import pylab as P
import numpy as np
from scipy.stats import chi2


file=h5py.File('/nfs/slac/g/ki/ki03/lande/compare_flight_mc_psf/v1/merged.hdf5')

flux=np.asarray(file['flux_mc'])
ts_ext_P7SOURCE_V4=np.asarray(file['ts_ext_P7SOURCE_V4'])
ts_ext_P7SOURCE_V6=np.asarray(file['ts_ext_P7SOURCE_V6'])
ts=np.asarray(file['ts_P7SOURCE_V6'])
index=np.asarray(file['index_mc'])


index_mc=2
#for flux_mc in [ 1e-9, 3e-9, 1e-8, 3e-8, 1e-7, 3e-7, 1e-6, 3e-6 ]:
for flux_mc,kwargs in [ [3e-8, dict() ] ]:

    select = np.where((flux==flux_mc) & (index==index_mc) & (ts>25))

    for irf,ts_ext in [['P7SOURCE_V4',ts_ext_P7SOURCE_V4],
                       ['P7SOURCE_V6',ts_ext_P7SOURCE_V6]]:
        
        ts_ext = ts_ext[select]

        print irf, ts_ext
        ts_ext[ts_ext<0] = 0
        print irf, ts_ext


        max_ts=25
        bins=np.linspace(0,max_ts,1e3)
        bin_center=bins[:-1] + (bins[1]-bins[0])/2

        binned=np.histogram(ts_ext,bins=bins)[0]

        if any(ts_ext>max_ts):
            print 'v4: ',ts_ext[np.where(ts_ext>max_ts)]
            print 'v6: ',ts_ext[np.where(ts_ext>max_ts)]

        cdf=np.cumsum(binned[::-1])[::-1]
        cdf=cdf.astype(float)/cdf[0] # normalize

        #cdf[cdf==0]=min_cdf

        #def format(x):
        #    a,b=x.split('e-0')
        #    return (r'$%s\times'%a if a !='1' else r'$')+'10^{-%s}\ \mathrm{ph}\ \mathrm{cm}^{-2}\mathrm{s}^{-1}$' % b
        #grid[i].semilogy(bin_center,cdf,color,linewidth=1,label=format(flux_mc))

        P.semilogy(bin_center,cdf,linewidth=1,label='%s, %s' % (irf,flux_mc), **kwargs)

    y = chi2.sf(bins,1)/2
    P.semilogy(bins, y, 'red', linewidth=1, label='$\chi^2_1/2$', zorder=0, dashes=(5,3))


P.legend()

P.savefig('compare_flight_mc_psf.pdf')


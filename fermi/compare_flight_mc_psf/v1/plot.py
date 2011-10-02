import h5py
import pylab as P
import numpy as np
from scipy.stats import chi2


file=h5py.File('/nfs/slac/g/ki/ki03/lande/compare_flight_mc_psf/v1/merged.hdf5')

flux=np.asarray(file['flux_mc'])
ts_ext_P7SOURCE_V4=np.asarray(file['ts_ext_P7SOURCE_V4'])
ts_ext_P7SOURCE_V6=np.asarray(file['ts_ext_P7SOURCE_V6'])
ts=np.asarray(file['ts_P7SOURCE_V6'])
ts_point = ts - ts_ext_P7SOURCE_V6
index=np.asarray(file['index_mc'])

fig=P.figure(figsize=(6.5,4))
from mpl_toolkits.axes_grid.axes_grid import Grid

grid = Grid(fig, 111, nrows_ncols = (1, 2), axes_pad=0.0)


min_cdf = 1e-4

for i,(irf,all_ts_ext) in enumerate([
    ['P7SOURCE_V6',ts_ext_P7SOURCE_V6],
    ['P7SOURCE_V4',ts_ext_P7SOURCE_V4]
]):

    max_ts=max(all_ts_ext) + 1

    axes = grid[i]

    index_mc=2
    for flux_mc in [ 1e-9, 3e-9, 1e-8, 3e-8, 1e-7, 3e-7, 1e-6, 3e-6 ]:
        kwargs=dict()

        select = (flux==flux_mc) & (index==index_mc) & (ts_point>25)

        print 'index=%s, flux=%s, num=%s' % (index_mc,flux_mc,np.sum(select))

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

        cdf[cdf == 0] = min_cdf
        
        axes.semilogy(bin_center,cdf,linewidth=1,label='%s' % (flux_mc), **kwargs)


    y = chi2.sf(bins,1)/2
    axes.semilogy(bins, y, 'red', linewidth=1, label='$\chi^2_1/2$', zorder=0, dashes=(5,3))

    axes.set_ylim(min_cdf,1)

    axes.set_xlabel('TS_ext')
    axes.set_ylabel('Cumulative Density')


grid[0].legend()

grid[1].set_xlim(0,100)

P.savefig('compare_flight_mc_psf.pdf')


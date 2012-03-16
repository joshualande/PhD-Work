from os.path import join, expandvars

import pylab as P
import yaml
import h5py
import numpy as np
from scipy.stats import chi2

from lande.utilities.arrays import isclose

recname = expandvars(join('$tsext_plane_data', 'v5', 'merged.hdf5'))
r = h5py.File(recname)

flux_list = np.asarray(r['flux'])
index_list = np.asarray(r['index'])
ts_point_list = np.asarray(r['TS_point'])
ts_ext_list = np.asarray(r['TS_ext'])

ts_ext_list = np.where(ts_ext_list > 0, ts_ext_list, 0)

max_ts_ext = max(ts_ext_list)

fig = P.figure(None, figsize=(6,6))
axes = fig.add_subplot(111)


for index,kwargs in [[1.5,dict(color='blue', label='index=1.5')],
                     [2,  dict(color='purple', label='index=2')],
                     [2.5,dict(color='green', label='index=2.5')],
                     [3,  dict(color='black', label='index=3')]
                    ]:

    cut = isclose(index,index_list) & (ts_point_list>=25)

    print 'index = %s' % index
    print '.. num', sum(cut)
    print '.. num bad', sum(isclose(index, index_list) & (ts_point_list < 25))
    ts_point = ts_point_list[cut]
    print '.. average ts_point',np.average(ts_point), np.std(ts_point)
    ts_ext = ts_ext_list[cut]
    print '.. average ts_ext',np.average(ts_ext), np.std(ts_ext)


    bins=np.linspace(0,max_ts_ext,1e3)
    data=np.histogram(ts_ext,bins=bins)[0]
    
    cdf=np.cumsum(data[::-1])[::-1]
    cdf=cdf.astype(float)/cdf[0] # normalize
    cdf = np.append(cdf, 0)

    axes.semilogy(bins,cdf,linewidth=1, **kwargs)


lower,upper=axes.get_xlim()
bins=np.linspace(lower,upper,10000)
y = chi2.sf(bins,1)/2
axes.semilogy(bins, y, color='red', linewidth=1, label='$\chi^2_1/2$', zorder=0, dashes=(5,3))

P.legend()

P.savefig('plot_tsext_plane.pdf')

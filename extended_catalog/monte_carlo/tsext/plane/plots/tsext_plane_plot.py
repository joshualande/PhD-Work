from os.path import join, expandvars

import pylab as P
import yaml
import h5py
import numpy as np
from scipy.stats import chi2

from lande.utilities.arrays import almost_equal
from lande.utilities.pubplot import set_latex_defaults, get_bw, save
from lande.utilities.save import loaddict

set_latex_defaults()

bw = get_bw()

r = loaddict('$tsext_plane_data/v12/merged.hdf5')
print r.keys()

flux_list = np.asarray(r['flux_mc'])
index_list = np.asarray(r['index_mc'])
ts_point_list = np.asarray(r['TS_point'])
ts_ext_list = np.asarray(r['TS_ext'])
ts_ext_list = np.where(ts_ext_list > 0, ts_ext_list, 0)

l_list = np.asarray(r['glon'])
b_list = np.asarray(r['glat'])

max_ts_ext = max(ts_ext_list)

fig = P.figure(None, figsize=(6,6))
axes = fig.add_subplot(111)


for index,basecut,kwargs in [
    [1.5,   almost_equal(1.5,index_list),           dict(color='blue', label='index=1.5')],
    [2.0,   almost_equal(2.0,index_list),           dict(color='purple', label='index=2')],
    [2.5,   almost_equal(2.5,index_list),           dict(color='green', label='index=2.5')],
    [3.0,   almost_equal(3.0,index_list),           dict(color='black', label='index=3')],
    [3.0,   almost_equal(3.0,index_list),           dict(color='black', label='index=3')],
#    ['sum', np.ones_like(index_list).astype(bool),  dict(color='orange', label='all indices')],
]:

    cut = basecut & (ts_point_list>=25)

    print 'index = %s' % index
    num_good = sum(cut)
    num_bad = sum(basecut & (ts_point_list < 25))
    print '.. num good', num_good
    print '.. num bad', num_bad

    if num_good < 1: continue

    ts_ext = ts_ext_list[cut]

    ts_point = ts_point_list[cut]
    print '.. average ts_point',np.average(ts_point), np.std(ts_point)
    ts_point_nocut = ts_point_list[basecut]
    print '.. average ts_point (nocut)',np.average(ts_point_nocut), np.std(ts_point_nocut)
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

save('plot_tsext_plane')

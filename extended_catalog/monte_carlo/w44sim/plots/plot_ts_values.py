from os.path import join, expandvars

import matplotlib.font_manager 
from matplotlib.ticker import MaxNLocator
import numpy as np
import h5py
import pylab as P

from lande.utilities.pubplot import set_latex_defaults,get_bw,save

set_latex_defaults()
bw=get_bw()

merged = expandvars(join('$w44simdata/','v33', 'merged.hdf5'))
results = h5py.File(merged, 'r')

ts_point = np.asarray(results['TS_Point'])

ll_point = np.asarray(results['ll_Point'])
ll_gaussian = np.asarray(results['ll_Gaussian'])
ll_disk = np.asarray(results['ll_Disk'])
ll_elliptical_disk = np.asarray(results['ll_EllipticalDisk'])
ll_elliptical_ring = np.asarray(results['ll_EllipticalRing'])

fig=P.figure(None, figsize=(6,6))

def histogram(axes, data,**kwargs):

    if len(data)==2:
        print data
        print len(data[0]),min(data[0]),max(data[0])
        print len(data[1]),min(data[1]),max(data[1])

    bins = 30
    axes.hist(data, 
              bins=bins,
              histtype='step',
              **kwargs)

    axes.xaxis.set_major_locator(MaxNLocator(6))
    axes.yaxis.set_major_locator(MaxNLocator(6))


axes=fig.add_subplot(221)
histogram(axes, ts_point, color='black')
axes.set_ylim(0,100)
axes.set_xlabel(r'$\mathrm{TS}_\mathrm{point}$')

axes=fig.add_subplot(222)
histogram(axes, 
          data=[2*(ll_disk-ll_point),
                2*(ll_gaussian-ll_point)],
          label=['Disk','Gaussian'],
          color=['black','red'])
axes.set_xlabel(r'$\mathrm{TS}_\mathrm{ext}$')
prop = matplotlib.font_manager.FontProperties(size=10)
axes.set_ylim(0,100)
axes.legend(prop=prop)

axes=fig.add_subplot(223)
histogram(axes, 
          2*(ll_elliptical_disk-ll_disk), 
          color='black')
axes.set_xlabel(r'$\mathrm{TS}_\mathrm{ellip.\ disk}-\mathrm{TS}_\mathrm{disk}$')

axes=fig.add_subplot(224)
ts_inc = 2*(ll_elliptical_ring-ll_elliptical_disk)
ts_inc = np.where(ts_inc > 0, ts_inc, 0)
histogram(axes, ts_inc,
         color='black')
axes.set_xlabel(r'$\mathrm{TS}_\mathrm{ellip.\ ring}-\mathrm{TS}_\mathrm{ellip.\ disk}$')

fig.tight_layout()

save('ts_comparision_w44sim')

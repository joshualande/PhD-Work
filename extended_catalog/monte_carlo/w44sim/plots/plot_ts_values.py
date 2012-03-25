from os.path import join, expandvars

import matplotlib.font_manager 
from matplotlib.ticker import MaxNLocator
import numpy as np
import h5py
import pylab as P

from lande.utilities.pubplot import set_latex_defaults,get_bw,save

set_latex_defaults()
bw=get_bw()

merged = expandvars(join('$w44simdata/','v7', 'merged.hdf5'))
results = h5py.File(merged, 'r')

ts_point = np.asarray(results['TS_Point'])

ll_point = np.asarray(results['ll_Point'])
ll_gaussian = np.asarray(results['ll_Gaussian'])
ll_disk = np.asarray(results['ll_Disk'])
ll_elliptical_disk = np.asarray(results['ll_EllipticalDisk'])
ll_elliptical_ring = np.asarray(results['ll_EllipticalRing'])

def histogram(axes, data, **kwargs):
    #default_kwargs=dict(bins=30, histtype='step')
    default_kwargs=dict(bins=30)
    default_kwargs.update(kwargs)

    axes.set_autoscaley_on(True)
    axes.set_autoscaley_on(True)

    bins = np.linspace(data.min(), data.max(), 30)
    data = np.histogram(data, bins=bins)

    axes.plot(bins, data)
    #axes.hist(data, **default_kwargs)

    axes.xaxis.set_major_locator(MaxNLocator(4))


fig=P.figure(None, figsize=(6,6))


axes=fig.add_subplot(221)
histogram(axes, ts_point)
axes.set_xlabel(r'$\textrm{TS}_\textrm{point}$')

axes=fig.add_subplot(222)
histogram(axes, 2*(ll_disk-ll_point), label='Disk')
histogram(axes, 2*(ll_gaussian-ll_point), label='Gaussian')
axes.set_xlabel(r'$\textrm{TS}_\textrm{ext}$')
prop = matplotlib.font_manager.FontProperties(size=10)
axes.legend(prop=prop)

axes=fig.add_subplot(223)
histogram(axes, 2*(ll_elliptical_disk-ll_disk))
axes.set_xlabel(r'$\textrm{TS}_\textrm{ellip. disk}-\textrm{TS}_\textrm{disk}$')

axes=fig.add_subplot(224)
ts_inc = 2*(ll_elliptical_ring-ll_elliptical_disk)
ts_inc = np.where(ts_inc > 0, ts_inc, 0)
histogram(axes, ts_inc)
axes.set_xlabel(r'$\textrm{TS}_\textrm{ellip. ring}-\textrm{TS}_\textrm{ellip. disk}$')

save('ts_comparision_w44sim')

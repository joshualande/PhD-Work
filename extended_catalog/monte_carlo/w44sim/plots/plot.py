from os.path import join, expandvars

from lande.utilities.pubplot import set_latex_defaults,get_bw,save

import matplotlib.font_manager 
from matplotlib.ticker import MaxNLocator
import numpy as np
import h5py
import pylab as P

set_latex_defaults()
bw=get_bw()

savedir = expandvars(join('$w44simdata/','v4', 'merged.hdf5'))
results = h5py.File(savedir, 'r')

ts_point = np.asarray(results['TS_Point'])

ll_point = np.asarray(results['ll_Point'])
ll_gaussian = np.asarray(results['ll_Gaussian'])
ll_disk = np.asarray(results['ll_Disk'])
ll_elliptical_disk = np.asarray(results['ll_EllipticalDisk'])
ll_elliptical_ring = np.asarray(results['ll_EllipticalRing'])

fig=P.figure(None, figsize=(6,6))

#hist_kwargs=dict(histtype='step')
hist_kwargs=dict()

axes=fig.add_subplot(221)
axes.hist(ts_point, **hist_kwargs)
axes.xaxis.set_major_locator(MaxNLocator(4))
axes.set_xlabel(r'$\textrm{TS}_\textrm{point}$')

axes=fig.add_subplot(222)
axes.hist(2*(ll_disk-ll_point), label='Disk', **hist_kwargs)
axes.hist(2*(ll_gaussian-ll_point), label='Gaussian', **hist_kwargs)
axes.xaxis.set_major_locator(MaxNLocator(4))
axes.set_xlabel(r'$\textrm{TS}_\textrm{ext}$')

prop = matplotlib.font_manager.FontProperties(size=10)
axes.legend(prop=prop)

axes=fig.add_subplot(223)
axes.hist(2*(ll_elliptical_disk-ll_disk), **hist_kwargs)
axes.set_xlabel(r'$\textrm{TS}_\textrm{ellip. disk}-\textrm{TS}_\textrm{disk}$')

axes=fig.add_subplot(224)

ts_inc = 2*(ll_elliptical_ring-ll_elliptical_disk)
ts_inc = np.where(ts_inc > 0, ts_inc, 0)
axes.hist(ts_inc, **hist_kwargs)
axes.set_xlabel(r'$\textrm{TS}_\textrm{ellip. ring}-\textrm{TS}_\textrm{ellip. disk}$')

save('w44sim')

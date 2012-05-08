from os.path import join, expandvars

import matplotlib.font_manager 
from matplotlib.ticker import MaxNLocator
import numpy as np
import h5py
import pylab as P
from matplotlib.lines import Line2D

from lande.utilities.pubplot import set_latex_defaults,get_bw,save
from lande.utilities.plotting import label_axes

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
          data=[2*(ll_gaussian-ll_point),
                2*(ll_disk-ll_point)],
          color=['red' if not bw else '0.6','black'])
axes.set_xlabel(r'$\mathrm{TS}_\mathrm{ext}$')
prop = matplotlib.font_manager.FontProperties(size=10)
axes.set_ylim(0,100)
axes.legend([Line2D([0],[0],color='black'),Line2D([0],[0],color='red' if not bw else '0.6')],
            ['disk','Gaussian'],
            prop=prop)


axes=fig.add_subplot(223)
histogram(axes, 
          2*(ll_elliptical_disk-ll_disk), 
          color='black')
axes.set_xlabel(r'$\mathrm{TS}_\mathrm{elliptical\ disk}-\mathrm{TS}_\mathrm{disk}$')

axes=fig.add_subplot(224)
ts_inc = 2*(ll_elliptical_ring-ll_elliptical_disk)
ts_inc = np.where(ts_inc > 0, ts_inc, 0)
histogram(axes, ts_inc,
         color='black')
axes.set_xlabel(r'$\mathrm{TS}_\mathrm{elliptical\ ring}-\mathrm{TS}_\mathrm{elliptical\ disk}$')

fig.tight_layout()

label_axes(fig)

save('ts_comparison_w44sim')

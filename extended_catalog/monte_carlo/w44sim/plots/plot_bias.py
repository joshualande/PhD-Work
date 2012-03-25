
from os.path import join, expandvars
import matplotlib.font_manager
from matplotlib.ticker import MaxNLocator

import numpy as np
import h5py
import pylab as P

from lande.utilities.pubplot import set_latex_defaults,get_bw,save

set_latex_defaults()
bw=get_bw()

savedir = expandvars(join('$w44simdata/','v7', 'merged.hdf5'))
results = h5py.File(savedir, 'r')

def plot(axes, quantity, hist_kwargs):

    for type in ['Point', 'Disk', 'Gaussian', 'EllipticalDisk', 'EllipticalRing']:

        name = '%s_%s' % (quantity,type)
        if name in results:
            array = np.asarray(results[name])

            print '%s, %s, average=%s' % (quantity, type, np.average(array))

            # TEMPORARY
            hist_kwargs['bins']=30
            # TEMPORARY

            axes.hist(array, label=type, **hist_kwargs)

    mc = '%s_mc' % quantity
    if mc in results:
        r=results[mc]
        r=r[0]
        print '%s, mc=%s' % (quantity, r)
        axes.axvline(r, label='mc')

    # TEMPORARY
    axes.set_ylim(ymax=axes.get_ylim()[1] + 300)
    # TEMPORARY

    axes.xaxis.set_major_locator(MaxNLocator(4))
    prop = matplotlib.font_manager.FontProperties(size=10)
    axes.legend(prop=prop)

fig=P.figure(None, figsize=(7,3))

hist_kwargs=dict(histtype='step')

axes=fig.add_subplot(131)
plot(axes,'r68',hist_kwargs=hist_kwargs)
axes.set_xlabel('r68 (degrees)')

axes=fig.add_subplot(132)
plot(axes, 'flux', hist_kwargs=hist_kwargs)
axes.set_xlabel('flux')

axes=fig.add_subplot(133)
plot(axes, 'index', hist_kwargs=hist_kwargs)
axes.set_xlabel('Spectral Index')

fig.subplots_adjust(bottom=0.2)

save('bias_w44sim')

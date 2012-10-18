
from os.path import join, expandvars
import matplotlib.font_manager
from matplotlib.ticker import MaxNLocator
from matplotlib.lines import Line2D

import numpy as np
import h5py
import pylab as P

from lande.utilities.pubplot import set_latex_defaults,get_bw,save
from lande.utilities.plotting import label_axes

set_latex_defaults()
bw=get_bw()

savedir = expandvars(join('$w44simdata/','v33', 'merged.hdf5'))
results = h5py.File(savedir, 'r')

print 'num',len(results['ll_mc'])

print_names = ['point',
               'Gaussian', 
               'disk', 
               'elliptical disk', 
               'elliptical ring', 
              ]

all_types = ['Point',
             'Gaussian',
             'Disk',
             'EllipticalDisk',
             'EllipticalRing']
all_colors = ['green' if not bw else '0.8',
              'orange' if not bw else '0.6',
              'blue' if not bw else '0.4',
              'red' if not bw else '0.2',
              'black' if not bw else '0.0']

def plot(axes, quantity, scale=1):

    bins=50

    d,l,c=[],[],[]

    for type,color in zip(all_types,all_colors):
        name = '%s_%s' % (quantity,type)
        if name in results:
            d.append(np.asarray(results[name])/scale)
            c.append(color)

            print '%s, %s, average=%s, len=%s' % (quantity, type, np.average(results[name]),len(results[name]))
    
    axes.hist(d, bins=bins, histtype='step', color=c)

    mc = '%s_mc' % quantity
    if mc in results:
        r=results[mc][0]/scale
        print '%s, mc=%s' % (quantity, r)
        axes.axvline(r, label='mc', dashes=[5,2], color='k')

    axes.xaxis.set_major_locator(MaxNLocator(5))
    axes.yaxis.set_major_locator(MaxNLocator(5))

    axes.set_ylabel('Number')
    axes.set_ylim(ymin=0)

#fig=P.figure(None, figsize=(6,6))
fig=P.figure(None, figsize=(6,6))


#axes=fig.add_subplot(321)
axes=fig.add_subplot(221)
plot(axes, 'flux', scale=1e-8)
axes.set_xlabel(r'Flux ($10^{-8}$ ph$\;$cm$^{-1}$s$^{-1}$)')

#axes=fig.add_subplot(322)
axes=fig.add_subplot(222)
plot(axes, 'index')
axes.set_xlabel('Spectral Index')

#axes=fig.add_subplot(323)
axes=fig.add_subplot(223)
plot(axes,'r68')
axes.set_xlabel('r68 (deg)')

#axes=fig.add_subplot(324)
#plot(axes,'eccentricity')
#axes.set_xlabel('Eccentricity')


#axes=fig.add_subplot(325)
#plot(axes,'angle')
#axes.set_xlabel('Ellipse Angle (deg)')


#axes=fig.add_subplot(326)
#plot(axes,'fraction')
#axes.set_xlabel('Ring Fraction')


prop = matplotlib.font_manager.FontProperties(size=6)
plots=[Line2D([0],[0],color=i) for i in all_colors]
axes.legend(reversed(plots),reversed(print_names), prop=prop, loc=1,
            borderaxespad=1)

fig.tight_layout()

label_axes(fig, borderpad=0.2)

save('bias_w44sim')

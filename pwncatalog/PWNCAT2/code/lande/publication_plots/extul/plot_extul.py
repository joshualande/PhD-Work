import plot_helper
from os.path import join, exists
from glob import glob
from collections import defaultdict

import pylab as P
import yaml

from mpl_toolkits.axes_grid.axes_grid import Grid
import numpy as np

from uw.like.roi_plotting import DegreesFormatter

from lande_plotting import fix_axesgrid

bw=plot_helper.get_bw()

fig = P.figure(None,(6,6))

grid = Grid(fig, 111, 
            nrows_ncols = (3, 1),
            share_all=False,
            axes_pad=0.0)

from uw.utilities.makerec import fitsrec
r = fitsrec('cached.fits')

extension_mc = r['extension_mc']
extension_ul = r['extension_ul']
index_mc = r['index_mc']
ts_point = r['ts_point']
ts_ext = r['ts_ext']

for index, plot_kwargs in [[1.5, dict(label=r'$\gamma=1.5$', color='blue' )],
                           [2,   dict(label=r'$\gamma=2$',   color='red'  )],
                           [2.5, dict(label=r'$\gamma=2.5$', color='green')],
                           [3,   dict(label=r'$\gamma=3$',   color='black')]
                          ]:

    cut = index_mc == index

    extlist = np.sort(np.unique(extension_mc[cut]))
            
    avg_ts_point = [np.mean(ts_point[cut&(extension_mc==e)]) for e in extlist]
    avg_ts_ext = [np.mean(ts_point[cut&(extension_mc==e)]) for e in extlist]
    coverage = [ np.average(e < extension_ul[cut&(extension_mc==e)]) for e in extlist]

    grid[0].plot(extlist, avg_ts_point, 'o', **plot_kwargs)
    grid[1].plot(extlist, avg_ts_ext, 'o', **plot_kwargs)
    grid[2].plot(extlist, coverage, '-', **plot_kwargs)


grid[0].legend(numpoints=1)

for g in grid: 
    g.xaxis.set_major_formatter(DegreesFormatter)
    g.set_xlabel('Extension')


grid[2].set_ylim(ymax=1.1)

grid[0].set_ylabel(r'$\mathrm{TS}_\mathrm{point}$')
grid[1].set_ylabel(r'$\mathrm{TS}_\mathrm{ext}$')
grid[2].set_ylabel(r'Coverage')

fix_axesgrid(grid)

plot_helper.save('extul')

import plot_helper
from os.path import join, exists
from glob import glob
from collections import defaultdict

import pylab as P
import yaml

from mpl_toolkits.axes_grid.axes_grid import Grid
from matplotlib.font_manager import FontProperties
import numpy as np

from uw.like.roi_plotting import DegreesFormatter

from lande_plotting import fix_axesgrid

bw=plot_helper.get_bw()

fig = P.figure(None,(6,6))

grid = Grid(fig, 111, 
            nrows_ncols = (4, 1),
            share_all=False,
            axes_pad=0.2)

from uw.utilities.makerec import fitsrec
r = fitsrec('cached.fits')
print r

extension_mc = r['extension_mc']
extension_ul = r['extension_ul']
index_mc = r['index_mc']
ts_point = r['ts_point']
ts_ext = r['ts_ext']
flux_mc = r['flux_mc']
type = np.char.strip(r['type'])

for index, plot_kwargs in [
                           [1.5, dict(label=r'$\gamma=1.5$', color='blue' )],
                           [2,   dict(label=r'$\gamma=2$',   color='red'  )],
                           [2.5, dict(label=r'$\gamma=2.5$', color='green')],
                           [3,   dict(label=r'$\gamma=3$',   color='black')]
                          ]:

    #cut = (index_mc == index) & (type=='dim')
    cut = (index_mc == index) & (type=='bright')

    extlist = np.sort(np.unique(extension_mc[cut]))

    print sum(cut),len(extlist)
    print 'for gamma=%s, avg num=%s' % (index,sum(cut)/len(extlist))

    for e in extlist:
        assert len(np.unique(flux_mc[cut&(extension_mc==e)])) == 1

    flux = [flux_mc[cut&(extension_mc==e)][0] for e in extlist]
            
    avg_ts_point = [np.mean(ts_point[cut&(extension_mc==e)]) for e in extlist]
    avg_ts_ext = [np.mean(ts_ext[cut&(extension_mc==e)]) for e in extlist]
    coverage = [ np.average(e < extension_ul[cut&(extension_mc==e)]) for e in extlist]

    print index, extlist, flux, avg_ts_point, avg_ts_ext, coverage

    #grid[0].semilogy(extlist, flux, '-', **plot_kwargs)
    grid[0].semilogy(extlist, flux, '*', **plot_kwargs)
    grid[1].plot(extlist, avg_ts_point, 'o', **plot_kwargs)
    grid[2].semilogy(extlist, avg_ts_ext, 'o', **plot_kwargs)
    #grid[3].plot(extlist, coverage, '-', **plot_kwargs)
    grid[3].plot(extlist, coverage, '*', **plot_kwargs)


prop = FontProperties(size=10)
grid[1].legend(numpoints=1, ncol=2, loc=2, prop=prop)

for g in grid: 
    g.xaxis.set_major_formatter(DegreesFormatter)
    g.set_xlabel('Extension')


grid[3].set_ylim(ymax=1.1)

grid[0].set_ylabel(r'Flux')
grid[1].set_ylabel(r'$\langle\mathrm{TS}_\mathrm{point}\rangle$')
grid[2].set_ylabel(r'$\langle\mathrm{TS}_\mathrm{ext}\rangle$')
grid[3].set_ylabel(r'Coverage')

grid[1].axhline(25, color='black', dashes=[5,2])
grid[2].axhline(16, color='black', dashes=[5,2])
grid[3].axhline(0.95, color='black', dashes=[5,2])

#fix_axesgrid(grid)

plot_helper.save('extul')

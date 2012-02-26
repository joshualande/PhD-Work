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

from lande_plotting import label_axesgrid

bw=plot_helper.get_bw()

from uw.utilities.makerec import fitsrec

r = fitsrec('/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/monte_carlo/extul/v11/cached.fits')

for type in ['dim','bright']:

    fig = P.figure(None,(6,6))

    grid = Grid(fig, 111, 
                nrows_ncols = (4, 1),
                share_all=False,
                axes_pad=0.2)


    extension_mc = r['extension_mc']
    extension_ul = r['extension_ul']
    index_mc = r['index_mc']
    ts_point = r['ts_point']
    ts_ext = r['ts_ext']
    flux_mc = r['flux_mc']
    type_array = np.char.strip(r['type'])

    for index, plot_kwargs in [
                               [1.5, dict(label=r'$\gamma=1.5$', color='blue' )],
                               [2,   dict(label=r'$\gamma=2$',   color='red'  )],
                               [2.5, dict(label=r'$\gamma=2.5$', color='green')],
                               [3,   dict(label=r'$\gamma=3$',   color='black')]
                              ]:

        cut = (index_mc == index) & (type_array==type)

        extlist = np.sort(np.unique(extension_mc[cut]))


        for e in extlist:
            assert len(np.unique(flux_mc[cut&(extension_mc==e)])) == 1

        a = np.asarray

        flux = a([flux_mc[cut&(extension_mc==e)][0] for e in extlist])
                
        avg_ts_point = a([np.mean(ts_point[cut&(extension_mc==e)]) for e in extlist])
        avg_ts_ext = a([np.mean(ts_ext[cut&(extension_mc==e)]) for e in extlist])
        coverage = a([ np.average(e < extension_ul[cut&(extension_mc==e)]) for e in extlist])

        number = a([ sum(cut&(extension_mc==e)) for e in extlist])
        print 'For %s, gamma=%s:' % (type,index)
        print '-- extlist=',extlist.tolist()
        print '-- flux=',flux.tolist()
        print '-- avg_ts_point', avg_ts_point.tolist()
        print '-- avg_ts_ext', avg_ts_ext.tolist()
        print '-- coverage', coverage.tolist()
        print '-- number', number.tolist()

        grid[0].semilogy(extlist, flux, '-', **plot_kwargs)
        grid[1].plot(extlist, avg_ts_point, 'o', **plot_kwargs)
        grid[2].semilogy(extlist, avg_ts_ext, 'o', **plot_kwargs)


        #error=False
        error=True
        if not error:
            grid[3].plot(extlist, coverage, '-', **plot_kwargs)
        else:
            import scipy.stats.distributions as dist

            c = 0.683 # See page 6 in the text
            k = a([np.sum(e < extension_ul[cut&(extension_mc==e)]) for e in extlist])
            n = a([np.sum(cut&(extension_mc==e)) for e in extlist])

            # Formula from http://arxiv.org/pdf/1012.0566v3.pdf
            p = coverage
            p_lower = dist.beta.ppf((1-c)/2.,k+1,n-k+1)
            p_higher = dist.beta.ppf(1-(1-c)/2.,k+1,n-k+1)

            grid[3].fill_between(extlist.tolist(), p_lower.tolist(), p_higher.tolist(), alpha=0.5, **plot_kwargs)

    grid[0].legend(numpoints=1, ncol=2, loc=3, prop=FontProperties(size=10))

    label_axesgrid(grid)

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

    plot_helper.save('extul_%s' % type)

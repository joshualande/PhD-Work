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

datadir = '/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/monte_carlo/extul/v1'

fig = P.figure(None,(6,6))

grid = Grid(fig, 111, 
            nrows_ncols = (3, 1),
            share_all=False,
            axes_pad=0.0)




for index, plot_kwargs in [[1.5, dict(label=r'$\gamma=1.5$', color='blue' )],
                           [2,   dict(label=r'$\gamma=2$',   color='red'  )],
                           [2.5, dict(label=r'$\gamma=2.5$', color='green')],
#                           [3,   dict(label=r'$\gamma=3$',   color='black')]
                          ]:

    subdir = join(datadir,'index_%s' % index)

    extension = defaultdict(lambda: defaultdict(list))

    for jobdir in glob(join(subdir,'?????')):
        print jobdir

        results = join(jobdir,'results.yaml')
        
        if exists(results):

            r = yaml.load(open(results))

            

            for i in r:

                e=i['mc']['extension']

                ts=max(i['point']['TS'],0)
                extension[e]['TS_point'].append(ts)

                ts_ext=max(i['TS_ext'],0)
                extension[e]['TS_ext'].append(ts_ext)
                extension[e]['extension_ul'].append(i['extension_ul'])

    extlist = np.sort(extension.keys())

    av_ts_point = [ np.mean(extension[e]['TS_point']) for e in extlist ]
    av_ts_ext = [ np.mean(extension[e]['TS_ext']) for e in extlist ]

    coverage = [ np.average(e < np.asarray(extension[e]['extension_ul'])) for e in extlist ]

    grid[0].plot(extlist, av_ts_point, 'o', **plot_kwargs)
    grid[1].plot(extlist, av_ts_ext, 'o', **plot_kwargs)
    grid[2].plot(extlist, coverage, '-', **plot_kwargs)

    #print dict(extension)

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

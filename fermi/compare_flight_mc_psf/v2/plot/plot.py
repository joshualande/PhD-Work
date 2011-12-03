from matplotlib import rc
rc('ps',usedistiller='xpdf')
rc('text', usetex=True)
rc('font', family='serif', serif="Computer Modern Roman")

import yaml
import numpy as np
import pylab as P

import matplotlib
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
from matplotlib.patheffects import withStroke
from mpl_toolkits.axes_grid.axes_grid import Grid

fig=P.figure(figsize=(5,3))
fig.subplots_adjust(right=0.95, top=0.95, bottom=0.15)

grid = Grid(fig, 111, nrows_ncols = (1, 2), axes_pad=0.0)

d=yaml.load(open('extension_test.yaml'))


min_cdf = 1e-4

format_float = lambda f: r'$%s$' % str(f).replace('e-0',r'\times 10^')

for i,(name,irf) in enumerate([['(a)','P7SOURCE_V6'], ['(b)','P7SOURCE_V4']]):

    axes = grid[i]

    grid[i].add_artist(
        AnchoredText(name, frameon=False, loc=2, prop=dict(size=14,
                     path_effects=[withStroke(linewidth=5,foreground='w')])))


    index_mc=2
    for flux_mc, color in zip(
            reversed([ 1e-8, 3e-8, 1e-7, 3e-7, 1e-6, 3e-6 ]),
            ['red', 'blue', 'green', 'black', 'orange', 'gray']
        ):
        kwargs=dict(color=color)

        ts = d[irf][flux_mc]['ts']
        cdf = d[irf][flux_mc]['cdf']

        cdf = np.asarray(cdf)
        cdf[cdf == 0] = min_cdf

        axes.semilogy(ts,cdf,linewidth=1,label=format_float(flux_mc), **kwargs)


ts = d['chi2']['ts']
cdf = d['chi2']['cdf']
axes.semilogy(ts, cdf, 'red', linewidth=1, label='$\chi^2_1/2$', zorder=0, dashes=(5,3))


axes.set_ylim(min_cdf,1)

axes.set_xlabel(r'$\mathrm{TS}_\mathrm{ext}$')
axes.set_ylabel('Cumulative Density')

prop = matplotlib.font_manager.FontProperties(size=10)
grid[0].legend(loc=1, prop=prop, columnspacing=1)

grid[1].set_xlim(0,100)

P.savefig('extension_test.eps')
P.savefig('extension_test.pdf')


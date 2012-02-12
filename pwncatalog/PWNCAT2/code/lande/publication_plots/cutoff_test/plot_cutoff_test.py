import plot_helper 

import math

bw = plot_helper.get_bw()

import pylab as P
import yaml
from os.path import join, expandvars
from lande_plotting import plot_gtlike_cutoff_test

from matplotlib.offsetbox import AnchoredText

fitdir=expandvars('$pwndata/spectral/v10/analysis_no_plots/')

cutoff_candidates = ['PSRJ0034-0534', 
                     'PSRJ0633+1746', 
                     'PSRJ1813-1246', 
                     'PSRJ1836+5925', 
                     'PSRJ2021+4026', 
                     'PSRJ2055+2539', 
                     'PSRJ2124-3358']

binning = '4bpd'

hypothesis='point'



ncols = 2
nrows = int(math.ceil(float(len(cutoff_candidates))/ncols))

fig = P.figure(None,(6,6))
from mpl_toolkits.axes_grid.axes_grid import Grid
grid = Grid(fig, 111, nrows_ncols = (nrows, ncols), 
            share_all=True,
            axes_pad=0.0)

for i in range(nrows*ncols):
    axes=grid[i]
    axes.set_yscale('log')
    axes.set_xscale('log')
    axes.set_xlim(10**2,10**5.5)
    axes.set_ylim(1e-13,1e-8)

from lande_plotting import fix_axesgrid

for i,pwn in enumerate(cutoff_candidates):
    print i,pwn

    axes=grid[i]


    f = join(fitdir,pwn,'results_%s.yaml' % pwn)
    r=yaml.load(open(f))

    cutoff_results=r[hypothesis]['gtlike']['test_cutoff']
    sed=join(fitdir,pwn,'seds','sed_gtlike_%s_%s_%s.yaml' % (binning, hypothesis, pwn))

    linewidth=1

    plot_gtlike_cutoff_test(cutoff_results=cutoff_results,
                            model_0_kwargs=dict(color='0.8' if bw else 'red', zorder=0, dashes=[5,2]),
                            model_1_kwargs=dict(color='0.4' if bw else 'blue', zorder=0),

                            sed_results=sed, 
                            plot_kwargs=dict(
                                axes=axes, 
                                data_kwargs=dict(linewidth=linewidth, ul_fraction=0.7), 
                                spectral_kwargs=dict(color='red', linewidth=linewidth)
                                ),
                            title='')


    letter = chr(i+97)
    _text = '(%s) %s' % (letter, pwn.replace('PSR','').replace('-','$-$'))
    at = AnchoredText(_text, loc=2, frameon=False)
    axes.add_artist(at)

fix_axesgrid(grid)
    
for i in range(nrows*ncols):
    axes = grid[i]
    axes.set_xlabel('Energy')
    axes.set_ylabel('E$^2\,$dN/dE')


plot_helper.save('cutoff_test')

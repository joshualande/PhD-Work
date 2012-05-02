from argparse import ArgumentParser

import math
from os.path import join, expandvars, exists

import yaml
import pylab as P
import numpy as np
from skymaps import SkyDir

from matplotlib.offsetbox import AnchoredText
from matplotlib.patheffects import withStroke

from lande.utilities.plotting import label_axes

from off_peak_bb import plot

import plot_helper 

bw = plot_helper.get_bw()

cutoff_candidates = ['PSRJ0034-0534', 'PSRJ0633+1746', 'PSRJ1813-1246', 'PSRJ1836+5925', 
                     'PSRJ2021+4026', 'PSRJ2055+2539', 'PSRJ2124-3358']

pwnlist = cutoff_candidates

ncols = 2
nrows = int(math.ceil(float(len(pwnlist))/ncols))

fig=P.figure(None,figsize=(6,7))

fig.subplots_adjust(hspace=.25,wspace=.25, left=0.15, right=0.9, top=0.9, bottom=0.1)

pwndata=yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_data_lande.yaml')))

r='$pwndata/off_peak/off_peak_bb/pwncat2/v2'

for i,pwn in enumerate(pwnlist):
    print i,pwn

    results = expandvars(join(r,pwn,'results_%s.yaml' % pwn))

    assert exists(results)

    results = yaml.load(open(results))

    ft1 = pwndata[pwn]['ft1']
    skydir = SkyDir(*pwndata[pwn]['cel'])

    axes=fig.add_subplot(nrows,ncols,i+1)

    emin = results['optimal_emin']
    emax = results['emax']
    radius = results['optimal_radius']
    blocks = results['blocks']
    off_peak_phase = results['off_peak_phase']

    plot(ft1, skydir=skydir, emin=emin, emax=emax, radius=radius, 
         off_peak=off_peak_phase, 
         off_peak_kwargs=dict(color='blue'),
         blocks=blocks, 
         nbins=50,
         repeat_phase=True,
         data_kwargs=dict(color='red'),
         axes=axes)


    axes.set_ylim(ymax=axes.get_ylim()[1]*1.5)

    # from http://matplotlib.sourceforge.net/faq/howto_faq.html#align-my-ylabels-across-multiple-subplots
    axes.yaxis.set_label_coords(-0.25,0.5)

    y,x = np.unravel_index(i, (nrows,ncols))
    if x != 0:
        axes.set_ylabel('')
    if y != nrows-1:
        axes.set_xlabel('')


    label_axes(fig)

# if there are not plots alow all of the bottom, overlay
# legend on higher up plots
i=len(cutoff_candidates)
while i < nrows*ncols:
    axes=fig.add_subplot(nrows,ncols,i+1 - ncols)
    axes.set_xlabel('Pulsar Phase')
    i+=1


base='off_peak_select'
if bw:
    P.savefig('%s_bw.pdf' % base)
    P.savefig('%s_bw.eps' % base)
else:
    P.savefig('%s_color.pdf' % base)
    P.savefig('%s_color.eps' % base)

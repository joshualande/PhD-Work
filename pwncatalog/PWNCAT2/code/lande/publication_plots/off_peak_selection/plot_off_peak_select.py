import plot_helper 

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--bw", action="store_true", default=False)
parser.add_argument("--fast", action="store_true", default=False)
args=parser.parse_args()

import math
from os.path import join as j, expandvars, exists

import yaml
import pylab as P
import numpy as np

from matplotlib.offsetbox import AnchoredText
from matplotlib.patheffects import withStroke

from skymaps import SkyDir
from uw.pulsar.phase_range import PhaseRange

from lande_pulsar import get_phases

bw = plot_helper.get_bw()

cutoff_candidates = ['PSRJ0034-0534', 
                     'PSRJ0633+1746', 
                     'PSRJ1813-1246', 
                     'PSRJ1836+5925', 
                     'PSRJ2021+4026', 
                     'PSRJ2055+2539', 
                     'PSRJ2124-3358']

pwnlist = cutoff_candidates

ncols = 2
nrows = int(math.ceil(float(len(pwnlist))/ncols))

fig=P.figure(None,figsize=(6,6))


fig.subplots_adjust(hspace=.25,wspace=.25, left=0.15, right=0.9, top=0.9, bottom=0.1)

pwndata=yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_data_lande.yaml')))


off_peak_selection='/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/off_peak/off_peak_bb/pwncat2/v1'


for i,pwn in enumerate(pwnlist):
    axes=fig.add_subplot(nrows,ncols,i+1)

    results=j(off_peak_selection,pwn,'results_%s.yaml' % pwn)
    if not exists(results): continue
    y=yaml.load(open(results))
    bb_phase=PhaseRange(*y['bayesian_blocks']['off_peak'])

    xx=np.asarray(y['bayesian_blocks']['xx'])
    yy=np.asarray(y['bayesian_blocks']['yy'])

    ft1 = pwndata[pwn]['ft1']

    emin = y['emin']
    emax = y['emax']
    rad = y['rad']

    skydir = SkyDir(*pwndata[pwn]['cel'])
    ft1=pwndata[pwn]['ft1']

    linewidth = 0.5
    nbins=50
    bins=np.linspace(0,1,nbins+1)
    binsz = bins[1]-bins[0]

    if not args.fast:

        phases = get_phases(ft1, skydir, emin, emax, rad)

        counts,bins=np.histogram(phases,bins=bins)
        x = np.asarray(zip(bins[:-1],bins[1:])).flatten()
        y = np.asarray(zip(counts,counts)).flatten()

        x,y = np.append(x, x+1), np.append(y, y)

        P.plot(x,y, lw=linewidth, color='black' if bw else 'blue')

    xx, yy = np.append(xx, xx+1), np.append(yy, yy)

    axes.plot(xx,yy*binsz, color='gray' if bw else 'red', lw=linewidth)

    axes.set_ylim(ymin=0)
    axes.set_ylim(ymax=axes.get_ylim()[1]*1.5)
    axes.set_xlim(0,2)

    # from http://matplotlib.sourceforge.net/faq/howto_faq.html#align-my-ylabels-across-multiple-subplots
    axes.yaxis.set_label_coords(-0.25,0.5)

    y,x = np.unravel_index(i, (nrows,ncols))
    print i, (nrows, ncols), (x,y)
    if x == 0:
        axes.set_ylabel('Counts')
    if y == nrows-1:
        axes.set_xlabel('Pulsar Phase')

    print i,pwn


    def add_text(text,loc,i):
        letter = chr(i+97)

        _text = '(%s) %s' % (letter, text.replace('PSR','').replace('-','$-$'))

        at = AnchoredText(_text, loc=loc, frameon=False)
        axes.add_artist(at)
        at.txt._text.set_path_effects([withStroke(foreground="w",linewidth=3)])
    add_text(pwn,2,i)

    bb_phase.axvspan(axes=axes, phase_offsets=[0,1], fill=True, edgecolor='none', 
                     linewidth=linewidth, facecolor='0.75')


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

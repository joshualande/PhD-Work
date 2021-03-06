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

from lande.fermi.pulsar.offpeak import plot_phaseogram_blocks

from lande.utilities import pubplot

pubplot.set_latex_defaults()

base='$pwncat2_off_peak_results/v6'

outdir = join(base,'plots')

r=join(base,'analysis')

bw = pubplot.get_bw()

cutoff_candidates = [['PSRJ0007+7303',100],
                     ['PSRJ0205+6449',100],
                     ['PSRJ1410-6132',100],
                     ['PSRJ1747-2958',100],
                     ['PSRJ2021+4026',100],
                     ['PSRJ2124-3358',100]]



pwnlist = cutoff_candidates

ncols = 2
nrows = int(math.ceil(float(len(pwnlist))/ncols))

fig=P.figure(None,figsize=(6,6))

fig.subplots_adjust(hspace=.35,wspace=.35, left=0.15, right=0.9, top=0.9, bottom=0.1)

pwndata=yaml.load(open(expandvars('$pwndata/pwncat2_data_lande.yaml')))

off_peak_results = yaml.load(open(expandvars('$pwndata/pwncat2_phase_lande.yaml')))


for i,(pwn,nbins) in enumerate(pwnlist):
    results = expandvars(join(r,pwn,'results_%s.yaml' % pwn))

    print i,pwn,results

    if not exists(results):
        print '%s does not exist' % results
        continue

    results = yaml.load(open(results))

    ft1 = pwndata[pwn]['ft1']
    skydir = SkyDir(*pwndata[pwn]['cel'])

    axes=fig.add_subplot(nrows,ncols,i+1)

    emin = results['optimal_emin']
    emax = results['emax']
    radius = results['optimal_radius']
    blocks = results['blocks']

    off_peak_phase = off_peak_results[pwn]['phase']

    import pickle
    jd = pickle.load(open('/nfs/farm/g/glast/u55/pulsar/2ndPulsarcatalog/psue/General/josh_dicts.pickle'))
    offset = float(jd[pwn.replace('PSRJ','J')]['shift'])

    print pwn,offset

    plot_phaseogram_blocks(ft1, skydir=skydir, 
                           emin=emin, emax=emax, radius=radius, 
                           phase_range=off_peak_phase, 
                           phase_range_kwargs=dict(color='black', fill=False, alpha=None, hatch='//'),
                           blocks=blocks, 
                           blocks_kwargs=dict(color='grey' if bw else 'red'),
                           nbins=nbins,
                           repeat_phase=False,
                           data_kwargs=dict(color='black', linewidth=0.5),
                           offset=offset,
                           axes=axes)


    axes.set_ylim(ymax=axes.get_ylim()[1]*1.2)

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


pubplot.save(join(outdir,'off_peak_phase'))

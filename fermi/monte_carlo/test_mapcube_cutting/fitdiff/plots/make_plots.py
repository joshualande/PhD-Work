#!/usr/bin/env python
from os.path import expandvars,join
import scipy.stats 
from matplotlib.ticker import MaxNLocator


import numpy as np
import pylab as P

from uw.utilities.makerec import fitsrec

recname = expandvars(join('$fitdiffdata','v4','cached.fits'))

r = fitsrec(recname)


plot_pull=True
#plot_pull=False

pointlike=True
#pointlike=False

if pointlike:
    print 'pointlike'
    norm=r['pointlike_norm']
    norm_err=r['pointlike_norm_err']
    norm_mc =r['pointlike_norm_mc']
else:
    print 'gtlike'
    norm=r['gtlike_norm']
    norm_err=r['gtlike_norm_err']
    norm_mc =r['gtlike_norm_mc']

if plot_pull:
    pull = (norm - norm_mc)/norm_err
else:
    percent = (norm  - norm_mc)/norm_mc

difftype=np.char.strip(r['difftype'])
location=np.char.strip(r['location'])
emin=r['emin']
emax=r['emax']
l=r['l']
b=r['b']

print difftype, location

P.figure(None,(8,8))

for i,_difftype,_emin,_emax in [
    [0, 'galactic', 1e2, 1e5], [1, 'galactic', 1e4, 1e5],
    [2, 'isotropic',1e2, 1e5], [3, 'isotropic',1e4, 1e5], 
    [4, 'sreekumar',1e2, 1e5], [5, 'sreekumar',1e4, 1e5]]:

    cut = (difftype==_difftype)&(emin==_emin)&(emax==_emax)

    ax = P.subplot(3,2,i+1)
    P.title('%s %g-%g MeV' % (_difftype, _emin, _emax))

    for _location in ['lowlat', 'highlat']:
    #for _location in ['lowlat']:
        good_cut = cut & (location==_location)


        if plot_pull:
            _pull = pull[good_cut]

            print _difftype,_emin,_emax,_location,len(_pull)
            if len(_pull) < 1: continue

            P.hist(_pull, label=_location, histtype='step', normed=True)
        else:
            _percent = percent[good_cut]

            print _difftype,_emin,_emax,_location,len(_percent)
            if len(_percent) < 1: continue

            P.hist(_percent, label=_location, histtype='step', normed=True)

    if plot_pull:
        low, up = ax.get_xlim()
        x = np.linspace(low, up, 100)
        P.plot(x,scipy.stats.norm.pdf(x))

    ax.xaxis.set_major_locator(MaxNLocator(4))


    if plot_pull:
        P.xlabel('pull')
    else:
        P.xlabel('percent error')

    P.legend()

P.subplots_adjust(wspace=0.4, hspace=0.4)

if plot_pull:
    if pointlike:
        P.savefig('plot_pulls_pointlike.pdf')
    else:
        P.savefig('plot_pulls_gtlike.pdf')
else:
    if pointlike:
        P.savefig('plot_percent_pointlike.pdf')
    else:
        P.savefig('plot_percent_gtlike.pdf')

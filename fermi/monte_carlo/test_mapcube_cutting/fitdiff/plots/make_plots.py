#!/usr/bin/env python
from os.path import expandvars,join
import scipy.stats 
from matplotlib.ticker import MaxNLocator


import numpy as np
import pylab as P


from lande.utilities.pubplot import set_latex_defaults
set_latex_defaults()

from lande.utilities.save import loaddict


name = expandvars(join('$fitdiffdata','v11','merged.hdf5'))
r = loaddict(name)

#plot_pull=True
plot_pull=False

#pointlike=True
pointlike=False

if pointlike:
    print 'pointlike'
    norm=np.asarray(r['pointlike_norm'])
    norm_err=np.asarray(r['pointlike_norm_err'])
    norm_mc=np.asarray(r['pointlike_norm_mc'])
else:
    print 'gtlike'
    norm=np.asarray(r['gtlike_norm'])
    norm_err=np.asarray(r['gtlike_norm_err'])
    norm_mc=np.asarray(r['gtlike_norm_mc'])

if plot_pull:
    pull = (norm - norm_mc)/norm_err
else:
    percent = (norm  - norm_mc)/norm_mc

difftype=np.char.strip(r['difftype'])
position=np.char.strip(r['position'])
emin=np.asarray(r['emin'])
emax=np.asarray(r['emax'])

print difftype, position

P.figure(None,(8,8))

for i,_difftype,_emin,_emax in [
    [0, 'galactic', 1e2, 1e5], [1, 'galactic', 1e4, 1e5],
    [2, 'isotropic',1e2, 1e5], [3, 'isotropic',1e4, 1e5], 
    [4, 'sreekumar',1e2, 1e5], [5, 'sreekumar',1e4, 1e5]]:

    cut = (difftype==_difftype)&(emin==_emin)&(emax==_emax)

    ax = P.subplot(3,2,i+1)
    P.title('%s %g-%g MeV' % (_difftype, _emin, _emax))

    for _position in ['lowlat', 'highlat' , 'galcenter', ]:
    #for _position in [ 'galcenter' ]:
        good_cut = cut & (position==_position)

        if plot_pull:
            _pull = pull[good_cut]

            print _difftype,_emin,_emax,_position,'num=',len(_pull)
            if len(_pull) < 1: continue

            P.hist(_pull, label=_position, histtype='step', normed=True)
        else:
            _percent = percent[good_cut]

            print _difftype,_emin,_emax,_position,len(_percent)
            if len(_percent) < 1: continue

            P.hist(_percent, label=_position, histtype='step', normed=True)

    if plot_pull:
        low, up = ax.get_xlim()
        x = np.linspace(low, up, 100)
        P.plot(x,scipy.stats.norm.pdf(x))

    ax.xaxis.set_major_locator(MaxNLocator(4))

    if plot_pull:
        P.xlabel('pull')
    else:
        P.xlabel('percent error')

    if i ==5:
        P.legend()

P.subplots_adjust(wspace=0.4, hspace=0.4)

if plot_pull:
    if pointlike:
        P.savefig('plot_pulls_pointlike.pdf')
        P.savefig('plot_pulls_pointlike.png')
    else:
        P.savefig('plot_pulls_gtlike.pdf')
        P.savefig('plot_pulls_gtlike.png')
else:
    if pointlike:
        P.savefig('plot_percent_pointlike.pdf')
        P.savefig('plot_percent_pointlike.png')
    else:
        P.savefig('plot_percent_gtlike.pdf')
        P.savefig('plot_percent_gtlike.png')

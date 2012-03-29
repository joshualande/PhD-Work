import numpy as np
import pylab as P
from pywcsgrid2.allsky_axes import make_allsky_axes_from_header
import matplotlib.pyplot as plt

from uw.like.roi_monte_carlo import MonteCarlo

from lande.utilities.save import loaddict

nphi = 0

def overlay(ax):
    results = loaddict('$simpsdata/v6/merged.hdf5')

    flux = np.asarray(results['flux_gtlike'])
    flux_err = np.asarray(results['flux_gtlike_err'])

#    flux = np.asarray(results['flux_pointlike'])
#    flux_err = np.asarray(results['flux_pointlike_err'])

    flux_mc = np.asarray(results['flux_mc'])
    glon = np.asarray(results['glon'])
    glat = np.asarray(results['glat'])
    ra = np.asarray(results['ra'])
    dec = np.asarray(results['dec'])
    phibins = np.asarray(results['phibins'])

    pull = (flux-flux_mc)/flux_err
    perr = (flux-flux_mc)/flux_mc

    pull=pull[phibins == nphi]
    perr=perr[phibins == nphi]

    maxerr = 0.03
    print 'max',maxerr
    color_mapper=lambda perr: (min(perr/maxerr,1),0,0) if perr > 0 else (0,0,min(np.abs(perr)/maxerr,1))

    for _glon, _glat, _perr in zip(glon, glat, perr):
        ax['gal'].plot([_glon],[_glat], marker='o', color=color_mapper(_perr), markersize=5)

fig = P.figure(None, figsize=(8, 5))

def plot(galactic, rect):

    pf = MonteCarlo.make_allsky_isotropic_pyfits(galactic=galactic, proj='AIT')
    h,d=pf[0].header,pf[0].data
    ax = make_allsky_axes_from_header(fig, rect=rect, header=h, lon_center=0.)
    im = ax.imshow(pf[0].data, origin="lower", cmap=plt.cm.gray_r)
    ax.grid()
    overlay(ax)

plot(True, 211)
plot(False, 212)

P.savefig('allsky_skymap_phibins_%s.pdf' % nphi)


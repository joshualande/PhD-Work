import numpy as np
import pylab as P
from pywcsgrid2.allsky_axes import make_allsky_axes_from_header
import matplotlib.pyplot as plt

from uw.like.roi_monte_carlo import MonteCarlo

from lande.utilities.save import loaddict

nphi = 0

def overlay(ax):
    #results = loaddict('$simsrcdata/v12/merged.hdf5')

#    flux = np.asarray(results['flux_gtlike'])
#    flux_err = np.asarray(results['flux_gtlike_err'])

    #results = loaddict('$simsrcdata/v11/sim_flux_1e-06_position_allsky_phibins_0_spatial_point_emin_100_emax_100000_time_2years/merged.hdf5')

    #results = loaddict('$simsrcdata/v11/sim_flux_1e-06_position_allsky_phibins_0_spatial_point_emin_100_emax_100000_time_2fgl/merged.hdf5')

    #results = loaddict('$simsrcdata/v11/sim_flux_1e-06_position_allsky_phibins_0_spatial_point_emin_100_emax_100000_time_2years/merged.hdf5')
    #results = loaddict('$simsrcdata/v15/merged.hdf5')
    results = loaddict('$simsrcdata/v15/merged.hdf5')

    flux = np.asarray(results['flux_pointlike'])
    flux_err = np.asarray(results['flux_pointlike_err'])

    flux_mc = np.asarray(results['flux_mc'])
    glon = np.asarray(results['glon'])
    glat = np.asarray(results['glat'])
    ra = np.asarray(results['ra'])
    dec = np.asarray(results['dec'])
    phibins = np.asarray(results['phibins'])
    time = np.asarray(results['time'])

    pull = (flux-flux_mc)/flux_err
    perr = (flux-flux_mc)/flux_mc

    cut = (phibins == nphi)&(time=='2fgl')

    pull=pull[cut]
    perr=perr[cut]
    glon=glon[cut]
    glat=glat[cut]

    maxerr = 0.05
    print 'max',maxerr
    color_mapper=lambda perr: (min(perr/maxerr,1),0,0) if perr > 0 else (0,0,min(np.abs(perr)/maxerr,1))

    for _glon, _glat, _perr in zip(glon, glat, perr):
        ax['gal'].plot([_glon],[_glat], marker='o', color=color_mapper(_perr), markersize=10)

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


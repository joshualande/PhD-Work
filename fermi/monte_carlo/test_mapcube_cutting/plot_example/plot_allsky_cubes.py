from uw.utilities import colormaps
from os.path import join
import matplotlib
import pylab as P
import pyfits

from pywcsgrid2.allsky_axes import make_allsky_axes_from_header

def plot_allsky(fig, pyfits, label, imshow_kwargs=dict(), **kwargs):

    data = p[0].data
    if len(p[0].data.shape) == 3:
        data = data.sum(axis=0)
    print data.shape
    header = p[0].header


    ax = make_allsky_axes_from_header(fig, header=header, lon_center=0, **kwargs)

    ax.imshow(data, origin="lower", cmap=colormaps.b, **imshow_kwargs)

    P.title(label)

    return ax
 

fig = P.figure(None, figsize=(8,5))

fig.subplots_adjust(wspace=0.3, hspace=0.2)

base='/nfs/slac/g/ki/ki03/lande/fermi/data/monte_carlo/test_mapcube_cutting/plot_example/'

p=pyfits.open(join(base,"datadir_l_0_b_0/isotrop_2year_P76_source_v0_spatial.fits"))
ax=plot_allsky(fig,p,rect=221, imshow_kwargs=dict(vmax=1e-30), label='Isotropic (l,b)=0,0' )

p=pyfits.open(join(base,"datadir_l_0_b_0/ring_2year_P76_v0_cut.fits"))
p[0].header['CDELT1'] = -0.125
p[0].data = p[0].data[:,:,::-1]
ax=plot_allsky(fig,p,rect=223, imshow_kwargs=dict(vmin=1e-10, vmax=5e-7), label='Galactic (l,b)=0,0')

p=pyfits.open(join(base,"datadir_l_69_b_84/isotrop_2year_P76_source_v0_spatial.fits"))
ax=plot_allsky(fig,p,rect=222, imshow_kwargs=dict(vmax=1e-30), label='Isotropic (l,b)=69,84') 

p=pyfits.open(join(base,"datadir_l_69_b_84/ring_2year_P76_v0_cut.fits"))
p[0].header['CDELT1'] = -0.125
p[0].data = p[0].data[:,:,::-1]
ax=plot_allsky(fig,p,rect=224, label='Galactic (l,b)=69,84') 

P.savefig('allsky_cubes.pdf')
P.savefig('allsky_cubes.png')


from os.path import join

from skymaps import SkyDir

from uw.like.pointspec_helpers import get_default_diffuse
from uw.like.roi_monte_carlo import MonteCarlo

from lande.fermi.likelihood.diffuse import get_background

if difftype == 'gal':
    return get_background('/afs/slac/g/glast/groups/diffuse/rings/2year/ring_2year_P76_v0.fits
elif difftype == 'iso':
    return get_background('/afs/slac/g/glast/groups/diffuse/rings/2year/isotrop_2year_P76_source_v0.txt
elif difftype == 'plaw'


#diffuse = diffuse[1:]

catalog_basedir = "/afs/slac/g/glast/groups/catalog/P7_V4_SOURCE"
ft2 = join(catalog_basedir,"ft2_2years.fits")
ltcube = join(catalog_basedir,"ltcube_24m_pass7.4_source_z100_t90_cl0.fits")

savedir='savedir'

ft1 = join(savedir,'ft1.fits')

emin=1e2
emax=1e3

#skydir=SkyDir(125,75,SkyDir.GALACTIC)
skydir=SkyDir(55,85,SkyDir.GALACTIC)

print 'simulating'

mc=MonteCarlo(
    savedir=savedir,
    sources=diffuse,
    seed=0,
    irf='none',
    ft1=ft1,
    ft2=ft2,
    roi_dir=skydir,
    maxROI=10,
    emin=emin,
    emax=emax,
    gtifile=ltcube)
mc.simulate()



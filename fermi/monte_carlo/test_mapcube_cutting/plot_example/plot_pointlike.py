from lande.fermi.data.catalogs import dict2fgl
import numpy as np
from os.path import join
from skymaps import SkyDir
from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.pointspec_helpers import get_default_diffuse

for roi_dir in [SkyDir(0,0, SkyDir.GALACTIC), SkyDir(70,85, SkyDir.GALACTIC)]:
        
    base='/nfs/slac/g/ki/ki03/lande/fermi/data/monte_carlo/test_mapcube_cutting/plot_example/'

    extra= 'l_%d_b_%d' % (roi_dir.l(), roi_dir.b())

    savedir=join(base,'datadir_%s' % extra)

    ft1 = join(savedir,'ft1.fits')
    binfile = join(savedir,'binned.fits')

    ft2 = dict2fgl['ft2']
    ltcube = dict2fgl['ltcube']

    ds = DataSpecification(
        ft1files = ft1,
        ft2files = ft2,
        ltcube = ltcube,
        binfile = binfile)

    emin=1e3
    emax=1e5

    sa = SpectralAnalysis(ds,
        emin = emin,
        emax = emax,
        irf='P7SOURCE_V6',
        roi_dir=roi_dir,
        minROI=10,
        maxROI=10,
        event_class=0
    )

    diffdir='/afs/slac/g/glast/groups/diffuse/rings/2year/'

    diffuse_sources = get_default_diffuse(diffdir=diffdir, 
                                          gfile='ring_2year_P76_v0.fits',
                                          ifile='isotrop_2year_P76_source_v0.txt')

    roi = sa.roi(roi_dir=roi_dir, diffuse_sources = diffuse_sources)

    roi.plot_counts_map(filename='counts_map_%s.png' % extra, size=10*np.sqrt(2), pixelsize=0.5)

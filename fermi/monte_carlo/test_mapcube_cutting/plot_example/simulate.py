#!/usr/bin/env python

from os.path import join

from skymaps import SkyDir

from uw.like.roi_monte_carlo import MonteCarlo
from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.pointspec_helpers import get_default_diffuse

from lande.fermi.data.catalogs import dict2fgl
from lande.fermi.likelihood.save import diffusedict, skydirdict
from lande.utilities.random import random_on_sphere
from lande.utilities.tools import savedict



for roi_dir in [SkyDir(0,0, SkyDir.GALACTIC), SkyDir(70,85, SkyDir.GALACTIC)]:
    
    savedir='/nfs/slac/g/ki/ki03/lande/fermi/data/monte_carlo/test_mapcube_cutting/plot_example/datadir_l_%d_b_%d' % (roi_dir.l(), roi_dir.b())

    emin=1e3
    emax=1e5

    diffdir='/afs/slac/g/glast/groups/diffuse/rings/2year/'

    diffuse_sources = get_default_diffuse(diffdir=diffdir, 
                                          gfile='ring_2year_P76_v0.fits',
                                          ifile='isotrop_2year_P76_source_v0.txt')


    ft2 = dict2fgl['ft2']
    ltcube = dict2fgl['ltcube']


    ft1 = join(savedir,'ft1.fits')
    m=MonteCarlo(
        sources=diffuse_sources,
        emin = emin,
        emax = emax,
        irf='P7SOURCE_V6',
        roi_dir=roi_dir,
        maxROI=10,
        seed=0,
        ft1=ft1,
        ft2=ft2,
        gtifile = ltcube,
        savedir=savedir)
    m.simulate()

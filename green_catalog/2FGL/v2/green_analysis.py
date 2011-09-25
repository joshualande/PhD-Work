#!/usr/bin/env python
import os

from lande_roi import *

from green_catalog import GreenCatalog
from argparse import ArgumentParser

def build_roi(name):

    folder=os.path.join(os.path.expandvars('$GREENCAT'),name,'v1')

    green_cat=GreenCatalog('$FERMI/catalogs/Green_cat.fits')
    skydir=green_cat.get_skydir(name)

    ds=DataSpecification(
        ft1files=[i.strip() for i in open(e('$FERMI/data/2FGL_P7v4/24m_pass7.4_source_z100_t90_cl0.lst')).readlines()],
        binfile='$FERMI/data/2FGL_P7v4/binned_24m_pass7.4_source_z100_t90_cl0.fits',
        ft2files='$FERMI/data/2FGL_P7v4/ft2_2years.fits',
        ltcube='$FERMI/data/2FGL_P7v4/ltcube_24m_pass7.4_source_z100_t90_cl0.fits')

    sa=SpectralAnalysis(ds,
            binsperdec = 4,
            roi_dir    = skydir,
            irf        = 'P7SOURCE_V6',
            maxROI     = 10,
            minROI     = 10,
            event_class = -1)

    roi = sa.roi(
        catalogs = Catalog2FGL('$FERMI/catalogs/gll_psc_v04.fit',
                              latextdir='$FERMI/extended_archives/Extended_archive_v10'),
        diffuse_sources = get_default_diffuse(
            diffdir=os.path.expandvars('$FERMI/diffuse'),
            gfile='ring_2year_P76_v0.fits',
            ifile='isotrop_2year_P76_source_v0.txt'),
        fit_emin = 1e4, fit_emax = 1e5
        )

    if not os.path.exists(folder):
        os.makedirs(folder)

    roi.save(os.path.join(folder,'roi_%s.dat' % name))


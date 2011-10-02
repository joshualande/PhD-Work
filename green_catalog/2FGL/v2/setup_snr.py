#!/usr/bin/env python
import yaml
from os.path import expandvars as e

from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.pointspec_helpers import get_default_diffuse, PointSource
from uw.like.roi_catalogs import Catalog2FGL
from uw.like.roi_extended import ExtendedSource
from uw.like.Models import PowerLaw
from uw.like.SpatialModels import Disk

from argparse import ArgumentParser
from skymaps import SkyDir

def setup_snr(name, snrdata, **kwargs):
    """ Creates the ROI + adds in the SNR. """
    roi=setup_roi(name, snrdata, **kwargs)

    roi.add_source(get_snr(name, snrdata))
    return roi

def setup_roi(name, snrdata, free_radius=2, fit_emin=1e4, fit_emax=1e5):

    snr=yaml.load(open(snrdata))[name]
    skydir=SkyDir(*snr['cel'])
    size=snr['size']

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
            event_class = 0)


    diffuse_sources = diffuse_sources = get_default_diffuse(
        diffdir=e('$FERMI/diffuse'),
        gfile='ring_2year_P76_v0.fits',
        ifile='isotrop_2year_P76_source_v0.txt')

    catalogs = Catalog2FGL('$FERMI/catalogs/gll_psc_v05.fit',
                           latextdir='$FERMI/extended_archives/gll_psc_v05_templates/',
                           free_radius=free_radius)

    roi = sa.roi(
        catalogs = catalogs,
        diffuse_sources = diffuse_sources,
        fit_emin = fit_emin, 
        fit_emax = fit_emax
        )

    return roi

def get_snr(name, snrdata, point_like=False):

    snr=yaml.load(open(snrdata))[name]
    skydir=SkyDir(*snr['cel'])
    radius=snr['radius']
    model=PowerLaw(index=2)

    if point_like:
        return PointSource(
            name=name,
            model=model,
            skydir=skydir
            )
    else:
        return ExtendedSource(
            name=name,
            model=model,
            spatial_model=Disk(
                sigma=radius,
                center=skydir
                )
            )

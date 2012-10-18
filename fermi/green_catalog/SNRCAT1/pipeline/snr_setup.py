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

def setup_snr(name, snrdata, pointlike, **kwargs):
    """ Creates the ROI + adds in the SNR. """
    roi=setup_roi(name, snrdata, **kwargs)

    roi.add_source(get_snr(name, snrdata, pointlike))
    return roi

def setup_roi(name, snrdata, catalog_dict=dict(), roi_dict=dict()):

    snr=yaml.load(open(snrdata))[name]
    skydir=SkyDir(*snr['cel'])
    size=snr['size']

    ds=DataSpecification(
        ft1files='$FERMILANDE/data/PWNCAT2/nov_30_2011/ft1_PWNCAT2_allsky.fits',
        ft2files='$FERMILANDE/data/PWNCAT2/nov_30_2011/ft2_PWNCAT2_allsky.fits',
        ltcube='$FERMILANDE/data/PWNCAT2/nov_30_2011/ltcube_PWNCAT2_allsky.fits',
        binfile='$FERMILANDE/data/PWNCAT2/nov_30_2011/binned_%s.fits' % 4)

    sa=SpectralAnalysis(ds,
            binsperdec = 4,
            roi_dir    = skydir,
            irf        = 'P7SOURCE_V6',
            maxROI     = 10,
            minROI     = 10,
            event_class = 0)


    diffuse_sources = diffuse_sources = get_default_diffuse(
        diffdir=e('$FERMILANDE/diffuse'),
        gfile='ring_2year_P76_v0.fits',
        ifile='isotrop_2year_P76_source_v0.txt')

    catalogs = Catalog2FGL('$FERMILANDE/catalogs/gll_psc_v05.fit',
                           latextdir='$FERMILANDE/extended_archives/gll_psc_v05_templates/',
                           **catalog_dict)

    roi = sa.roi(
        catalogs = catalogs,
        diffuse_sources = diffuse_sources, 
        **roi_dict)

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

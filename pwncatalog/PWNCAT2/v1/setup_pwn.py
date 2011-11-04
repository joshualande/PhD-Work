#!/usr/bin/env python
import yaml
import os
from glob import glob
from os.path import expandvars as e, join as j
from tempfile import mkdtemp
import numbers

import numpy as np

from skymaps import SkyDir

from uw.like.pointspec import SpectralAnalysis
from uw.like.pointspec_helpers import get_default_diffuse, PointSource, FermiCatalog
from uw.like.SpatialModels import Gaussian
from uw.like.roi_catalogs import Catalog2FGL
from uw.like.roi_extended import ExtendedSource
from uw.like.Models import PowerLaw
from uw.utilities import phasetools
from uw.pulsar.phase_range import PhaseRange

def setup_pwn(name, pwndata, fit_emin, fit_emax, extended=False, **kwargs):

    source = get_source(name,pwndata, fit_emin, fit_emax, extended=False)
    if isinstance(source,PointSource):
        ps,ds = [source],[]
    else:
        ps,ds = [],[source]

    roi = setup_region(name, pwndata, 
                       fit_emin=fit_emin, 
                       fit_emax=fit_emax, 
                       point_sources = ps,
                       diffuse_sources = ds,
                       **kwargs)
    return roi

def get_source(name, pwndata, fit_emin, fit_emax, extended=False):
    sources=yaml.load(open(pwndata))
    pulsar_position=SkyDir(*sources[name]['cel'])
    model=PowerLaw(index=2, e0=np.sqrt(fit_emin*fit_emax))
    model.set_flux(
        PowerLaw(norm=1e-11, index=2).i_flux(fit_emin,fit_emax),
        fit_emin,fit_emax)

    if extended:
        return ExtendedSource(
            name=name,
            model=model,
            spatial_model=Gaussian(sigma=0.1,center=pulsar_position))
    else:
        return PointSource(
            name=name,
            model=model,
            skydir=pulsar_position)

def get_catalog(free_radius,max_free):
    return Catalog2FGL('$FERMI/catalogs/gll_psc_v05.fit', 
                       latextdir='$FERMI/extended_archives/gll_psc_v05_templates',
                       free_radius=free_radius,
                       max_free = max_free)

def setup_region(name,pwndata, phase, free_radius, max_free, 
                 roi_size=10, savedir=None, binsperdec=4,
                 point_sources=[], diffuse_sources=[],
                 **kwargs):
    """Name of the source
    pwndata Yaml file
    
    returns pointlike ROI.
    """

    if savedir is None: 
        savedir=mkdtemp(prefix='/scratch/')
    elif not os.path.exists(savedir):
        os.makedirs(savedir)
    else:
        for file in glob(j(savedir,'*')):
            os.remove(file)


    phase = PhaseRange(phase)

    sources=yaml.load(open(pwndata))

    ltcube=sources[name]['ltcube']

    pulsar_position=SkyDir(*sources[name]['cel'])
    ft2=sources[name]['ft2']
    ft1=sources[name]['ft1']

    diffuse_sources += get_default_diffuse(diffdir="/afs/slac/g/glast/groups/diffuse/rings/2year",
                                          gfile="ring_2year_P76_v0.fits",
                                          ifile="isotrop_2year_P76_source_v0.txt")

    catalog=FermiCatalog(e("$FERMI/catalogs/gll_psc_v02.fit"))

    catalog=get_catalog(free_radius,max_free)

    binfile=j(savedir,'binned_phased.fits')

    if np.allclose(phase.phase_fraction,1):
        phased_ltcube = ltcube
        phased_ft1 = ft1
    else:
        # create a temporary ltcube scaled by the phase factor
        phased_ltcube=j(savedir,'phased_ltcube.fits')
        if not os.path.exists(phased_ltcube):
            phasetools.phase_ltcube(ltcube,phased_ltcube, phase=phase)

        # apply phase cut to ft1 file
        phased_ft1 = j(savedir,'ft1_phased.fits')
        if not os.path.exists(phased_ft1):
            phasetools.phase_cut(ft1,phased_ft1,phaseranges=phase.tolist(dense=False))

    from uw.like.pointspec import DataSpecification
    ds = DataSpecification(
        ft1files = phased_ft1,
        ft2files = ft2,
        ltcube   = phased_ltcube,
        binfile  = binfile)

    print 'For now, 4 bins per decade. Eventually, this will have to be better.'
    sa = SpectralAnalysis(ds,
                          binsperdec = binsperdec,
                          emin       = 100,
                          emax       = 1000000,
                          irf        = "P7SOURCE_V6",
                          roi_dir    = pulsar_position,
                          maxROI     = roi_size,
                          minROI     = roi_size)

    roi=sa.roi(point_sources=point_sources,
               diffuse_sources=diffuse_sources,
               catalogs=catalog,
               phase_factor=1,
               **kwargs)

    print 'bins ',roi.bin_edges

    return roi

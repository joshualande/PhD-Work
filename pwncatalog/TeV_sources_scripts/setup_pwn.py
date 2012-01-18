#!/usr/bin/env python
import yaml
import numbers
import os
from glob import glob
from os.path import expandvars as e, join as j
from tempfile import mkdtemp
import numbers

import numpy as np

from skymaps import SkyDir

from uw.like.pointspec import SpectralAnalysis
from uw.like.pointspec_helpers import get_default_diffuse, PointSource
from uw.like.SpatialModels import Gaussian, EllipticalGaussian
from uw.like.roi_catalogs import Catalog2FGL, FermiCatalog
from uw.like.roi_extended import ExtendedSource
from uw.like.Models import PowerLaw
from uw.utilities import phasetools
from uw.pulsar.phase_range import PhaseRange
from uw.like.SpatialModels import SpatialMap
isnum = lambda x: isinstance(x, numbers.Real)

def setup_tev(name, tevsources, ft1,ft2,ltcube,fit_emin, fit_emax, extended=False, **kwargs):
    """ Sets up the ROI for studying a TeV Source. """
    tev=yaml.load(open(tevsources))
    source=tev[name]
    ra,dec=source['cel']
    tev_position=SkyDir(ra,dec)
    binsperdec=4
    binfile=e('/afs/slac/g/glast/users/rousseau/TeV_sources/bexpmap/binned_%sbpd_%s.fits' %(binsperdec,name))

    source2=yaml.load(open("/afs/slac/g/glast/users/rousseau/TeV_sources/scripts/tevdata/tev_galactic_sources.yaml"))
    
    #parse the extension
    ext=source2[name]['ext']
    print ext
    if isnum(ext):
        sigma = ext
        angle=0
        template = None
    elif isinstance(ext, list) and len(ext) == 3 and isnum(ext[0]) and isnum(ext[1]) and isnum(ext[2]):
        sigma = [ext[0],ext[1]]
        angle=ext[2]
        template=source2[name]['template']
    elif ext == '?':
        sigma = 0 # best we can do since no published size
        template = None
    else:
        raise Exception("Unrecogized size %g" % sigma)

    source = get_source(name, 
                        fit_emin=fit_emin, 
                        fit_emax=fit_emax, 
                        position = tev_position, sigma = sigma, angle=angle, template=template,
                        extended=extended)

    roi = setup_region(name, 
                       phase = PhaseRange(0,1),
                       ft1=ft1, 
                       ft2=ft2, 
                       ltcube=ltcube, 
                       binsperdec=binsperdec,
                       binfile=binfile,
                       roi_dir=tev_position,
                       fit_emin=fit_emin, 
                       fit_emax=fit_emax, 
                       sources = [source],
                       savedir = None,
                       **kwargs)
    return roi

def setup_pwn(name, pwndata, fit_emin, fit_emax, extended=False,catalog_name="None", **kwargs):
    """ Sets up the ROI for studying a LAT Pulsar in the off pulse. """

    sourcedict=yaml.load(open(pwndata))[name]
    ltcube=sourcedict['ltcube']
    pulsar_position=SkyDir(*sourcedict['cel'])
    ft1=sourcedict['ft1']
    ft2=sourcedict['ft2']

    source = get_source(name, 
                        fit_emin = fit_emin, 
                        fit_emax = fit_emax, 
                        position = pulsar_position,
                        sigma = 0.1,
                        extended=extended)

    roi = setup_region(name, 
                       ft1=ft1, 
                       ft2=ft2, 
                       ltcube=ltcube, 
                       roi_dir=pulsar_position,
                       fit_emin=fit_emin, 
                       fit_emax=fit_emax,
                       catalog_name=catalog_name,
                       sources = [source],
                       **kwargs)
    return roi

def get_source(name, position, 
               fit_emin, fit_emax, 
               extended=False, sigma=None, angle=None, template=None):
    """ build a souce. """
    model=PowerLaw(index=2, e0=np.sqrt(fit_emin*fit_emax))
    flux=PowerLaw(norm=1e-11, index=2, e0=1e3).i_flux(fit_emin,fit_emax)
    model.set_flux(flux,fit_emin,fit_emax)
    
    if extended and sigma!=0:
        if isnum(sigma):
            return ExtendedSource(
                name=name,
                model=model,
                spatial_model=Gaussian(sigma=sigma, center=position))
        elif len(sigma)==2:
            return ExtendedSource(
                name=name,
                model=model,
                spatial_model=SpatialMap(file=template))
    else:
        return PointSource(
            name=name,
            model=model,
            skydir=position)

def get_catalog(**kwargs):
    return Catalog2FGL('$FERMI/catalogs/gll_psc_v05.fit', 
                       latextdir='$FERMI/extended_archives/gll_psc_v05_templates',
                       prune_radius=0,
                       **kwargs)

def setup_region(name, phase,
                 ft1, ft2, ltcube, roi_dir,
                 free_radius, max_free, binsperdec,
                 catalog_name="None",
                 roi_size=10, savedir=None, 
                 sources = [], # list of point+diffuse sources 
                 binfile = None,
                 **kwargs):
    """ Create a pointlike ROI. """

    if savedir is None: 
        savedir=mkdtemp(prefix='/scratch/')
    elif not os.path.exists(savedir):
        os.makedirs(savedir)
    else:
        for file in glob(j(savedir,'*')):
            os.remove(file)

    phase = PhaseRange(phase)

    point_sources, diffuse_sources = [],[]
    for source in sources:
        if isinstance(source,PointSource):
            point_sources.append(source)
        else:
            diffuse_sources.append(source)

    diffuse_sources += get_default_diffuse(diffdir="/afs/slac/g/glast/groups/diffuse/rings/2year",
                                          gfile="ring_2year_P76_v0.fits",
                                          ifile="isotrop_2year_P76_source_v0.txt")

#    catalog=FermiCatalog(e("$FERMI/catalogs/gll_psc18month_uw10_assoc.fits"))

    catalog=get_catalog(free_radius=free_radius,max_free=max_free)

    if binfile is None: binfile=j(savedir,'binned_phased.fits')

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
                          roi_dir    = roi_dir,
                          maxROI     = roi_size,
                          minROI     = roi_size,
#                          tstart=239500801,
#                          tstop=282614402,
                          event_class= 2)

    roi=sa.roi(point_sources=point_sources,
               diffuse_sources=diffuse_sources,
               catalogs=catalog,
               phase_factor=1,
               **kwargs)
    print roi
    try :
        if catalog_name!="None":
            roi.del_source(catalog_name)
    except :
        print "nom catalog pas trouve"

    print 'bins ',roi.bin_edges

    return roi

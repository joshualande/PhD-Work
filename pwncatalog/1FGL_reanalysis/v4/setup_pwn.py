#!/usr/bin/env python
import yaml
from os.path import expandvars as e, join as j
import numbers
from tempfile import mkdtemp

import numpy as np
import pyfits

from skymaps import SkyDir

from uw.like.pointspec import SpectralAnalysis
from uw.like.pointspec_helpers import get_default_diffuse, PointSource, FermiCatalog
from uw.like.SpatialModels import Gaussian
from uw.like.roi_catalogs import Catalog2FGL
from uw.like.roi_extended import ExtendedSource
from uw.like.Models import PowerLaw
from uw.utilities import phasetools
from uw.pulsar.phase_range import PhaseRange

def phase_ltcube(ltcube,outputfile,phase,phase_col_name='PULSE_PHASE'):
    """ Scale ltcube """

    from numpy import array
    ltcube = pyfits.open(ltcube)
    cb=ltcube['exposure'].data.field('cosbins')
    cb*=phase.phase_fraction

    ltcube.writeto(outputfile,clobber=True)
    ltcube.close()


def setup_pwn(name, pwndata, *args, **kwargs):

    roi = setup_region(name, pwndata, *args, **kwargs)
    # keep overall flux of catalog source,
    # but change the starting index to 2.
    roi.add_source(get_source(name,pwndata))
    return roi

def get_source(name,pwndata, extended=False):
    sources=yaml.load(open(pwndata))
    pulsar_position=SkyDir(*sources[name]['dir'])
    model=PowerLaw(norm=1e-11, index=2)

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

def setup_region(name,pwndata,phase, free_radius=5, tempdir=None, maxroi=10,
              xml=None, **kwargs):
    """Name of the source
    pwndata Yaml file
    
    returns pointlike ROI.
    """

    phase = PhaseRange(phase)

    sources=yaml.load(open(pwndata))

    catalog_name=sources[name]['catalog']['2fgl']
    ltcube=sources[name]['ltcube']
    pulsar_position=SkyDir(*sources[name]['dir'])
    ft2=sources[name]['ft2']
    ft1=sources[name]['ft1']


    catalog=FermiCatalog(e("$FERMI/catalogs/gll_psc_v02.fit"))
    catalog=Catalog2FGL('$FERMI/catalogs/gll_psc_v05.fit', 
                        latextdir='$FERMI/extended_archives/gll_psc_v05_templates',
                        free_radius=free_radius)
    catalog_source=catalog.get_source(catalog_name)

    center=catalog_source.skydir

    if tempdir is None: tempdir=mkdtemp(prefix='/scratch/')

    binfile=j(tempdir,'binned_phased.fits')

    if np.allclose(phase.phase_fraction,1):
        phased_ltcube = ltcube
        phased_ft1 = ft1
    else:
        # create a temporary ltcube scaled by the phase factor
        phased_ltcube=j(tempdir,'phased_ltcube.fits')
        phase_ltcube(ltcube,phased_ltcube, phase=phase)

        # apply phase cut to ft1 file
        phased_ft1 = j(tempdir,'ft1_phased.fits')
        phasetools.phase_cut(ft1,phased_ft1,phaseranges=phase.tolist(dense=False))

    from uw.like.pointspec import DataSpecification
    ds = DataSpecification(
        ft1files = phased_ft1,
        ft2files = ft2,
        ltcube   = phased_ltcube,
        binfile  = binfile)

    sa = SpectralAnalysis(ds,
                          binsperdec = 4,
                          emin       = 100,
                          emax       = 100000,
                          irf        = "P6_V11_DIFFUSE",
                          roi_dir    = center,
                          maxROI     = maxroi,
                          minROI     = maxroi)

    if xml is None:
        roi=sa.roi(
            diffuse_sources=get_default_diffuse(diffdir="/afs/slac/g/glast/groups/diffuse/mapcubes",
                                                gfile="gll_iem_v02.fit",
                                                ifile="isotropic_iem_v02.txt"),
            catalogs = catalog,
            phase_factor =1,
            **kwargs)
    else:
        roi=sa.roi_from_xml(
            roi_dir=center,
            xmlfile = xml,
            phase_factor =1,
            **kwargs)

    print 'bins ',roi.bin_edges

    roi.del_source(catalog_name)
        

    return roi

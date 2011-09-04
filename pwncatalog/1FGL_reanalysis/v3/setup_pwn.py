#!/usr/bin/env python
import yaml
from os.path import expandvars as e, join as j

from tempfile import mkdtemp

from uw.like.pointspec import SpectralAnalysis
from uw.like.pointspec_helpers import get_default_diffuse, PointSource, FermiCatalog
from uw.like.SpatialModels import Disk
from uw.like.Models import PowerLaw
from skymaps import SkyDir
from uw.utilities import phasetools

import toolkit

def setup_pwn(name,pwndata,phase_ranges,tempdir=None):
    """Name of the source
    pwndata Yaml file
    
    returns pointlike ROI.
    """

    sources=yaml.load(open(pwndata))

    catalog_name=sources[name]['catalog']
    ltcube=sources[name]['ltcube']
    pulsar_position=SkyDir(*sources[name]['dir'])
    ft2=sources[name]['ft2']
    ft1=sources[name]['ft1']

    # in case no list was passed
    if len(phase_ranges)==2 and isinstance(phase_ranges[0],numbers.Real) and \
       isinstance(phase_ranges[1],numbers.Real):
        phase_ranges = [phase_ranges] 

    phase_factor=toolkit.phase_ranges(phase_ranges)


    catalog=FermiCatalog(e("$FERMI/catalogs/gll_psc_v02.fit"),free_radius=5)
    catalog_source=[i for i in catalog.get_sources(SkyDir(),180) if i.name==catalog_name][0]

    center=catalog_source.skydir

    if tempdir is None: tempdir=mkdtemp()

    binfile=j(tempdir,'binned_phased.fits)

    # apply phase cut to ft1 file
    phased_ft1 = j(tempdir,'ft1_phased.fits')
    phasetools.phase_cut(ft1,phased_ft1,phaseranges=phase_ranges)

    # create a temporary ltcube scaled by the phase factor
    phased_ltcube=j(tempdir,'phased_ltcube.fits')
    toolkit.phase_ltcube(ltcube,phased_ltcube, phase_ranges=phase_ranges)

    from uw.like.pointspec import DataSpecification
    data_specification = DataSpecification(
                         ft1files = phased_ft1,
                         ft2files = ft2,
                         ltcube   = phased_ltcube,
                         binfile  = binfile)

    spectral_analysis = SpectralAnalysis(data_specification,
                                         binsperdec = 4,
                                         emin       = 100,
                                         emax       = 100000,
                                         irf        = "P6_V3_DIFFUSE",
                                         roi_dir    = center,
                                         maxROI     = 10,
                                         minROI     = 10)

    roi=spectral_analysis.roi(
        roi_dir=center,
        diffuse_sources=get_default_diffuse(diffdir=e("$FERMI/diffuse"),
                                            gfile="gll_iem_v02.fit",
                                            ifile="isotropic_iem_v02.txt"),
        catalogs = catalog,
        fit_emin = 100,
        fit_emax = 100000,
        phase_factor = 1) # phaseing already done to the ltcube

    # delete original pulsar
    roi.del_source(catalog_name)

    # add in PWN Candidate
    source=PointSource(
            name=name,
            model=PowerLaw(index=2),
            skydir=pulsar_position
        )
    source.model.set_flux(1e-8,emin=100,emax=100000)

    roi.add_source(source)

    return roi

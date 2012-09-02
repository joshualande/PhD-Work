#!/usr/bin/env python
import yaml
from os.path import expandvars as e

from uw.like.pointspec import SpectralAnalysis
from uw.like.pointspec_helpers import get_default_diffuse, PointSource, FermiCatalog
from uw.like.SpatialModels import Disk
from uw.like.Models import PowerLaw
from skymaps import SkyDir

def setup_pwn(name,pwnlist,phasing=True):
    """Name of the source
    pwnlist Yaml file
    phasing=true : apply phase cut
    phasing=false : don't do it
    
    returns pointlike ROI.
    """

    sources=yaml.load(open(pwnlist))

    catalog_name=sources[name]['catalog']
    phase=sources[name]['phase']
    ltcube=sources[name]['ltcube']
    binfile=sources[name]['binfile']
    pulsar_position=SkyDir(*sources[name]['dir'])

    ft2=sources[name]['ft2']

    if phasing==True:
        phase_factor=phase[1]-phase[0] if phase[1]>phase[0] else (1-phase[0]) + (phase[1]-0)
        ft1=sources[name]['ft1']
    else :
        phase_factor=1.0
        raise Exception("Unable to phase data")


    catalog=FermiCatalog(e("$FERMI/catalogs/gll_psc_v02.fit"),free_radius=5)
    catalog_source=[i for i in catalog.get_sources(SkyDir(),180) if i.name==catalog_name][0]

    center=catalog_source.skydir

    from uw.like.pointspec import DataSpecification
    data_specification = DataSpecification(
                         ft1files = ft1,
                         ft2files = ft2,
                         ltcube   = ltcube,
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
        phase_factor = phase_factor)

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

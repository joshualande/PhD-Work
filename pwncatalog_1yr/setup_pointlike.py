#!/usr/bin/env python
import yaml
from os.path import expandvars as e

from uw.like.pointspec import SpectralAnalysis
from uw.like.pointspec_helpers import get_default_diffuse, PointSource, FermiCatalog
from uw.like.SpatialModels import Disk
from uw.like.Models import PowerLaw
from skymaps import SkyDir

from lande_roi import LandeROI

def setup_pointlike(name,pwnlist,phasing=True):
    """Name of the source
    pwnlist Yaml file
    phasing=true : apply phase cut
    phasing=false : don't do it"""

    sources=yaml.load(open(pwnlist))

    catalog_name=sources[name]['catalog']
    phase=sources[name]['phase']
    ltcube=sources[name]['ltcube']

    if phasing==True:
        phase_factor=phase[1]-phase[0] if phase[1]>phase[0] else (1-phase[1]) + (phase[0]-0)
        ft1=sources[name]['ft1']
    else :
        phase_factor=1.0
        raise Exception("Unable to phase data")


    catalog=FermiCatalog(e("$FERMI/catalogs/gll_psc_v02.fit"))
    catalog_source=[i for i in catalog.get_sources(SkyDir(),180) if i.name==catalog_name][0]

    center=catalog_source.skydir

    from uw.like.pointspec import DataSpecification
    data_specification = DataSpecification(
                         ft1files = ft1,
                         ltcube   = ltcube,
                         binfile  = "binned_%s.fits" % name)

    spectral_analysis = SpectralAnalysis(data_specification,
                                         binsperdec = 8,
                                         emin       = 100,
                                         emax       = 100000,
                                         irf        = "P6_V3_DIFFUSE",
                                         roi_dir    = center,
                                         maxROI     = 10,
                                         minROI     = 10)

    roi=LandeROI(spectral_analysis.roi(
        roi_dir=center,
        diffuse_sources=get_default_diffuse(diffdir=e("$FERMI/diffuse"),
            gfile="gll_iem_v02.fit",
            ifile="isotropic_iem_v02.txt"),
        catalogs = catalog,
        fit_emin = 100,
        fit_emax = 100000,
        phase_factor = phase_factor)
    )

    print 'phase factor = ',roi.phase_factor

    roi.del_source(catalog_name)

    # make residual TS map

    # add in PWN Candidate
    roi.add_source(
        PointSource(
            name=name,
            model=PowerLaw(),
            skydir=catalog_source.skydir
        )
    )

    return roi

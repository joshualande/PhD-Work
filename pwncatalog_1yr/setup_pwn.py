#!/usr/bin/env python

def setup():
    import yaml
    from os.path import expandvars as e
    from argparse import ArgumentParser

    from uw.like.pointspec import SpectralAnalysis
    from uw.like.pointspec_helpers import get_default_diffuse, PointSource, FermiCatalog
    from uw.like.SpatialModels import Disk
    from uw.like.Models import PowerLaw
    from skymaps import SkyDir

    # Note that ArgumentParser correctly interprets negative numbers as positional arguments!
    """
    parser = ArgumentParser()
    parser.add_argument("-a", "--all_sources", required=True, help="List of all yaml sources")
    parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
    args=parser.parse_args()
    """

    class Empty(): pass

    args=Empty()
    args.all_sources=e("$PWNSCRIPTS/pwnlist.yaml")
    args.name="PSRJ0835-4510"

    name=args.name

    sources=yaml.load(open(args.all_sources))

    catalog_name=sources[name]['catalog']
    phase=sources[name]['phase']
    ft1=sources[name]['ft1']
    ltcube=sources[name]['ltcube']

    phase_fraction=phase[1]-phase[0] if phase[1]>phase[0] else (1-phase[1]) + (phase[0]-0)

    catalog=FermiCatalog(e("$FERMI/catalogs/gll_psc_v02.fit"))
    catalog_source=[i for i in catalog.get_sources(SkyDir(),180) if i.name==catalog_name][0]

    center=catalog_source.skydir

    from uw.like.pointspec import DataSpecification
    data_specification = DataSpecification(
                         ft1files = ft1,
                         ltcube   = ltcube,
                         binfile  = "binned.fits")

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
        fit_emax = 100000
    )

    roi.del_source(catalog_name)

    print roi

    roi.fit()

    print roi

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

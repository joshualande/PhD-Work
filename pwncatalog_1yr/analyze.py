#!/usr/bin/env python
import yaml
from os.path import expandvars as e
from argparse import ArgumentParser

from uw.like.pointspec import SpectralAnalysis
from uw.like.pointspec_helpers import get_default_diffuse, PointSource
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
args.all_sources="pwnlist.yaml"
args.name="PSRJ0835-4510"

name=args.name

sources=yaml.load(open(args.all_sources))

catalog_name=name.replace("PSRJ","PSR J")
phase=sources[name]['phase']
ft1=sources[name]['ft1']
ltcube=sources[name]['ltcube']

phase_fraction=phase[1]-phase[0]


from lande_roi import Catalog2FGL
catalog=Catalog2FGL(e("$FERMI/catalogs/24M7_uw82.fits"),
                    e("$FERMI/extended_archives/Extended_archive_v08/"))
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
                                     irf        = "P7SOURCE_V6",
                                     roi_dir    = center,
                                     maxROI     = 10,
                                     minROI     = 10)

roi=spectral_analysis.roi(
    roi_dir=center,
    diffuse_sources=get_default_diffuse(diffdir=e("$FERMI/diffuse"),
        gfile="ring_24month_P76_v1.fits",
        ifile="isotrop_21month_P76_source_v2.txt"),
    catalogs = catalog,
    fit_emin = 100,
    fit_emax = 100000
)

roi.del_source(catalog_name)

if "Vela X" in roi.dsm.names: roi.del_source("Vela X")
if "MSH 15-52" in roi.dsm.names: roi.del_source("MSH 15-52")

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

print roi

# First, calculate upper limit
    
roi.fit(use_gradient=True)

print roi

roi.localize()

if roi.TS(which=name,quick=False) > 16:

    source = roi.get_source(which=name)
    point_position = source.skydir

    roi.modify(which=name,spatial_model=Disk())

    roi.fit_extension(which=name,use_gradient=True)

    ts_ext=roi.TS_ext(which=name,use_gradient=True)

    print 'ts_ext = ',ts_ext

    if ts_ext<16:
        roi.modify(which=name,spatial_model=point_position)

    roi.fit(use_gradient=True)

    # get spectral values

    model = roi.get_model(which=name)

    print model.i_flux(100,100000)

    # make residual TS map

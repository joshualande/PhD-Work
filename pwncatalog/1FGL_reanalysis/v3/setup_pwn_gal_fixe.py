#!/usr/bin/env python
import yaml
from os.path import expandvars as e, join as j
import numbers

from tempfile import mkdtemp

from uw.like.pointspec import SpectralAnalysis
from uw.like.pointspec_helpers import get_default_diffuse, PointSource, FermiCatalog
from uw.like.SpatialModels import Disk
from uw.like.Models import PowerLaw
from skymaps import SkyDir
from uw.utilities import phasetools
from uw.like.roi_save import *
import pyfits

def get_phase_factor(phase):
    return sum([p[1]-p[0] if p[1]>p[0] else (1-p[0]) + (p[1]-0)
                      for p in phase])

def phase_ltcube(ltcube,outputfile,phase,phase_col_name='PULSE_PHASE'):
    """ Scale ltcube """

    from numpy import array
    ltcube = pyfits.open(ltcube)
    cb=ltcube['exposure'].data.field('cosbins')
    cb*=get_phase_factor(phase)

    ltcube.writeto(outputfile,clobber=True)
    ltcube.close()


def setup_pwn(name,pwndata,phase, free_radius=5, tempdir=None, **kwargs):
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
    if len(phase)==2 and isinstance(phase[0],numbers.Real) and \
       isinstance(phase[1],numbers.Real):

        # write in case phase wraps around.
        if phase[0]>phase[1]:
            phase=[[phase[0],1.0],[0.0,phase[1]]]
        else:
            phase = [phase] 

    phase_factor=get_phase_factor(phase)

    catalog=FermiCatalog(e("$FERMI/catalogs/gll_psc_v02.fit"),free_radius=free_radius)
    catalog_source=[i for i in catalog.get_sources(SkyDir(),180) if i.name==catalog_name][0]

    center=catalog_source.skydir

    if tempdir is None: tempdir=mkdtemp(prefix='/scratch/')

    binfile=j(tempdir,'binned_phased.fits')

    # apply phase cut to ft1 file
    phased_ft1 = j(tempdir,'ft1_phased.fits')
    phasetools.phase_cut(ft1,phased_ft1,phaseranges=phase)

    # create a temporary ltcube scaled by the phase factor
#    phased_ltcube=j(tempdir,'phased_ltcube.fits')
#    phase_ltcube(ltcube,phased_ltcube, phase=[0.0,1.0])
    phased_ltcube=ltcube
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
        phase_factor = phase_factor,
        **kwargs) # phaseing already done to the ltcube
    print "phase_factor=%.2f"%phase_factor

    # keep overall flux of catalog source,
    # but change the starting index to 2.
    roi.modify(which=catalog_name, name=name, index=2, 
               keep_old_flux=True)
    
    roi.toXML(filename="essai")
    print roi
    roi.print_summary()

    for names in roi.get_names():
        try :
            roi.modify(names,Norm=roi.get_model(names)[0]*roi.phase_factor)
        except :
            try :
                roi.modify(names,Int_flux=roi.get_model(names)[0]*roi.phase_factor)
            except :
                print names
    table=roi.get_names()

    print roi.modify(which=table[len(table)-2],model=PowerLaw(p=[1.0*phase_factor,0.1]),free=[True,False])
    print roi.modify(which=table[len(table)-1],model=PowerLaw(p=[1.0*phase_factor,0.1]),free=[True,False])
#    print roi.modify(which='eg_v02',free=[False])
    print roi

    return roi

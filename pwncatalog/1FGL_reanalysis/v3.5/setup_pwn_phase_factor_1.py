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


def setup_pwn(name,pwndata,phase, free_radius=5, tempdir=None, emin=1.0e2, emax=1.0e5,maxroi=10,model=None,**kwargs):
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
    print "phase"
    print phase
    print "phase_factor=%.2f"%phase_factor

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
#    phase_ltcube(ltcube,phased_ltcube, phase=phase)
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
                                         maxROI     = maxroi,
                                         minROI     = maxroi)

    if model == None :
        roi=spectral_analysis.roi(
            roi_dir=center,
            diffuse_sources=get_default_diffuse(diffdir=e("$FERMI/diffuse"),
                                                gfile="gll_iem_v02.fit",
                                                ifile="isotropic_iem_v02.txt"),
            catalogs = catalog,
            phase_factor = 1.0,
            fit_emin = [emin,emin],
            fit_emax = [emax,emax],
            **kwargs)
    else :
        roi=spectral_analysis.roi(
            roi_dir=center,
            xmlfile = model,
            phase_factor =1.0,
            fit_emin = [emin,emin],
            fit_emax = [emax,emax],
            **kwargs)

    print "---------------------Energy range--------------------"
    
    print "emin="+str(roi.bands[0].emin)+"\n"
    print "emax="+str(roi.bands[len(roi.bands)-1].emax)+"\n"
        

    # keep overall flux of catalog source,
    # but change the starting index to 2.
    roi.modify(which=catalog_name, name=name, index=2, 
               keep_old_flux=True)

    return roi

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
from uw.like.SpatialModels import Disk
from uw.like.Models import PowerLaw
from uw.utilities import phasetools
from phase_range import PhaseRange

def phase_ltcube(ltcube,outputfile,phase,phase_col_name='PULSE_PHASE'):
    """ Scale ltcube """

    from numpy import array
    ltcube = pyfits.open(ltcube)
    cb=ltcube['exposure'].data.field('cosbins')
    cb*=phase.phase_fraction

    ltcube.writeto(outputfile,clobber=True)
    ltcube.close()


def setup_pwn(name,pwndata,phase, free_radius=5, tempdir=None, emin=1.0e2, emax=1.0e5,maxroi=10,model=None,**kwargs):
    """Name of the source
    pwndata Yaml file
    
    returns pointlike ROI.
    """

    phase = PhaseRange(phase)

    sources=yaml.load(open(pwndata))

    catalog_name=sources[name]['catalog']
    ltcube=sources[name]['ltcube']
    pulsar_position=SkyDir(*sources[name]['dir'])
    ft2=sources[name]['ft2']
    ft1=sources[name]['ft1']


    catalog=FermiCatalog(e("$FERMI/catalogs/gll_psc_v02.fit"))
    catalog=Catalog2FGL('$FERMI/catalogs/gll_psc_v05.fit', 
                        latextdir='$FERMI/extended_archives/',
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
            phase_factor = get_phase_factor(phase),
            fit_emin = [emin,emin],
            fit_emax = [emax,emax],
            **kwargs)
    else :
        roi=spectral_analysis.roi(
            roi_dir=center,
            xmlfile = model,
            phase_factor = get_phase_factor(phase),
            fit_emin = [emin,emin],
            fit_emax = [emax,emax],
            **kwargs)

    print "---------------------Energy range--------------------"
    
    print "emin="+str(roi.bands[0].emin)+"\n"
    print "emax="+str(roi.bands[len(roi.bands)-1].emax)+"\n"
        

    # keep overall flux of catalog source,
    # but change the starting index to 2.
    roi.modify(which=catalog_name, name=name, index=2, keep_old_flux=True)

    return roi

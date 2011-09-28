#!/usr/bin/env python
import toolbag
import yaml
from tempfile import mkdtemp
from os.path import join
import shutil
import argparse

import numpy as N

from skymaps import IsotropicPowerLaw
from uw.like.roi_monte_carlo import MonteCarlo,NoSimulatedPhotons
from skymaps import SkyDir
from uw.like.pointspec import DataSpecification,SpectralAnalysis
from uw.like.pointspec_helpers import PointSource
from uw.like.roi_diffuse import DiffuseSource
from uw.like.pixeldata import PixelData
from uw.like.Models import PowerLaw
from uw.like.SpatialModels import Disk
from uw.utilities.fitstools import merge_bpd

from argparse import ArgumentParser

# Note that ArgumentParser correctly interprets negative numbers as positional arguments!
parser = ArgumentParser()
parser.add_argument("i",type=int)
args=parser.parse_args()
i=args.i
istr='%07d' % i

N.random.seed(i)

irf='P7SOURCE_V6'
emin=1e3
emax=1e5
results='results_%d.yaml' % i

# use Sreekumar-like defaults
diffuse_sources = [DiffuseSource(
        IsotropicPowerLaw(10*1.5e-5,2.1),
        PowerLaw(p=[1,1],index_offset=1),
        'Isotropic Diffuse x 10',
        )]


tempdir=mkdtemp(prefix='/scratch/')

# first simulated the diffuse emission

ft2=join(tempdir,'ft2.fits')
ltcube=join(tempdir,'ltcube.fits')

print 'First, simulating the diffuse emission'
diffuse_ft1=join(tempdir,'diffuse_ft1.fits')
diffuse_binfile=join(tempdir,'diffuse_binfile.fits')

skydir_mc=SkyDir(0,0)

mc=MonteCarlo(
    diffuse_sources=diffuse_sources,
    seed=i,
    irf=irf,
    ft1=diffuse_ft1,
    ft2=ft2,
    tstart=0,
    tstop=31556926,
    ltfrac=0.8,
    roi_dir=skydir_mc,
    maxROI=15,
    emin=emin,
    emax=emax)
mc.simulate()

PixelData(ft1files=diffuse_ft1,binfile=diffuse_binfile,binsperdec=4,event_class=0)

results_dict=[]

index_mc=2

for flux_mc in [ 1e-9, 3e-9, 1e-8, 3e-8, 1e-7, 3e-7, 1e-6, 3e-6 ]:

    source_str="%g_%g_%s" % (flux_mc,index_mc,istr)

    print 'Flux_mc=%g, Index_mc=%g' % (flux_mc,index_mc)

    name_mc='source_%s' % istr

    model_mc=PowerLaw(p=[1,index_mc])
    model_mc.set_flux(flux_mc,100,N.inf)

    source_mc=PointSource(name=name_mc,skydir=skydir_mc,model=model_mc)

    source_ft1=join(tempdir,'source_%s_ft1.fits' % source_str)
    source_binfile=join(tempdir,'source_%s_binned.fits' % source_str)

    all_binfile=join(tempdir,'all_%s_binned.fits' % source_str)

    mc=MonteCarlo(
        point_sources=source_mc,
        seed=i,
        irf=irf,
        ft1=source_ft1,
        ft2=ft2,
        roi_dir=skydir_mc,
        maxROI=15,
        emin=emin,
        emax=emax)
    try:
        mc.simulate()

        PixelData(ft1files=source_ft1,binfile=source_binfile,binsperdec=4,event_class=0)

        merge_bpd([diffuse_binfile,source_binfile],outfile=all_binfile)
    except NoSimulatedPhotons, ex:
        print 'No simulated photons for source %s'  % source_str
        all_binfile=diffuse_binfile

    ds=DataSpecification(
        ft2files = ft2,
        ltcube   = ltcube,
        binfile  = all_binfile)

    results_dict.append(dict(
        i=i,
        istr=istr,
        flux_mc=flux_mc,
        index_mc=index_mc,
    ))


    for fit_irf in ["P7SOURCE_V6", "P7SOURCE_V4"]:

        print 'Using fit_irf %s' % fit_irf

        sa=SpectralAnalysis(ds,
            irf         = fit_irf,
            roi_dir     = skydir_mc,
            maxROI      = 10,
            minROI      = 10,
            event_class = 0, # not this is necessary for MC data
            emin        = emin,
            emax        = emax,
        )

        source_guess=PointSource(name=name_mc,skydir=skydir_mc,model=model_mc.copy())

        roi=sa.roi(
            roi_dir=skydir_mc,
            diffuse_sources=[j.copy() for j in diffuse_sources],
            point_sources=[source_guess]
        )

        print 'bins = ',roi.bin_edges

        print 'Fitting unmodified ROI'

        def fit():
            try:
                roi.fit(use_gradient=True)
            except Exception, err:
                print '\n\n\n\nERROR FITTING: %s\n\n\n' % (str(err))

        fit()
        try:
            roi.localize(which=name_mc,update=True,maxdist=5)
        except Exception, err:
            print '\n\n\n\nERROR LOCALIZING: %s\n\n\n' % (str(err))
        fit()

        model=roi.get_model(which=name_mc)
        flux,flux_err=model.i_flux(emin=100,emax=100000,error=True)
        index = model['index']
        index_err=model.error('index')

        roi.print_summary()

        print roi

        print 'Modifying to extended source'

        roi.modify(which=name_mc,spatial_model=Disk(sigma=.1))

        fit()

        try:
            roi.fit_extension(which=name_mc,bandfits=False,estimate_errors=False)
            ts_ext=roi.TS_ext(which=name_mc,bandfits=False)
        except Exception, err:
            print '\n\n\n\nERROR FITTING EXTENSION: %s\n\n\n' % (str(err))
            ts_ext=-99

        fit()

        ts=roi.TS(which=name_mc,bandfits=False)

        source=roi.get_source(which=name_mc)
        sigma=source.spatial_model['sigma']


        results_dict[-1]['ts_%s' % fit_irf] = ts
        results_dict[-1]['ts_ext_%s' % fit_irf] = ts_ext
        results_dict[-1]['sigma_%s' % fit_irf] = sigma

    results_dict = toolbag.tolist(results_dict)

    temp=open(results,'w')
    temp.write(yaml.dump(results_dict))
    temp.close()

shutil.rmtree(tempdir)

#!/usr/bin/env python

import yaml
import imp
import os
import argparse

import numpy as N
from uw.like.pointspec_helpers import PointSource,FermiCatalog
from uw.like.roi_catalogs import SourceCatalog
from skymaps import SkyDir,SkyIntegrator,SkyImage
from uw.like.pointspec import SpectralAnalysis,DataSpecification
from uw.like.Models import *
from uw.like.roi_diffuse import ROIDiffuseModel_OTF
from uw.like.roi_extended import ExtendedSource,ROIExtendedModel
import uw.like.SpatialModels 
from uw.like.SpatialModels import DefaultSpatialModelValues

import lande_roi

def add_ts_ext(outfile):
    
    # Do pointlike part
    for spatial in outfile.keys():
        # Loop over all spatial hypothesis with pseudo counterpart to calculate TS_ext.
        if outfile.has_key('Pseudo'+spatial):
            outfile[spatial]['Pointlike']['TS_ext']={}

            for type in outfile[spatial]['Pointlike']['logLikelihood'].keys():

                h1=outfile[spatial]['Pointlike']['logLikelihood'][type]
                h0=outfile['Pseudo'+spatial]['Pointlike']['logLikelihood'][type]

                outfile[spatial]['Pointlike']['TS_ext'][type]=2*(h1-h0)

    # Do gtlike part, compare to point hypothesis
    for spatial in outfile.keys():
        if spatial in DefaultSpatialModelValues.models.keys() and \
                outfile.has_key('Point'):

            if outfile[spatial].has_key('Gtlike') and \
                    outfile['Point'].has_key('Gtlike'):

                h1=outfile[spatial]['Gtlike']['logLikelihood']['spectral']
                h0=outfile['Point']['Gtlike']['logLikelihood']['spectral']

                outfile[spatial]['Gtlike']['TS_ext']={'spectral':2*(h1-h0)}

    # get ts_inc
    if 'TwoPoints' in outfile.keys() and 'Point' in outfile.keys():

        for method in ['Gtlike','Pointlike']:

            if outfile['TwoPoints'].has_key(method) and outfile['Point'].has_key(method):
                outfile['TwoPoints'][method]['TS_inc']={
                    'spectral':float(2*(outfile['TwoPoints'][method]['logLikelihood']['spectral']-
                                     outfile['Point'][method]['logLikelihood']['spectral']))
                }

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="""like runSourcelike, but like, better.""")

    parser.add_argument("-O", "--datafiles", help="Datafiles to find data in",required=True)
    parser.add_argument("-n", "--name", help="Name of the source to be analysed",required=True)
    parser.add_argument("-H","--hypothesis",action='append', help="""List of hypothesis to use.""",required=True)
    parser.add_argument("--bandfits", action='store_true', default=False)

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all","--All",default=False, action="store_true", help="Run all the followup stuff")
    group.add_argument("--pointlike","--Pointlike",default=False, action="store_true", help="Run just the pointlike followup stuff")
    group.add_argument("--gtlike", "--Gtlike", default=False, action='store_true')


    parser.add_argument("--irf", required=True)
    parser.add_argument("--psf-irf", default=None)
    parser.add_argument("--roi", type=float, default=10, help="Default= %default.")
    parser.add_argument("--localize", action='store_true', default=False, 
            help="localization the sources")
    parser.add_argument("-e", "--emin", type=float, required=True,
            help="""Minimum energy bin to use. Default=%default""")
    parser.add_argument("-E", "--emax", type=float, required=True,
            help="""Maximum energy in fit. This is also an inclusive option
    so the largest bin containing the emax value will be the biggest bin used. Default=%default""")
    parser.add_argument("--convert-plaw", default=False, action='store_true')
    parser.add_argument("--bg-exclude", nargs='*', action='append')
    parser.add_argument("--prune-radius", type=float, help='prunes catalog poing sources within this radius of the source.')
    parser.add_argument("--num-points", type=int, help='For analytic convolution')
    parser.add_argument("--modify-roi")
    parser.add_argument("--error", default="HESSE")
    args = parser.parse_args()

    if args.num_points is not None:
        from uw.utilities.convolution import AnalyticConvolution
        AnalyticConvolution.set_points(args.num_points)


    name=args.name

    savename = name.replace(' ','_')

    datafiles=imp.load_source('datafiles',args.datafiles)

    start_spectral = None

    manager=FermiCatalog(datafiles.catalog) if not isinstance(datafiles.catalog,SourceCatalog) else datafiles.catalog
    source = manager.get_source(name) # only works with Catalog2FGL (oops)
    start_spectral = source.model
    skydir = source.skydir

    outfile={'start_cel':[skydir.ra(),skydir.dec()],
             'start_gal':[skydir.l(),skydir.b()],
             'name':name}

    ds = DataSpecification(
        binfile  = datafiles.binfile,
        ltcube   = datafiles.ltcube,
        ft1files = datafiles.ft1files,
        ft2files = datafiles.ft2file)

    sa = SpectralAnalysis(ds,
        binsperdec = datafiles.binsperdecade,
        emin       = datafiles.emin,
        emax       = datafiles.emax,
        roi_dir    = skydir,
        irf        = args.irf,
        psf_irf    = args.psf_irf,
        exp_radius = args.roi+5,
        maxROI     = args.roi,
        minROI     = args.roi,
        event_class = 0) # p7 has funny event classes

    for hypothesis in args.hypothesis:
        print
        print '#'*60
        print


        print 'Beginning hypothesis %s' % hypothesis
        print

        diffuse_sources = [lande_roi.LandeROI.get_background(i) if isinstance(i,str) else i.copy() for i in datafiles.background]

        point_sources = []

        start_dir = skydir

        if hypothesis == 'Point':
            source=PointSource(skydir=start_dir, name=name, model=start_spectral.copy())
            point_sources.append(source)
        elif hypothesis == 'TwoPoints':
            source1 = PointSource(name='%s (first)' % name,
                             model=start_spectral.copy(),
                             skydir=start_dir)
            source2 = PointSource(name='%s (second)' % name,
                             model=start_spectral.copy(),
                             skydir=start_dir)

            point_sources += [source1, source2]

        elif hypothesis != 'Background':
            # get out the spatial model with the name 'hypothesis'
            obj = eval("uw.like.SpatialModels.%s" % hypothesis)
            spatial_model = obj(center=start_dir, coordsystem=SkyDir.GALACTIC)
            spatial_model.limits[0:2] = N.asarray([[-1,1],[-1,1]])
                                                          
            source=ExtendedSource(name=name, 
                                  model=start_spectral.copy(),
                                  spatial_model=spatial_model)
            diffuse_sources.append(source)

        roi = lande_roi.VerboseROI(sa.roi(point_sources = point_sources, diffuse_sources = diffuse_sources,
                     fit_emin=args.emin, fit_emax=args.emax, catalogs=datafiles.catalog))

        if args.modify_roi is not None:
            modify_roi=imp.load_source('modify_roi',args.modify_roi)
            modify_roi.modify_roi(name,roi)

        roi.print_summary()
        if args.convert_plaw:
            if hypothesis == 'TwoPoints':
                roi.modify(which='%s (first)' % name,model=PowerLaw(e0=N.sqrt(args.emin*args.emax)))
                roi.modify(which='%s (second)' % name,model=PowerLaw(e0=N.sqrt(args.emin*args.emax)))
            else:
                roi.modify(which=name,model=PowerLaw(e0=N.sqrt(args.emin*args.emax)))

        if args.prune_radius:
            # necessary to do here instead of in the FermiCatalog for the case Background
            # so that we prune even when there is no 'source' to fit
            for source in roi.psm.point_sources:
                if name not in source.name and \
                        N.degrees(source.skydir.difference(start_dir)) < args.prune_radius:
                    print 'deleting source %s because it is too close to our source' % source.name
                    roi.del_source(source)

        roi.prune_empty_diffuse_models() # this is a hack for the ring models Markus gave me.

        if hypothesis in ['Background', 'TwoPoints']:
            if name in roi.get_names():
                roi.del_source(name)

        roi.print_summary()
        roi.fit()
        roi.print_summary()

        if args.localize and hypothesis != 'Background':
            if hypothesis == 'Point':
                roi.localize(which=name, bandfits=args.bandfits)
            elif hypothesis == 'TwoPoints':
                roi.dual_localize(source1, source2)
            else:

                roi.fit_extension(which=name,
                                      bandfits=args.bandfits, error=args.error)

                # localize to get better localization error
                roi.localize(which=name, bandfits=args.bandfits, update=False)

        roi.fit()
        roi.print_summary()
        print roi

        roi.save('roi_%s_%s.dat' % (hypothesis,savename))

        outfile[hypothesis]={}
        outfile[hypothesis]['Pointlike']=roi.get_info_dict(name)

    outfile['bins']=roi.bin_edges.tolist()                                                                                       

    add_ts_ext(outfile)

    file=open("results_%s.yaml" % savename,'w')
    file.write(yaml.dump(outfile))
    file.close()

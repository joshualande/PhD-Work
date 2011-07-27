#!/usr/bin/env python
""" Performs a followup analysis in the current directory. """
import matplotlib as mpl
mpl.rcParams['backend'] = 'Agg' 

import yaml
import imp
import glob
import os
from argparse import ArgumentParser

from GtApp import GtApp
from BinnedAnalysis import BinnedObs,BinnedAnalysis
from pyLikelihood import ParameterVector
import lande_roi

from runPointlike import add_ts_ext
from skymaps import SkyDir

parser = ArgumentParser()
parser.add_argument("-O", "--datafiles", help="Datafiles to find data in",required=True)
parser.add_argument("-n", "--name", help="Name of the source to be analysed",required=True)
parser.add_argument("-H","--hypothesis", help="""List of hypothesis to use.""",required=True)

group = parser.add_mutually_exclusive_group()
group.add_argument("--all","--All",default=False, action="store_true", help="Run all the followup stuff")
group.add_argument("--pointlike","--Pointlike",default=False, action="store_true", help="Run just the pointlike followup stuff")
group.add_argument("--gtlike", "--Gtlike", default=False, action='store_true')

parser.add_argument("--bandfits", action='store_true', default=False)
parser.add_argument("--profile", action='store_true', default=False)
parser.add_argument("-T", "--tsmap", action='store_true', default=False, 
        help="Create ts maps")
parser.add_argument("--front-only-maps", default=False, action='store_true')
parser.add_argument("--sed", action='store_true', default=True)
parser.add_argument("-f","--fov", type=float, default=10., 
        help="Field-Of-View. This is only used in generating images and TS maps!")
parser.add_argument("-p","--pixelsize", type=float, default=0.125, 
        help="Size of pixels to use when creating images.")
parser.add_argument("--test-two-sources", default=False, action='store_true')
parser.add_argument("--maps", default=False, action='store_true')
parser.add_argument("--binsz", type=float, help='sent to gtlike_followup')
parser.add_argument("--bigger-roi", action='store_true', default=False, help='sent to gtlike_followup')
args,remaining_args = parser.parse_known_args()

name = args.name
savename = name.replace(' ','_')

results='results_%s.yaml' % savename
outfile=yaml.load(open(results))

hypothesis = args.hypothesis

roi_name='roi_%s_%s.dat' % (hypothesis,savename)

skydir=SkyDir(*outfile['start_cel'])

print 'Working on',roi_name

base=os.path.splitext(roi_name)[0]
base=base.split('_')
base.pop(0) # remove the "roi_" part

spatial=base.pop(0)

# incase datafiles defines any important environment variables.
datafiles=imp.load_source('datafiles',args.datafiles)

roi=lande_roi.VerboseROI.load(roi_name)

roi.remove_nan_background_sources(name)

t=lande_roi.StopWatch()
print 'Beginning Stopwatch'

if datafiles.__dict__.has_key('cache_ft1_dir'): 
    cache_dir=os.path.join(datafiles.cache_ft1_dir,savename)
    if not os.path.exists(cache_dir): 
        os.mkdir(cache_dir)
    cachefile=os.path.join(cache_dir,savename+'_emin_%g_emax_%g.fits' % (min(roi.fit_emin),max(roi.fit_emax)))
    roi.cache_ft1(cachefile)
print t

roi.toRegion('results_%s_%s.reg' % (spatial,savename))

# if two point sources, use first hypothesis
which=name if spatial != 'TwoPoints' else '%s (first)' % name

if (args.maps or args.all or args.pointlike) and \
        'Pseudo' not in spatial:
    roi.plot_counts_map(filename='map_%s_%s.png' % (spatial,savename),
                    countsfile='counts_%s_%s.fits' % (spatial,savename),
                    modelfile='model_%s_%s.fits' % (spatial,savename))

    roi.plot_significance(filename='significance_%s_%s.png' % (spatial,savename))

    if spatial not in ['Background']:

        # make slice & radial integral front events only.
        roi.plot_slice(which=which,filename='slice_%s_%s_gal.png' % (spatial,savename),conv_type=0,galactic=True)
        print t
        roi.plot_slice(which=which,filename='slice_%s_%s_cel.png' % (spatial,savename),conv_type=0,galactic=False)
        print t
        roi.plot_radial_integral(which=which,filename='radial_%s_%s.png' % (spatial,savename),conv_type=0)
        print t
        roi.plot_source(which=which,filename='source_%s_%s.png' % (spatial,savename))
        print t
        roi.plot_sources(which=which,filename='sources_%s_%s.png' % (spatial,savename))
        print t
        roi.plot_model(which=which,filename='model_%s_%s.png' % (spatial,savename))
        print t

if args.sed or args.all or args.pointlike:
    if spatial not in ['Background' ]:
        roi.plot_sed(which=which,filename='sed_%s_%s.png' % (spatial,savename), 
                use_ergs=True, galmap=False)
        print t

if (args.tsmap or args.all or args.pointlike) and 'Pseudo' not in spatial:

    roi.plot_tsmap(filename='res_tsmap_%s_%s.png' % (spatial,savename),
                   fitsfile='res_tsmap_%s_%s.fits' % (spatial,savename),
                   pixelsize=args.pixelsize,
                   size=args.fov,
                   galactic=True,
                   title='Residual TS Map %s' % spatial.replace('_',' '))
    print t

if (args.gtlike or args.all) and 'Pseudo' not in spatial and spatial != 'Background':


    srcmdl_file='Gtlike_srcmdl_%s_%s.xml' % (spatial,savename)

    kwargs={}
    if args.bigger_roi is not None: kwargs['bigger_roi']=args.bigger_roi
    if args.binsz is not None: kwargs['binsz']=args.binsz

    outfile[spatial]['Gtlike']=roi.gtlike_followup(name,
            output_srcmdl_file=srcmdl_file,**kwargs)
    print t

if (args.profile or args.all or args.pointlike) and \
        spatial not in ['Background','Point','TwoPoints'] and \
        'Pseudo' not in spatial:

    roi.plot_profile(which=name,
            filename='profile_%s_%s.png' % (spatial,savename),
            datafile='profile_%s_%s.yaml' % (spatial,savename),
            quick=False,use_gradient=True
    )
    print t


add_ts_ext(outfile)

if args.gtlike:
    file=open("results_followup_%s_Gtlike_%s.yaml" % (hypothesis,savename),'w')
elif args.pointlike:
    file=open("results_followup_%s_Pointlike_%s.yaml" % (hypothesis,savename),'w')
elif args.all:
    file=open("results_followup_%s_%s.yaml" % (hypothesis,savename),'w')
else:
    file=open("results_followup_%s_Custom_%s.yaml" % (hypothesis,savename),'w')
file.write(yaml.dump(outfile))
file.close()

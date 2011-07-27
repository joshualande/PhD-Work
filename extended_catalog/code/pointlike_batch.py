#!/usr/bin/env python

from uw.like.roi_catalogs import FermiCatalog,SourceCatalog

from skymaps import SkyDir
import sys
import imp
import os
import csv
import re
import math
import pyfits
import glob
from textwrap import dedent
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-o", "--outdir", help="Name of output directory for jobs",required=True)
parser.add_argument("-s", "--sources", default=None, nargs='+', help='analyze these sources, instead of all catalog soruces)')
parser.add_argument("-O", "--datafiles", help="Datafiles to find data in",required=True)
parser.add_argument("-q", "--queue", default='-q kipac-ibq', 
        help="Name of the queue where job is submitted. Default=%default")
parser.add_argument("-H","--hypothesis",action='append',
                  help="""List of hypothesis to use.""",required=True)
parser.add_argument("-C", "--cmd", default="",
        help="The string should include all extra flags that should be used when running runPointlike")
parser.add_argument("-F", "--followup-cmd", default="")
parser.add_argument("--followup-all", default=False, action="store_true")
parser.add_argument("--always-followup")
parser.add_argument("--latcut", type=float, help='latitude cut')
parser.add_argument("--followup-ts", type=float)
args = parser.parse_args()

datafiles=imp.load_source('datafiles',args.datafiles)
catalog=datafiles.catalog

if len(sys.argv)<1:
    parser.print_help()
    sys.exit(1)

if args.outdir is None: parser.error("--outdir must be set.")

if '-H' in args.cmd: raise Exception("-H must not be specified in --cmd")

if not os.path.exists(args.outdir): os.mkdir(args.outdir)

submit_all=open("%s/submit_all.py" % args.outdir,'w')
submit_all.write("""
#!/usr/bin/env python
import glob
from os.path import exists,isdir
from os import system

import argparse
parser=argparse.ArgumentParser()
parser.add_argument("-n",default=False,action="store_true",help="Don't do anything")
parser.add_argument("-q","--queue",default="%s")
args = parser.parse_args()

for savename in glob.glob("*"):
    if isdir(savename):
        results="%%s/v1/results_%%s.yaml" %% (savename,savename)
        log="%%s/v1/log_%%s.txt" %% (savename,savename)
        if (not exists(results) and (not exists(log) or "Results reported at" in open(log).read())) or \
                (exists(results) and not exists(log)):
            string="cd %%s/v1; bsub -q %%s -oo log_%%s.txt sh $PWD/run_%%s.sh; cd .." %% (savename,args.queue,savename,savename)
            if args.n:
                print string
            else:
                system(string)
""" % args.queue)
submit_all.close()

followup=open("%s/followup.py" % args.outdir,'w')
followup.write("""
#!/usr/bin/env python
import glob
import yaml
from os.path import exists,isdir,getsize
from os import system
import argparse
parser=argparse.ArgumentParser()
parser.add_argument("-H","--hypothesis",action='append',choices=["Background","Point","PseudoDisk","Disk"])
parser.add_argument("-n",default=False,action="store_true",help="Don't do anything")
parser.add_argument("-t","--type",action='append',choices=["Gtlike","Pointlike"])
parser.add_argument("-q","--queue",default="%s")
parser.add_argument("--followup-all", default=False, action="store_true")
args = parser.parse_args()
if args.hypothesis is None: args.hypothesis=%s
if args.type==None: args.type=['Gtlike','Pointlike']

""" % (args.queue,str(args.hypothesis)))

if args.always_followup is not None:
    followup.write("""
always_followup=[i.strip() for i in open("%s").readlines()]
""" % (str(args.always_followup)))
else:
    followup.write("""
always_followup=[]
""")


followup.write("""
for savename in glob.glob("*"):
    if isdir(savename):
        results="%s/v1/results_%s.yaml" % (savename,savename)
        log="%s/v1/log_%s.txt" % (savename,savename)
        if exists(results) and exists(log) and "Results reported at" in open(log).read():

            data=yaml.load(open(results))
            name=data['name']

            ts_point=data['PseudoDisk']['Pointlike']['TS']['slow']
            ts_pseudodisk=data['PseudoDisk']['Pointlike']['TS']['slow']
            ts_disk=data['Disk']['Pointlike']['TS']['slow']

            ts_ext_spectral=data['Disk']['Pointlike']['TS_ext']['spectral']
            ts_ext_bandfits=data['Disk']['Pointlike']['TS_ext']['bandfits']
            sigma=data['Disk']['Pointlike']['Sigma'][0]""")

if not args.followup_all:
    followup.write("""
            if (ts_ext_spectral>%s and ts_point>9 and ts_pseudodisk>9 and ts_disk>9 and sigma<2.9) \\
                    or name in always_followup or args.followup_all:""" % (args.followup_ts))
else:
    followup.write("""
            if True:""")

followup.write("""

                for type in args.type:

                    for hyp in args.hypothesis:
                        followup_results="%s/v1/results_followup_%s_%s_%s.yaml" % (savename,hyp,type,savename)
                        followup_log="%s/v1/log_followup_%s_%s_%s.txt" % (savename,hyp,type,savename)

                        if (not exists(followup_results) or getsize(followup_results)==0) \\
                                and (not exists(followup_log) or \\
                                "Results reported at" in open(followup_log).read()):
                            string="cd %s/v1; bsub -q %s -oo log_followup_%s_%s_%s.txt sh $PWD/followup_%s_%s_%s.sh; cd ../.." % (savename,args.queue,hyp,type,savename,hyp,type,savename)
                            if args.n:
                                print string
                            else:
                                system(string)
 """)
followup.close()

merge=open("%s/merge.py" % args.outdir,'w')
merge.write("""
#!/usr/bin/env python
import glob
import yaml
from os.path import exists,isdir,getsize
from lande_roi import merge_dict
from runPointlike import add_ts_ext
for savename in glob.glob("*"):
    if isdir(savename):
        results="%%s/v1/results_%%s.yaml" %% (savename,savename)
        if not exists(results): continue
        all_results=[yaml.load(open(results))]

        for type in ['Gtlike','Pointlike']:
            for hyp in %s:
                results_followup = "%%s/v1/results_followup_%%s_%%s_%%s.yaml" %% (savename,hyp,type,savename)
                if exists(results_followup) and getsize(results_followup)>0:
                    all_results.append(yaml.load(open(results_followup)))

        print 'merging %%s' %% savename
        merged_results = reduce(merge_dict,all_results)
        add_ts_ext(merged_results)
        save_results=open("%%s/v1/results_followup_%%s.yaml" %% (savename,savename),'w')
        yaml.dump(merged_results,save_results)

""" % str(args.hypothesis))

manager=FermiCatalog(catalog) if not isinstance(catalog,SourceCatalog) else catalog
sources=manager.get_sources(SkyDir(),180)

if args.sources is not None:
    all_names=[i.name for i in sources]
    select_sources=[]
    for name in args.sources:
        if name not in all_names:
            raise Exception('Name "%s" not in list of all names' % name) 
        index=all_names.index(name)
        source=sources[index]
        select_sources.append(source)
    sources=select_sources

for source in sources:
    name=source.name

    if args.latcut and abs(source.skydir.b())< args.latcut:
        continue

    savename=name.replace(' ','_')

    outdir = "%s/%s/v1" % (args.outdir,savename)
    if not os.path.exists(outdir): os.makedirs(outdir)

    file=open('%s/run_%s.sh' % (outdir,savename),'w')
    file.write(dedent(r"""
        ulimit -c 0
        runPointlike.py \
            -n "%s" \
            -O %s \
            -H %s \
            %s""" % (name,args.datafiles,' -H '.join(args.hypothesis),args.cmd)))

    file.close()

    for type in ['Gtlike','Pointlike']:

        for hyp in args.hypothesis:
            file=open('%s/followup_%s_%s_%s.sh' % (outdir,hyp,type,savename),'w')
            file.write(dedent(r"""
                ulimit -c 0
                followup.py -n "%s" --%s \
                    -O %s \
                    -H %s \
                    %s %s""" % (name,type,args.datafiles,hyp,args.cmd,args.followup_cmd)))

print "Done creating jobs sources"

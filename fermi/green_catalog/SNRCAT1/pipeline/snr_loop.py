"""
A script to loop over the snr when
doing analysis. Example:

python snr_loop.py -c lande_pipeline.py \
        --superfile $superfile/snrdata.yaml \
        -o $FERMILANDE/green_catalog/test/v1
"""
import yaml
from os.path import expandvars as e
from os.path import join
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-c", "--command", required=True)
parser.add_argument("--superfile", required=True)
parser.add_argument("-o", "--outdir", required=True)
args,remaining_args = parser.parse_known_args()

  
outdir=args.outdir

sources=yaml.load(open(args.superfile))

if os.path.exists(outdir):
    raise Exception("outdir %s already exists" % outdir)
os.makedirs(outdir)

for name in sources.keys():
    if name == 'notes': continue

    print name

    folder=join(outdir,name)
    os.makedirs(folder)

    file=join(folder,'run_%s.sh' % name)

    temp=open(file,'w')
    temp.write("""\
python %s/%s \\
--name %s \\
--superfile %s %s""" % (os.getcwd(),args.command,name,
                     args.superfile,' '.join(remaining_args)))


submit_all=join(outdir,'submit_all.py')
temp=open(submit_all,'w')
temp.write("""
#!/usr/bin/env python
import glob
from os.path import exists,isdir,expandvars
from os import system
import argparse
import subprocess

parser=argparse.ArgumentParser()
parser.add_argument("-n",default=False,action="store_true",help="Don't do anything")
parser.add_argument("-q","--queue",default='xxl',help="Don't do anything")
args = parser.parse_args()

p=subprocess.Popen(['bjobs', '-w'],stdout=subprocess.PIPE)
queue_jobs,err=p.communicate()

for name in glob.iglob("*"):
    if isdir(name):
        results="%s/results*%s.yaml" % (name,name)
        log="%s/log_%s.txt" % (name,name)
        run='$PWD/%s/run_%s.sh' % (name,name)

        results_exists = len(glob.glob(results)) > 0
        is_in_queue = expandvars(run) in queue_jobs

        if not is_in_queue and not results_exists:
            string="cd %s; bsub -q %s -oo log_%s.txt sh $PWD/run_%s.sh; cd .." % (name,args.queue,name,name)
            if args.n:
                print string
            else:
                system(string)
""")



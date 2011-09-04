import yaml
from os.path import expandvars as e
from os.path import join
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-c", "--command", required=True)
parser.add_argument("-o", "--outdir", required=True)
args=parser.parse_args()
  
outdir=args.outdir

sources=yaml.load(open('pwndata.yaml'))

if os.path.exists(outdir):
    raise Exception("outdir %s already exists" % outdir)
os.makedirs(outdir)

for name in sources.keys():
    print name

    folder=join(outdir,name)
    os.makedirs(folder)

    file=join(folder,'run_%s.sh' % name)

    temp=open(file,'w')
    temp.write("""\
python %s/%s \\
-n %s \\
--pwndata %s/pwndata.yaml \\
--pwnphase %s/pwnphase.yaml """ % (os.getcwd(),args.command,name,os.getcwd(),os.getcwd()))


submit_all=join(outdir,'submit_all.py')
temp=open(submit_all,'w')
temp.write("""
#!/usr/bin/env python
import glob
from os.path import exists,isdir
from os import system
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("-n",default=False,action="store_true",help="Don't do anything")
args = parser.parse_args()

for name in glob.iglob("*"):
    if isdir(name):
        results="%s/results_%s.yaml" % (name,name)
        log="%s/log_%s.txt" % (name,name)
        if not exists(results) and (not exists(log) or "Results reported at" in open(log).read()):
            string="cd %s; bsub -q kipac-ibq -oo log_%s.txt sh $PWD/run_%s.sh; cd .." % (name,name,name)
            if args.n:
                print string
            else:
                system(string)
""")



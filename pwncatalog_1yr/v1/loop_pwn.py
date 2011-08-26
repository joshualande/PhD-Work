import yaml
from os.path import expandvars as e
from os.path import join
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-c", "--command", required=True, choices=["analyze_pointlike.py","upper_limit_pointlike.py"])
parser.add_argument("-o", "--outdir", required=True)
parser.add_argument("-l", "--pwnlist", required=True, help="List of all yaml sources")
args=parser.parse_args()
  
command=args.command
outdir=args.outdir

sources=yaml.load(open(args.pwnlist))

os.makedirs(outdir)

for name in sources.keys():
    print name

    folder=join(outdir,name)
    os.makedirs(folder)

    folder=join(outdir,name,'v1')
    os.makedirs(folder)

    file=join(folder,'run_%s.sh' % name)

    temp=open(file,'w')
    temp.write("""\
python $PWNSCRIPTS/%s \\
-n %s \\
-l %s""" % (command,name,args.pwnlist))


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
        results="%s/v1/results_%s.yaml" % (name,name)
        log="%s/v1/log_%s.txt" % (name,name)
        if not exists(results) and (not exists(log) or "Results reported at" in open(log).read()):
            string="cd %s/v1; bsub -q xxl -R 'rhel50&&linux64' -oo log_%s.txt sh $PWD/run_%s.sh; cd ../.." % (name,name,name)
            if args.n:
                print string
            else:
                system(string)
""")



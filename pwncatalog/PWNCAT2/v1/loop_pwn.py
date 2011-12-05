"""
A script to loop over the PWN when
doing analysis. Example:

python loop_pwn.py -c analyze_v1.py \
        --pwndata /afs/slac/g/glast/users/rousseau/svn/pwncatalog/1FGL_reanalysis/v4/pwndata_v1.yaml  \
        --pwnphase /afs/slac/g/glast/users/rousseau/svn/pwncatalog/1FGL_reanalysis/v4/pwnphase_v1.yaml \
        -o /afs/slac/g/glast/users/rousseau/PWN_cat/1FGL_reanalysis/v4/analyze_v1/

python loop_pwn.py -c analyze.py \
        --pwndata /u/gl/lande/svn/lande/trunk/pwncatalog/1FGL_reanalysis/v4/pwndata/pwndata_v1.yaml  \
        --pwnphase /u/gl/lande/svn/lande/trunk/pwncatalog/1FGL_reanalysis/v4/pwndata/pwnphase_v1.yaml \
        -o /nfs/slac/g/ki/ki03/lande/pwncatalog/1FGL_reanalysis/v4/analyze_v1

"""
import yaml
from os.path import expandvars as e
from os.path import join
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-c", "--command", required=True)
group=parser.add_mutually_exclusive_group(required=True)
group.add_argument("--pwndata")
group.add_argument("--tevdata")
parser.add_argument("-o", "--outdir", required=True)
args,remaining_args = parser.parse_known_args()

outdir=args.outdir

if args.pwndata is not None:
    sources=yaml.load(open(args.pwndata))
    flags = '--pwndata %s' % args.pwndata
else:
    sources=yaml.load(open(args.tevdata))
    flags = '--tevdata %s' % args.tevdata

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
%s \\
%s""" % (os.getcwd(),args.command,name, flags,' '.join(remaining_args)))

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
parser.add_argument("-emin", "--emin",  default=1.0e2, type=float)
parser.add_argument("-emax", "--emax",  default=1.0e5, type=float)
args = parser.parse_args()

p=subprocess.Popen(['bjobs', '-w'],stdout=subprocess.PIPE)
queue_jobs,err=p.communicate()

for name in glob.iglob("*"):
    if isdir(name):
        log="%s/log_%s.txt" % (name,name)
        run='$PWD/%s/run_%s.sh' % (name,name)

        is_in_queue = expandvars(run) in queue_jobs
        log_exists = exists(log)
        job_failed = log_exists and 'Successfully completed' not in open(log).read()

        if not is_in_queue and (not log_exists or job_failed):
            string="cd %s; bsub -q %s -oo log_%s.txt sh $PWD/run_%s.sh; cd .." % (name,args.queue,name,name)
            if args.n:
                print string
            else:
                system(string)
""")



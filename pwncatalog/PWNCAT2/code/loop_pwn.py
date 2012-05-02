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
from os.path import expandvars
from os.path import join
import os
from textwrap import dedent
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-c", "--command", required=True)
group=parser.add_mutually_exclusive_group(required=True)
group.add_argument("--pwndata")
group.add_argument("--tevsources")
parser.add_argument("-o", "--outdir", required=True)
args,remaining_args = parser.parse_known_args()

outdir=args.outdir

if args.pwndata is not None:
    sources=yaml.load(open(expandvars(args.pwndata)))
    flags = '--pwndata %s' % args.pwndata
else:
    sources=yaml.load(open(expandvars(args.tevsources)))
    flags = '--tevsources %s' % args.tevsources

if os.path.exists(outdir):
    raise Exception("outdir %s already exists" % outdir)
os.makedirs(outdir)

for name in sources.keys():
    print name

    folder=join(outdir,name)
    os.makedirs(folder)

    file=join(folder,'run_%s.sh' % name)

    temp=open(file,'w')
    temp.write(dedent("""\
        python %s \\
            -n %s \\
            %s \\
            %s""" % (args.command,name, flags,' '.join(remaining_args))))

submit_all=join(outdir,'submit_all.sh')
temp=open(submit_all,'w')
temp.write("""submit_all */run_*.sh $@""")

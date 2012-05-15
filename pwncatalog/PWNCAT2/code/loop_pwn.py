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
from os.path import expandvars, join, exists
import os
from textwrap import dedent
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--pwndata", required=True)
parser.add_argument("-o", "--outdir", required=True)
parser.add_argument("--clobber", default=False, action='store_true')
args,remaining_args = parser.parse_known_args()

outdir=args.outdir

sources=yaml.load(open(expandvars(args.pwndata)))
flags = '--pwndata %s' % args.pwndata

if exists(outdir): 
    if not args.clobber:
        raise Exception("outdir %s already exists" % outdir)
    pass
else:
    os.makedirs(outdir)

for name in sources.keys():
    print name

    folder=join(outdir,name)

    if not exists(folder): os.makedirs(folder)

    file=join(folder,'run_%s.sh' % name)
    temp=open(file,'w')
    temp.write(dedent("""\
        python $pwncode/analyze_psr.py \\
            -n %s \\
            %s \\
            %s""" % (name, flags,' '.join(remaining_args))))

    for hypothesis in ['at_pulsar', 'point', 'extended']:
        for followup in ['plots','gtlike','variability']:
            if hypothesis != 'point' and followup == 'variability':
                continue

            file=join(folder,'followup_%s_%s_%s.sh' % (name,hypothesis,followup))
            temp=open(file,'w')
            temp.write(dedent("""\
                python $pwncode/followup_psr.py \\
                    -n %s \\
                    --hypothesis=%s
                    --followup=%s
                    %s \\
                    %s""" % (name, hypothesis, followup, flags,' '.join(remaining_args))))

submit_all=join(outdir,'submit_all.sh')
open(submit_all,'w').write("""submit_all */run_*.sh $@""")

submit_all=join(outdir,'followup_all.sh')
open(submit_all,'w').write("""for pwn in PSR*; do submit_all $pwn/followup_* $@ --requires=$pwn/results_$pwn.yaml; done""")

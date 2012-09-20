"""
A script to loop over the PWN when
doing analysis. Example:

python loop_pwn.py 
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
        python $pwncode/main.py \\
            --name %s \\
            %s \\
            %s""" % (name, flags,' '.join(remaining_args))))

    for hypothesis in ['at_pulsar', 'point', 'extended']:
        for followup in ['tsmaps','plots','gtlike','variability']:
            if hypothesis not in ['at_pulsar','point'] and  followup == 'variability':
                continue

            file=join(folder,'followup_%s_%s_%s.sh' % (name,followup,hypothesis))
            temp=open(file,'w')
            temp.write(dedent("""\
                python $pwncode/followup.py \\
                    --name %s \\
                    --hypothesis=%s \\
                    --followup=%s \\
                    %s \\
                    %s""" % (name, hypothesis, followup, flags,' '.join(remaining_args))))

submit_all=join(outdir,'submit_all.sh')
open(submit_all,'w').write("""submit_all */run_*.sh $@""")

submit_all=join(outdir,'followup_all.sh')
open(submit_all,'w').write("""#!/usr/bin/env bash
submit_list=""
for pwn in PSR*; do
    for hypothesis in at_pulsar point extended; do
        if [ -e $pwn/roi_${hypothesis}_${pwn}.dat -a -e $pwn/results_${pwn}_pointlike_${hypothesis}.yaml ]; then
            submit_list="$pwn/followup_${pwn}_*_${hypothesis}.sh $submit_list"
        fi
    done
done
submit_all $submit_list $@""")

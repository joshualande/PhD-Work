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

    for hypothesis in ['at_pulsar','point','extended']:
        for followup in ['altdiff']:
            for dist in ['Lorimer', 'SNR']:
                for halo in [4,10]:
                    for TS in [150, 100000]:
                        file=join(folder,'followup_%s_%s_dist_%s_halo_%s_TS_%s_%s.sh' % (name,followup,dist,halo,TS,hypothesis))
                        temp=open(file,'w')
                        temp.write(dedent("""\
                            python $pwncode/followup.py \\
                                --name %s \\
                                --hypothesis=%s \\
                                --followup=%s \\
                                --dist=%s --halo=%s --TS=%s \\
                                %s \\
                                %s""" % (name, hypothesis, followup, dist, halo, TS, flags,' '.join(remaining_args))))


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
submit_all $submit_list $@ -v altdiff""")


submit_all=join(outdir,'altdiff.sh')
open(submit_all,'w').write("""#!/usr/bin/env bash
submit_list=""

for pwn in PSRJ0007+7303 PSRJ0205+6449 PSRJ0534+2200 \
    PSRJ0631+1036 PSRJ0633+1746 PSRJ0734-1559 \
    PSRJ0835-4510 PSRJ0908-4913 PSRJ1023-5746 \
    PSRJ1044-5737 PSRJ1105-6107 PSRJ1112-6103 \
    PSRJ1119-6127 PSRJ1124-5916 PSRJ1410-6132 \
    PSRJ1513-5908 PSRJ1620-4927 PSRJ1746-3239 \
    PSRJ1747-2958 PSRJ1809-2332 PSRJ1813-1246 \
    PSRJ1836+5925 PSRJ1838-0537 PSRJ2021+4026 \
    PSRJ2032+4127 PSRJ2055+2539 PSRJ0034-0534 \
    PSRJ0102+4839 PSRJ0218+4232 PSRJ0340+4130 \
    PSRJ1658-5324 PSRJ2043+1711 PSRJ2124-3358 \
    PSRJ2302+4442; do

    for hypothesis in at_pulsar point extended; do
        if [ -e $pwn/roi_${hypothesis}_${pwn}.dat -a -e $pwn/results_${pwn}_pointlike_${hypothesis}.yaml ]; then
            submit_list="$pwn/followup_${pwn}_altdiff_*_${hypothesis}.sh $submit_list"
        fi
    done
done
submit_all $submit_list $@ -q kipac-ibq""")

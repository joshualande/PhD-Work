#!/usr/bin/env python
from os.path import join, expandvars, exists
from os import makedirs
from textwrap import dedent

# version 1
num=10
savedir = expandvars('$fitdiffdata/v1')


for difftype in ['galactic', 'isotropic', 'sreekumar']:
    print difftype
    for location in ['highlat','lowlat']:
        print location
        for emin,emax in [[1e2,1e5], [1e4, 1e5]]:
            print emin,emax

            subdir = join(savedir, 'diff_%s_loc_%s_emin_%g_emax_%g' % (difftype, location, emin, emax))

            for i in range(num):
                print i
                istr='%05d' % i

                jobdir = join(subdir,istr)
                if not exists(jobdir): makedirs(jobdir)

                run = join(jobdir,'run.sh')
                open(run,'w').write(dedent("""\
                python $fitdiffcode/simulate.py %g \\
                        --difftype=%s --location=%s --emin=%g --emax=%g""" % (i,difftype,location,emin,emax)))

submit_all = join(savedir,'submit_all.sh')
open(submit_all,'w').write("submit_all */*/run.sh $@")

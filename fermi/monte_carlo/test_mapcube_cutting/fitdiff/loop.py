#!/usr/bin/env python
from os.path import join, expandvars, exists
from os import makedirs
from textwrap import dedent

# version 1
#num=1000
#savedir = expandvars('$fitdiffdata/v1')

# version 2
# Primary difference: 8bins per decade
#num=1000
#savedir = expandvars('$fitdiffdata/v2')


# version 3
# Primary difference: gtlike, new sreekumar code
#num=1000
#savedir = expandvars('$fitdiffdata/v3')

# Primary difference: fix l,b cut
#num=1000
#savedir = expandvars('$fitdiffdata/v4')

# Primary difference: diffuse_pad=10, energy_pad=2
#num=1000
#savedir = expandvars('$fitdiffdata/v5')

# Primary difference: diffuse_pad=10, energy_pad=2
num=1000
savedir = expandvars('$fitdiffdata/v6')

# Primary difference: diffuse_pad=10, energy_pad=2
num=100
savedir = expandvars('$fitdiffdata/v7')

for difftype in ['galactic', 'isotropic', 'sreekumar']:
    print difftype
    for location in ['highlat','lowlat']:
        print location
        for emin,emax in [[1e2,1e5], [1e4, 1e5]]:
            print emin,emax

            subdir = join(savedir, 'diff_%s_loc_%s_emin_%g_emax_%g' % (difftype, location, emin, emax))

            for i in range(num):
                istr='%05d' % i

                jobdir = join(subdir,istr)
                if not exists(jobdir): makedirs(jobdir)

                run = join(jobdir,'run.sh')
                open(run,'w').write(dedent("""\
                python $fitdiffcode/simulate.py %g \\
                        --difftype=%s --location=%s --emin=%g --emax=%g""" % (i,difftype,location,emin,emax)))

submit_all = join(savedir,'submit_all.sh')
open(submit_all,'w').write("submit_all */*/run.sh $@")

from os.path import join, expandvars, exists
from os import makedirs

# version 1
#num=10000
#savedir = expandvars('$tsext_plane_data/v1')

# version 2 - better fluxes
#num=1000
#savedir = expandvars('$tsext_plane_data/v2')

# version 3 - better fluxes
#num=1000
#savedir = expandvars('$tsext_plane_data/v3')

# version 4 - better fluxes
#num=1000
#savedir = expandvars('$tsext_plane_data/v4')

# version 5 - better fluxes
#num=10000
#savedir = expandvars('$tsext_plane_data/v5')

# version 6 - change spatial range to be smaller.
#num=50
#savedir = expandvars('$tsext_plane_data/v6')

# version 7 - better flux calcuation 
#num=500
#savedir = expandvars('$tsext_plane_data/v7')

# version 8 - weighted livetime should be more correct
#num=1000
#savedir = expandvars('$tsext_plane_data/v8')

# version 9 - change flux
#num=10000
#savedir = expandvars('$tsext_plane_data/v9')

# version 10 - change flux
#num=1000
#savedir = expandvars('$tsext_plane_data/v10')

# version 11 - change flux
#num=1000
#savedir = expandvars('$tsext_plane_data/v11')

# version 12 - change flux
num=110000
savedir = expandvars('$tsext_plane_data/v12')

for i in range(num):
    istr='%05d' % i

    jobdir = join(savedir,istr)
    if not exists(jobdir): makedirs(jobdir)

    run = join(jobdir,'run.sh')
    open(run,'w').write("""python $tsext_plane_code/simulate.py %g""" % i)

submit_all = join(savedir,'submit_all.sh')
open(submit_all,'w').write(
        "submit_all */run.sh $@"
    )




from lande.utilities.simtools import SimBuilder

# version 1
#num=100
#savedir = expandvars('$w44simdata/v1')

# version 2
#num=2000
#savedir = expandvars('$w44simdata/v2')

# version 3 - save r68
#num=2000
#savedir = expandvars('$w44simdata/v3')

# version 4 - better mapcube cutting
#num=100
#savedir = expandvars('$w44simdata/v4')

# version 5 - no edisp, save out r68 for MC
#num=100
#savedir = expandvars('$w44simdata/v5')

# version 6 - w/ edisp in simulation, w/ gtlike
#num=100
#savedir = expandvars('$w44simdata/v6')

# version 7 - enable energy dispersion fitting in gtlike, fix annoygin warnings
#num=1000
#savedir = expandvars('$w44simdata/v7')
#
#from os.path import join, expandvars, exists
#from os import makedirs
#for i in range(num):
#    istr='%05d' % i
#
#    jobdir = join(savedir,istr)
#    if not exists(jobdir): makedirs(jobdir)
#
#    run = join(jobdir,'run.sh')
#    open(run,'w').write("""python $w44simcode/simulate.py %g""" % i)
#
#submit_all = join(savedir,'submit_all.sh')
#open(submit_all,'w').write("submit_all */run.sh $@")




# version 8 - unbinned likelihood
b = SimBuilder(
        savedir='$w44simdata/v8',
        code='$w44simcode/simulate.py',
        num=100,
        )
b.build()


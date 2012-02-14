import random
from textwrap import dedent
from os.path import expandvars,join,exists
from os import makedirs,getcwd

random.seed(0)

num=100


# v4
#basedir =  expandvars('$pwndata/monte_carlo/extul/v4/')
#for index_mc,min_flux,max_flux in [[1.5, 1.5e-9, 4.5e-9], 
#                                   [2,   5e-9,   1.5e-8],
#                                   [2.5, 1.5e-8, 4.5e-8],
#                                   [3,   2.5e-8, 7.5e-8]]:

# v5
#basedir =  expandvars('$pwndata/monte_carlo/extul/v5/')
#for index_mc,min_flux,max_flux in [[1.5, 1e-9,   1e-8], 
#                                   [2,   5e-9,   1e-8],
#                                   [2.5, 1e-8,   1.5e-8],
#                                   [3,   1.5e-8, 2.5e-8]]:

# v6
basedir =  expandvars('$pwndata/monte_carlo/extul/v6/')
for index_mc,min_flux,max_flux in [[1.5, 1e-9,   1e-8], 
                                   [2,   3e-9,   2e-8],
                                   [2.5, 1e-8,   2e-8],
                                   [3,   1.5e-8, 2e-8]]:

    workdir = join(basedir,'index_%g' % (index_mc))

    for i in xrange(num):

        istr='%05d' % i


        jobdir = join(workdir,istr)

        if not exists(jobdir): makedirs(jobdir)

        run = open(join(jobdir,'run.sh'),'w')
        run.write(dedent("""\
            python $pwnmc/extul/extul.py \\
                --index=%g \\
                --min-flux=%g \\
                --max-flux=%g \\
                %g""" % (index_mc,min_flux,max_flux,i)))
        run.close()


submit_all = join(basedir,'submit_all.sh')
open(submit_all,'w').write(
    "submit_all */*/run.sh $@"
)

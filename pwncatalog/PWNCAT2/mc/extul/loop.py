import random
from textwrap import dedent
from os.path import expandvars,join,exists
from os import makedirs,getcwd

random.seed(0)

num=10

basedir =  expandvars('$pwndata/monte_carlo/extul/v2/')

# Note, flux here is defined as the 100MeV to 316GeV flux
for index,flux in [[1.5, 1e-9], 
                   [2,   5e-9],
                   [2.5, 1e-8],
                   [3,   1e-7]]:

    workdir = join(basedir,'index_%g' % (index))

    for i in xrange(num):

        istr='%05d' % i


        jobdir = join(workdir,istr)

        if not exists(jobdir): makedirs(jobdir)

        run = open(join(jobdir,'run.sh'),'w')
        run.write(dedent("""\
            python $pwnmc/extul/extul.py \\
                --index=%g \\
                --flux=%g \\
                %g""" % (index,flux,i)))
        run.close()


submit_all = join(basedir,'submit_all.sh')
open(submit_all,'w').write(
    "submit_all */*/run.sh $@"
)

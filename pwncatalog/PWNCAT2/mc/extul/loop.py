import random
from textwrap import dedent
from os.path import expandvars,join,exists
from os import makedirs,getcwd

random.seed(0)

num=50


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
#basedir =  expandvars('$pwndata/monte_carlo/extul/v6/')
#for index_mc,min_flux,max_flux in [[1.5, 1e-9,   1e-8], 
#                                   [2,   3e-9,   2e-8],
#                                   [2.5, 1e-8,   2e-8],
#                                   [3,   1.5e-8, 2e-8]]:

# v7
#basedir =  expandvars('$pwndata/monte_carlo/extul/v7/')
#for index_mc,min_flux,max_flux in [[1.5, 1e-9,   2e-8], 
#                                   [2,   5e-9,   2e-8],
#                                   [2.5, 1e-8,   3.5e-8],
#                                   [3,   1.5e-8, 3.5e-8]]:

# v8
basedir =  expandvars('$pwndata/monte_carlo/extul/v8/')
for index_mc,min_flux,max_flux,min_extension, max_extension, type in \
                                                                     [[1.5, 1e-9,   2e-8,     0,  3.0,  'dim'], 
                                                                      [2,   4e-9,   2e-8,     0,  3.0,  'dim'],
                                                                      [2.5, 1e-8,   1.75e-8,  0,  3.0,  'dim'],
                                                                      [3,   1.5e-8, 2e-8,     0,  3.0,  'dim'],

                                                                      [1.5, 1e-6, 1e-6, 0, 0.25,   'bright'], 
                                                                      [2,   1e-6, 1e-6, 0, 0.25,   'bright'],
                                                                      [2.5, 1e-6, 1e-6, 0, 0.25,   'bright'],
                                                                      [3,   1e-6, 1e-6, 0, 0.25,   'bright'],

                                       ]:


    workdir = join(basedir,'%s_index_%g' % (type,index_mc))

    for i in xrange(num):

        istr='%05d' % i


        jobdir = join(workdir,istr)

        if not exists(jobdir): makedirs(jobdir)

        run = open(join(jobdir,'run.sh'),'w')
        run.write(dedent("""\
            python $pwnmc/extul/extul.py \\
                --type=%s \\
                --index=%g \\
                --min-flux=%g \\
                --max-flux=%g \\
                --min-extension=%g
                --max-extension=%g
                %g""" % (type,index_mc,min_flux,max_flux,min_extension,max_extension,i)))
        run.close()


submit_all = join(basedir,'submit_all.sh')
open(submit_all,'w').write(
    "submit_all */*/run.sh $@"
)

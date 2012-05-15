import random
from textwrap import dedent
from os.path import expandvars,join,exists
from os import makedirs,getcwd

random.seed(0)



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
#basedir =  expandvars('$pwndata/monte_carlo/extul/v8/')
#for index_mc,min_flux,max_flux,min_extension, max_extension, type in \
#     [[1.5,   1e-9,    2e-8, 0, 2.0,  'dim'], 
#      [  2,   4e-9,    2e-8, 0, 2.0,  'dim'],
#      [2.5,   1e-8, 1.75e-8, 0, 2.0,  'dim'],
#      [  3, 1.5e-8,    2e-8, 0, 2.0,  'dim'],
#
#      [1.5,   5e-8,   5e-8, 0, 0.5,   'bright'], 
#      [  2, 1.3e-7, 1.3e-7, 0, 0.5,   'bright'],
#      [2.5, 2.1e-7, 2.1e-7, 0, 0.5,   'bright'],
#      [  3, 2.5e-7, 2.5e-7, 0, 0.5,   'bright'],
#                                       ]:

# v9
#basedir =  expandvars('$pwndata/monte_carlo/extul/v9/')
#for index_mc,min_flux,max_flux,min_extension, max_extension, type in \
#     [[1.5,   1e-9,  1.6e-8, 0, 2.0,  'dim'], 
#      [  2,   4e-9,    2e-8, 0, 2.0,  'dim'],
#      [2.5,   1e-8, 2.31e-8, 0, 2.0,  'dim'],
#      [  3, 1.5e-8,  2.4e-8, 0, 2.0,  'dim'],
#
#      [1.5,  4.6e-8,  4.6e-8, 0, 0.5,   'bright'], 
#      [  2, 1.15e-7, 1.15e-7, 0, 0.5,   'bright'],
#      [2.5,  2.1e-7,  2.1e-7, 0, 0.5,   'bright'],
#      [  3,  2.8e-7,  2.8e-7, 0, 0.5,   'bright'],
#                                       ]:

# v10 & v11 & & v12 & v13
#basedir =  expandvars('$pwndata/monte_carlo/extul/v10/')
#basedir =  expandvars('$pwndata/monte_carlo/extul/v11/')
#basedir =  expandvars('$extuldata/v12/')
#  - note primiary difference in v12: 8bins per decade instead of 4
basedir =  expandvars('$extuldata/v13/')
num=1000
for index_mc,min_flux,max_flux,min_extension, max_extension, type in \
     [[1.5,   1e-9,  1.8e-8, 0, 2.0,  'dim'], 
      [  2,   4e-9,  2.2e-8, 0, 2.0,  'dim'],
      [2.5,   1e-8, 2.31e-8, 0, 2.0,  'dim'],
      [  3, 1.5e-8,  2.4e-8, 0, 2.0,  'dim'],

      [1.5,  4.6e-8,  4.6e-8, 0, 0.25,   'bright'], 
      [  2, 1.15e-7, 1.15e-7, 0, 0.25,   'bright'],
      [2.5,  2.1e-7,  2.1e-7, 0, 0.25,   'bright'],
      [  3,  2.8e-7,  2.8e-7, 0, 0.25,   'bright'],
                                       ]:

    workdir = join(basedir,'%s_index_%g' % (type,index_mc))

    for i in xrange(num):

        istr='%05d' % i


        jobdir = join(workdir,istr)

        if not exists(jobdir): makedirs(jobdir)

        run = open(join(jobdir,'run.sh'),'w')
        run.write(dedent("""\
            python $extulcode/extul.py \\
                --type=%s \\
                --index=%g \\
                --min-flux=%g \\
                --max-flux=%g \\
                --min-extension=%g \\
                --max-extension=%g \\
                %g""" % (type,index_mc,min_flux,max_flux,min_extension,max_extension,i)))
        run.close()


submit_all = join(basedir,'submit_all.sh')
open(submit_all,'w').write(
    "submit_all */*/run.sh $@"
)

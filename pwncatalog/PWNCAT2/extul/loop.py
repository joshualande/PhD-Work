import random
from os.path import expandvars,join,exists
from os import makedirs,getcwd

random.seed(0)

num=300

basedir =  expandvars('$pwndata/monte_carlo/extul/v1/')



for i in xrange(num):

    istr='%05d' % i

    jobdir = join(basedir,istr)

    if not exists(jobdir): 
        makedirs(jobdir)

    run = open(join(jobdir,'run.sh'),'w')
    run.write(r"""python %s/extul.py  %d""" % (getcwd(),i))
    run.close()


import os
from os.path import expandvars,join,exists
from os import makedirs,getcwd

num=100000

print 'putting the folder in the current directory, for now'
workdir =  expandvars('/nfs/slac/g/ki/ki03/lande/compare_flight_mc_psf/v1')

if not exists(workdir): makedirs(workdir) 

submit_all=open(join(workdir,'submit_all.sh'),'w')
submit_all.write(r"""
for i in `seq 0 %s`; do
    istr=`printf %%07d $i`
    cd $istr
    if [ ! -e log.txt ]; then
        bsub -q xxl -oo log.txt sh $PWD/run.sh
    fi
    cd ..
done
    """ % num
)
submit_all.close()


for i in xrange(num+1):
    if i%100 == 0: print i

    istr='%07d' % i

    jobdir = join(workdir,istr)

    if not exists(jobdir): 
        makedirs(jobdir)

    run = open(join(jobdir,'run.sh'),'w')
    run.write("python %s/monte_carlo.py %s" % (getcwd(),i))
    run.close()


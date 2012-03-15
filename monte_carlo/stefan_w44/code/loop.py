#exit 1
for type in FileFunction LogParabola; do
    for i in `seq 0 0`; do
        istr=`printf %05d $i`
        folder=${type}_simulation/$istr/
        mkdir -p $folder
        sub="python $PWD/simulate.py $i --spectrum $type"
        echo $sub
        bsub -q xxl -oo $folder/log_$type.txt $sub
    done
done

from os.path import join, expandvars, exists
from os import makedirs

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
num=100
savedir = expandvars('$w44simdata/v4')

for i in range(num):
    istr='%05d' % i

    jobdir = join(savedir,istr)
    if not exists(jobdir): makedirs(jobdir)

    run = join(jobdir,'run.sh')
    open(run,'w').write("""python $w44simcode/simulate.py %g""" % i)

submit_all = join(savedir,'submit_all.sh')
open(submit_all,'w').write("submit_all */run.sh $@")




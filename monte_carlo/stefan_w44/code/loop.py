from os.path import join, expandvars, exists
from os import makedirs

num=5
savedir = expandvars('$stefan_w44_data/v1')

for model in ['FileFunction', 'LogParabola']:

    subdir = join(savedir, model)

    for i in range(num):
        istr='%05d' % i

        jobdir = join(subdir,istr)
        if not exists(jobdir): makedirs(jobdir)

        run = join(jobdir,'run.sh')
        open(run,'w').write("""python $stefan_w44_code/simulate.py %g --spectrum %s""" % (i,model))

submit_all = join(savedir,'submit_all.sh')
open(submit_all,'w').write("submit_all */*/run.sh $@")

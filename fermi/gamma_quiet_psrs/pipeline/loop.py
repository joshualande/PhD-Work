from os.path import join
from textwrap import dedent
from itertools import product

from lande.utilities.save import loaddict
from lande.utilities.jobtools import JobBuilder


class PipelineBuilder(JobBuilder):
    def build_followup(self, code, hypotheses, followups):
        for perm in product(*self.values):
            subdir = self.build_subdir(perm)
            args = self.build_args(perm)

            for hypothesis in hypotheses:
                for followup in followups:
                    run = join(subdir,'followup_%s_%s.sh' % (hypothesis,followup))
                    open(run,'w').write("python %s --hypothesis=%s --followup=%s %s" % (code,args,hypothesis,followup))


            followup_all = join(self.savedir,'followup_all.sh')
            open(followup_all,'w').write(dedent("""
            #!/usr/bin/env bash
            submit_list=""
            for pwn in PSR*; do
                for hypothesis in at_pulsar point extended; do
                    if [ -e $pwn/roi_${hypothesis}_${pwn}.dat -a -e $pwn/results_${pwn}_pointlike_${hypothesis}.yaml ]; then
                        submit_list="$pwn/followup_${pwn}_*_${hypothesis}.sh $submit_list"
                    fi
                done
            done
            submit_all $submit_list $@
            """))


radiopsr_data='$gamma_quiet_psrs_data/gamma_quiet_psrs_data.yaml'
names=loaddict(radiopsr_data).keys()
bigfile='$lat2pc/BigFile/Pulsars_BigFile_v20121002103223.fits'

params=dict(name=names, 
            bigfile=bigfile)
params['radiopsr-data']=radiopsr_data
b = PipelineBuilder(
    savedir='$gamma_quiet_psrs_analysis/v1',
    code='$gamma_quiet_psrs_pipeline/main.py',
    params=params,
    short_folder_names=True,
)
b.build()
b.build_followup(
    code = '$gamma_quiet_psrs_pipeline/followup.py',
    hypotheses=['at_pulsar','point','extended'],
    followups=['gtlike','plots','tsmaps'])

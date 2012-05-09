
from uw.pulsar.phase_range import PhaseRange
from os.path import join, expandvars, exists
from os import makedirs
import yaml


pwndata=yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_data_lande.yaml')))

r='$pwndata/off_peak/off_peak_bb/pwncat2/v4'

pwnlist = sorted(pwndata.keys())

d=dict()

print 'len',len(pwnlist)
for i,pwn in enumerate(pwnlist):

    results = yaml.load(open(expandvars(join(r,'analysis',pwn,'results_%s.yaml' % pwn))))

    ft1 = pwndata[pwn]['ft1']
    off_peak_phase = results['off_peak_phase']

    optimal_emin=results['optimal_emin']
    emax=results['emax']
    optimal_radius=results['optimal_radius']

    f = PhaseRange(off_peak_phase).tolist(dense=True)
    d[pwn] = dict(
        phase = f,
        optimal_emin=optimal_emin,
        emax=emax,
        optimal_radius=optimal_radius,
    )

output=yaml.dump(d).replace("'","")
print output

merged=expandvars(join(r,'merged'))
if not exists(merged): makedirs(merged)
open(join(merged,'merged.yaml'),'w').write(output)

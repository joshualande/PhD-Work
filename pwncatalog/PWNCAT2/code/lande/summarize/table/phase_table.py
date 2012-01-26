from table_helper import get_pwnlist,get_results,table_name,write_latex
from lande_toolbag import OrderedDefaultdict

from os.path import join as j
def get_phase(pwn):
    folder='$pwndata/off_peak/off_peak_bb/pwncat2/v1/'
    file=j(folder,pwn,'v1','results_%s.yaml' % pwn)
    r=yaml.load(file)
    phase=r['bayesian_blocks']['off_peak']
    return phase

def all_energy_table(pwnlist):

    table = OrderedDefaultdict(list)
    phase_name='PHASE'

    for pwn in pwnlist:
        table['PSR'].append(table_name(pwn))

        phase=get_pase(pwn)
        table[phase_name]=str(phase)

    write_latex(table,
                filebase='off_peak_phase_range',
                latexdict = dict(units={
                                     #flux_name:r'($10^{-9} \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                 }))


pwnlist=get_pwnlist()
all_energy_table(pwnlist)

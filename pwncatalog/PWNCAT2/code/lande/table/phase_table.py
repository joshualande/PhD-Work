from table_helper import get_pwnlist,get_results,table_name,write_latex
from lande_toolbag import OrderedDefaultdict

import yaml
from os.path import join as j,expandvars

def get_phase(pwn):
    phase = yaml.load('$pwncode/pwndata/pwncat2_phase_lande.yaml')[pwn]['phase']
def all_energy_table(pwnlist):

    table = OrderedDefaultdict(list)
    phase_name='PHASE'

    for pwn in pwnlist:
        table['PSR'].append(table_name(pwn))

        phase=get_phase(pwn)
        table[phase_name]=str(phase)

    write_latex(table,
                filebase='off_peak_phase_range',
                latexdict = dict(units={
                                     #flux_name:r'($10^{-9} \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                 }))


pwnlist=get_pwnlist()
all_energy_table(pwnlist)

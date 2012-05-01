from table_helper import get_pwnlist,get_results,table_name,write_latex,write_confluence
from lande.utilities.tools import OrderedDefaultDict

import yaml
from os.path import join as j,expandvars

confluence=True

def all_energy_table(pwnlist):

    data = yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_phase_lande.yaml')))

    table = OrderedDefaultDict(list)

    psr_name='PSR'
    phase_name='Phase'
    optimal_emin_name='Optimal Emin' if confluence else r'Optimal $E_\text{min}$'
    optimal_radius_name='Optimal radius'

    for pwn in pwnlist:
        print pwn
        table[psr_name].append(table_name(pwn,confluence))

        phase=data[pwn]['phase']
        optimal_emin=data[pwn]['optimal_emin']
        optimal_radius=data[pwn]['optimal_radius']

        table[phase_name].append('%.2f - %.2f' % tuple(phase))
        table[optimal_emin_name].append('%.2f' % optimal_emin)
        table[optimal_radius_name].append('%.2f' % optimal_radius)

    print yaml.dump(table)
    if confluence:
        write_confluence(table, filebase='phase_range')
    else:
        write_latex(table, filebase='phase_range')


pwnlist=get_pwnlist()
all_energy_table(pwnlist)

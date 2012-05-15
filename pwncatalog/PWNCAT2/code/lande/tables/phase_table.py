import yaml
from os.path import join as j,expandvars
import numbers

from uw.pulsar.phase_range import PhaseRange

from lande.utilities.tools import OrderedDefaultDict
from lande.utilities.table import get_confluence

from table_helper import get_pwnlist,get_results,write_latex,write_confluence
from table_helper import PWNFormatter


confluence=get_confluence()

format=PWNFormatter(confluence=confluence, precision=2)

def all_energy_table(pwnlist):

    data = yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_phase_lande.yaml')))

    table = OrderedDefaultDict(list)

    psr_name='PSR'
    phase_name='Phase'
    optimal_emin_name='Optimal Emin' if confluence else r'Optimal $E_\text{min}$'
    optimal_radius_name='Optimal radius'

    for pwn in pwnlist:
        print pwn
        table[psr_name].append(format.pwn(pwn))

        phase=PhaseRange(data[pwn]['phase'])
        optimal_emin=data[pwn]['optimal_emin']
        optimal_radius=data[pwn]['optimal_radius']

        table[phase_name].append(phase.pretty_format())
        table[optimal_emin_name].append('%.2f' % optimal_emin)
        table[optimal_radius_name].append('%.2f' % optimal_radius)

    print yaml.dump(table)
    if confluence:
        write_confluence(table, filebase='phase_range')
    else:
        write_latex(table, filebase='phase_range')


pwnlist=get_pwnlist()
all_energy_table(pwnlist)

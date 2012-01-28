from table_helper import get_pwnlist,get_results,table_name,write_latex
from lande_toolbag import OrderedDefaultdict

import yaml
from os.path import join as j,expandvars

def get_phase(pwn):
    phase = yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_phase_lande.yaml')))
    return phase[pwn]['phase']

def all_energy_table(pwnlist):

    table = OrderedDefaultdict(list)

    psr_name='PSR'
    phase_name='Phase'

    obs_id = 'ObsID'
    distance = 'Distance'
    rejected = 'Observation period rejected (MJD)'

    for pwn in pwnlist:
        print pwn
        table[psr_name].append(table_name(pwn))

        phase=get_phase(pwn)
        table[obs_id].append(r'\nodata')
        table[phase_name].append('%.2f-%.2f' % tuple(phase))

        table[distance].append(r'\nodata')
        table[rejected].append(r'\nodata')

    print table
    write_latex(table,
                filebase='off_peak_phase_range',
                latexdict = dict(
                    units=dict(
                        distance='kpc'
                        #flux_name:r'($10^{-9}\ \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                        )
                    )
               )


pwnlist=get_pwnlist()
all_energy_table(pwnlist)

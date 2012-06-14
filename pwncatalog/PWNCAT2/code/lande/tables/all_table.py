from os.path import expandvars

import yaml
import numpy as np

from skymaps import SkyDir

from uw.pulsar.phase_range import PhaseRange

from lande.utilities.table import get_confluence
from lande.utilities.tools import OrderedDefaultDict

from table_helper import get_pwnlist,get_results,write_latex, write_confluence, BestHypothesis,PWNFormatter

confluence=get_confluence()

format=PWNFormatter(confluence=confluence, precision=2)

def localization_table(pwnlist):

    table = OrderedDefaultDict(list)

    psr_name='PSR'
    phase_name='Phase'
    ts_point_name=r'$\ts_\text{point}$' if not confluence else 'TS_point'
    ts_ext_name=r'\tsext' if not confluence else 'TS_ext'
    ts_cutoff_name = r'$\ts_\text{cutoff}$' if not confluence else 'TS_cutoff'
    flux_name = r'$F_{0.1-316}$' if not confluence else 'F_(0.1-316)'
    index_name = r'$\Gamma$' if not confluence else 'Gamma'
    cutoff_name = r'$E_\text{cutoff}$' if not confluence else 'E_cutoff'

    data = yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_phase_lande.yaml')))

    for pwn in pwnlist:
        print pwn

        phase=PhaseRange(data[pwn]['phase'])


        results = get_results(pwn)

        if results is None:
            # job crashed/not finished
            table[psr_name].append(format.pwn(pwn))
            table[phase_name].append(phase.pretty_format())
            table[ts_point_name].append('None')
            table[ts_ext_name].append('None')
            table[ts_cutoff_name].append('None')
            table[flux_name].append('None')
            table[index_name].append('None')
            table[cutoff_name].append('None')
        else:

            point_gtlike = results['point']['gtlike']
            point_pointlike = results['point']['pointlike']

            extended_pointlike = results['extended']['pointlike']
            extended_gtlike = results['extended']['gtlike']
            

            b = BestHypothesis(results)
            gtlike = b.gtlike
            pointlike = b.pointlike
            type = b.type
            cutoff = b.cutoff

            ts_point = b.ts_point
            ts_ext = b.ts_ext
            ts_cutoff = b.ts_cutoff

            if type == 'upper_limit': 
                continue

            phase=PhaseRange(data[pwn]['phase'])

            table[psr_name].append(format.pwn(pwn))
            table[phase_name].append(phase.pretty_format())

            table[ts_point_name].append(format.value(ts_point,precision=1))
            table[ts_ext_name].append(format.value(ts_ext,precision=1))
            table[ts_cutoff_name].append(format.value(ts_cutoff,precision=1))


                
    filebase='off_peak_all'
    if confluence:
        write_confluence(table,
                         filebase=filebase,
                         units={
                             flux_name:r'(10^-9 erg cm^-2 s^-1)',
                             cutoff_name:r'(GeV)',
                         })
    else:
        write_latex(table,
                    preamble=r'\tabletypesize{\tiny}',
                    filebase=filebase,
                    units={
                        flux_name:r'($10^{-9}$\ erg\,cm$^{-2}$\,s$^{-1}$)',
                        cutoff_name:r'(GeV)',
                    },
                   )



pwnlist=get_pwnlist()
localization_table(pwnlist)


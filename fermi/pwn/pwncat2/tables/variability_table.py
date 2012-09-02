from os.path import join,exists,expandvars
import yaml

from lande.fermi.pipeline.pwncat2.table import get_pwnlist,get_results,write_latex,write_confluence
from lande.fermi.pipeline.pwncat2.table import PWNFormatter

from lande.utilities.tools import OrderedDefaultDict
from lande.utilities.table import get_confluence

confluence=get_confluence()

format=PWNFormatter(confluence=confluence, precision=2)

ts_var_folder = '$pwndata/spectral/v10/variability/v3/'

def cutoff_table(pwnlist):

    table = OrderedDefaultDict(list)
    psr_name='PSR'
    ts_var_name = r'$\ts_\text{var}$' if not confluence else 'TS_var'

    t='gtlike'

    for pwn in pwnlist:

        print pwn

        table[psr_name].append(format.pwn(pwn))

        var = expandvars(join(ts_var_folder,pwn,'results_%s.yaml' % pwn))
        if exists(var): 

            v = yaml.load(open(var))

            ts_var = v['TS_var'][t]
            table[ts_var_name].append(format.value(ts_var, precision=1))
        else:
            table[ts_var_name].append(r'None')

    filebase='variability'
    if confluence:
        write_confluence(table,filebase=filebase)
    else:
        write_latex(table,filebase=filebase)


pwnlist=get_pwnlist()
cutoff_table(pwnlist)


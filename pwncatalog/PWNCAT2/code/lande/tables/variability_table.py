from table_helper import get_pwnlist,get_results,write_latex,write_confluence
from table_helper import PWNFormatter
from lande.utilities.tools import OrderedDefaultDict
from os.path import join,exists,expandvars
import yaml

confluence=True

format=PWNFormatter(confluence=confluence, precision=2)

ts_var_folder = '$pwndata/spectral/v10/variability/v3/'

def cutoff_table(pwnlist):

    table = OrderedDefaultDict(list)
    psr_name='PSR'
    #ts_point_name = r'$\ts_\text{point}$'
    ts_var_name = r'$\ts_\text{var}$' if not confluence else 'TS_var'

    t='gtlike'

    for pwn in pwnlist:
        #results = get_results(pwn)
        #if results is None: continue

        #ts_point = results['point'][t]['TS']

        #if ts_point < 25:
        #    continue

        print pwn

        table[psr_name].append(format.pwn(pwn))

        #table[ts_point_name].append('%.1f' % ts_point)

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


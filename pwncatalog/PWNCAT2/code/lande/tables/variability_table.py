from table_helper import get_pwnlist,get_results,table_name,write_latex
from lande_toolbag import OrderedDefaultdict
from os.path import join,exists,expandvars
import yaml


ts_var_folder = '$pwndata/spectral/v10/variability/v3/'

def cutoff_table(pwnlist):

    table = OrderedDefaultdict(list)
    psr_name='PSR'
    #ts_point_name = r'$\ts_\text{point}$'
    ts_var_name = r'$\ts_\text{var}$'

    t='gtlike'

    for pwn in pwnlist:
        #results = get_results(pwn)
        #if results is None: continue

        #ts_point = results['point'][t]['TS']

        #if ts_point < 25:
        #    continue

        print pwn

        table[psr_name].append(table_name(pwn))

        #table[ts_point_name].append('%.1f' % ts_point)

        var = expandvars(join(ts_var_folder,pwn,'results_%s.yaml' % pwn))
        if exists(var): 

            v = yaml.load(open(var))

            ts_var = v['TS_var'][t]
            table[ts_var_name].append('%.1f' % ts_var)
        else:
            table[ts_var_name].append(r'None')

    write_latex(table,filebase='variability')


pwnlist=get_pwnlist()
cutoff_table(pwnlist)


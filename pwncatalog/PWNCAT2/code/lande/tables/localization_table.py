from lande.fermi.pipeline.pwncat2.table import get_pwnlist,get_results,write_latex, write_confluence, BestHypothesis
from lande.fermi.pipeline.pwncat2.table import PWNFormatter

from lande.utilities.tools import OrderedDefaultDict
import numpy as np
from skymaps import SkyDir
from lande.utilities.table import get_confluence

confluence=get_confluence()

format=PWNFormatter(confluence=confluence, precision=2)

def localization_table(pwnlist):

    table = OrderedDefaultDict(list)

    psr_name='PSR'
    l_name='GLON'
    b_name='GLAT'
    ts_point_name =r'$\ts_\text{point}$' if not confluence else 'TS_point'
    ts_ext_name =r'\tsext' if not confluence else 'TS_ext'
    offset_name = 'Offset'
    ext_name = 'Extension'
    poserr_name = 'Pos Err'

    for pwn in pwnlist:

        results = get_results(pwn)

        print pwn

        if results is None or \
           not results.has_key('point') or \
           not results['point'].has_key('gtlike') or \
           not results['point'].has_key('pointlike') or \
           not results.has_key('extended') or \
           not results['extended'].has_key('gtlike') or \
           not results['extended'].has_key('pointlike'):
            continue
            

        at_pulsar_gtlike = results['at_pulsar']['gtlike']
        at_pulsar_pointlike = results['at_pulsar']['pointlike']
        

        point_gtlike = results['point']['gtlike']
        point_pointlike = results['point']['pointlike']
        
        extended_gtlike = results['extended']['gtlike']
        extended_pointlike = results['extended']['pointlike']

        ts_point = point_gtlike['TS']
        ts_ext = max(extended_gtlike['ts_ext'],0)

        b = BestHypothesis(results)
        gtlike = b.gtlike
        pointlike = b.pointlike
        type = b.type



        if type != 'upper_limit':

            l,b=pointlike['position']['gal']

            try:
                poserr='%.2f' % pointlike['spatial_model']['ellipse']['lsigma']
            except:
                poserr='None'

            o = np.degrees(SkyDir(*pointlike['position']['equ']).difference(SkyDir(*at_pulsar_pointlike['position']['equ'])))

            if type == 'extended':
                extension = extended_pointlike['spatial_model']['Sigma']
                extension_err = extended_pointlike['spatial_model']['Sigma_err']
                ext = format.error(extension, extension_err)

            elif type == 'point':
                extension_ul = point_pointlike['extension_upper_limit']['extension']
                ext = format.ul(extension_ul)

            table[psr_name].append(format.pwn(pwn))

            table[ts_point_name].append('%.1f' % ts_point)
            table[l_name].append('%.2f' % l)
            table[b_name].append('%.2f' % b)
            table[poserr_name].append(poserr)
            table[offset_name].append('%.2f' % o)
            table[ts_ext_name].append('%.1f' % ts_ext)
            table[ext_name].append(ext)
            
    deg = '(deg)'

    filebase='localization'
    if confluence:
        write_confluence(table,
                    filebase=filebase,
                    units={
                        l_name:deg,
                        b_name:deg,
                        offset_name:deg,
                        ext_name:deg,
                        poserr_name:deg,
                    })
    else:
        write_latex(table,
                    filebase=filebase,
                    units={
                        l_name:deg,
                        b_name:deg,
                        offset_name:deg,
                        ext_name:deg,
                        poserr_name:deg,
                    })



pwnlist=get_pwnlist()
localization_table(pwnlist)

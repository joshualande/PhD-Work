from table_helper import get_pwnlist,get_results,table_name,write_latex, BestHypothesis
from lande_toolbag import OrderedDefaultdict
import numpy as np
from skymaps import SkyDir

def localization_table(pwnlist):

    table = OrderedDefaultdict(list)

    psr_name='PSR'
    l_name='GLON'
    b_name='GLAT'
    ts_point_name =r'$\ts_\text{point}$'
    ts_ext_name =r'\tsext'
    offset_name = 'Offset'
    ext_name = 'Extension'
    poserr_name = 'Pos Err'

    for pwn in pwnlist:

        results = get_results(pwn)

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


        print pwn,type

        if type != 'upper_limit':

            print pwn

            l,b=pointlike['gal']

            try:
                poserr='%.2f' % pointlike['spatial_model']['lsigma']
            except:
                poserr='None'

            o = np.degrees(SkyDir(*pointlike['equ']).difference(SkyDir(*at_pulsar_pointlike['equ'])))

            if type == 'extended':
                extension = extended_pointlike['spatial_model']['Sigma']
                extension_err = extended_pointlike['spatial_model']['Sigma_err']
                ext = '$%.2f \pm %.2f$' % (extension, extension_err)

            elif type == 'point':
                extension_ul = point_pointlike['extension_upper_limit']
                ext = '$<%.2f$' % extension_ul

            table[psr_name].append(table_name(pwn))

            table[ts_point_name].append('%.1f' % ts_point)
            table[l_name].append('%.2f' % l)
            table[b_name].append('%.2f' % b)
            table[poserr_name].append(poserr)
            table[offset_name].append('%.2f' % o)
            table[ts_ext_name].append('%.1f' % ts_ext)
            table[ext_name].append(ext)
            
    deg = '(deg)'
    write_latex(table,
                filebase='localization',
                latexdict = dict(#caption=r'All Energy spectral fit for the %s LAT-detected Pulsars'  % len(pwnlist),
                                 #preamble=r'\tabletypesize{\scriptsize}',
                                 units={
                                     l_name:deg,
                                     b_name:deg,
                                     offset_name:deg,
                                     ext_name:deg,
                                     poserr:deg,
                                 }))


pwnlist=get_pwnlist()
localization_table(pwnlist)

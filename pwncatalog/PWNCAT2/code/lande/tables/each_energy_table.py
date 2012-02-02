from table_helper import get_pwnlist,get_results,table_name,write_latex, BestHypothesis
from lande_toolbag import OrderedDefaultdict

def each_energy_table(pwnlist):

    table = OrderedDefaultdict(list)

    TS1_name = r'$\ts_{0.1-1}$'
    TS2_name = r'$\ts_{1-10}$'
    TS3_name = r'$\ts_{10-316}$'

    flux1_name = '$F_{0.1-1}$'
    flux2_name = '$F_{1-10}$'
    flux3_name = '$F_{10-316}$'

    index1_name = r'$\Gamma_{0.1-1}$'
    index2_name = r'$\Gamma_{1-10}$'
    index3_name = r'$\Gamma_{10-316}$'

    for pwn in pwnlist:

        results = get_results(pwn)
        table['PSR'].append(table_name(pwn))

        if results is None: 
            table[TS1_name].append('None')
            table[flux1_name].append('None')
            table[index1_name].append('None')

            table[TS2_name].append('None')
            table[flux2_name].append('None')
            table[index2_name].append('None')

            table[TS3_name].append('None')
            table[flux3_name].append('None')
            table[index3_name].append('None')
        else:
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

            ts = gtlike['bands']['TS']

            f = gtlike['bands']['flux']
            flux = f['value']
            flux_err = f['error']
            ul = f['upper_limit']

            ts = [i if i > 0 else 0 for i in ts]

            table[TS1_name].append('%.1f' % ts[0])
            table[flux1_name].append('$%.2f \pm %.2f$' % (flux[0]/1e-9,flux_err[0]/1e-9) if ts[0] > 25 else '$<%.2f$' % (ul[0]/1e-9))
            table[index1_name].append('None')


            table[TS2_name].append('%.1f' % ts[1])
            table[flux2_name].append('$%.2f \pm %.2f$' % (flux[1]/1e-9,flux_err[1]/1e-9) if ts[1] > 25 else r'$<%.2f$' % (ul[1]/1e-9))
            table[index2_name].append('None')

            table[TS3_name].append('%.1f' % ts[2])
            table[flux3_name].append('$%.2f \pm %.2f$' % (flux[2]/1e-9,flux_err[2]/1e-9) if ts[2] > 25 else r'$<%.2f$' % (ul[2]/1e-9))
            table[index3_name].append('None')

    write_latex(table,
                filebase='off_peak_each_energy',
                latexdict = dict(#caption=r'Energy bin spectral fit for the %s LAT-detected Pulsars'  % len(pwnlist),
                                 #preamble=r'\tabletypesize{\scriptsize}',
                                 units={
                                     flux1_name:r'($10^{-9}\ \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                     flux2_name:r'($10^{-9}\ \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                     flux3_name:r'($10^{-9}\ \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                 }))

pwnlist=get_pwnlist()
each_energy_table(pwnlist)

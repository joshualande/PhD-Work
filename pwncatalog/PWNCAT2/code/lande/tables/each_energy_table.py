from table_helper import get_pwnlist,get_results,table_name,write_latex, BestHypothesis
from lande_toolbag import OrderedDefaultdict
from numpy import asarray as a

def each_energy_table(pwnlist):

    table = OrderedDefaultdict(list)

    psr_name='PSR'
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
        table[psr_name].append(table_name(pwn))

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
            print 'name',pwn

            b = BestHypothesis(results)
            gtlike = b.gtlike
            pointlike = b.pointlike
            type = b.type
            print type

            ts = gtlike['bands']['TS']
            flux = gtlike['bands']['flux']['value']
            flux_err = gtlike['bands']['flux']['error']
            ul = gtlike['bands']['flux']['upper_limit']
            index = -a(gtlike['bands']['index']['value'])
            index_err = -a(gtlike['bands']['index']['error'])

            ts = [i if i > 0 else 0 for i in ts]

            table[TS1_name].append('%.1f' % ts[0])
            if ts[0] >= 25:
                table[flux1_name].append(r'$%.2f \pm %.2f$' % (flux[0]/1e-9,flux_err[0]/1e-9))
                table[index1_name].append(r'$%.2f \pm %.2f$' % (index[0], index_err[0]))
            else:
                table[flux1_name].append('$<%.2f$' % (ul[0]/1e-9))
                table[index1_name].append(r'\nodata')


            table[TS2_name].append('%.1f' % ts[1])
            if ts[1] >= 25:
                table[flux2_name].append(r'$%.2f \pm %.2f$' % (flux[1]/1e-9,flux_err[1]/1e-9))
                table[index2_name].append(r'$%.2f \pm %.2f$' % (index[1], index_err[1]))
            else:
                table[flux2_name].append(r'$<%.2f$' % (ul[1]/1e-9))
                table[index2_name].append(r'\nodata')

            table[TS3_name].append('%.1f' % ts[2])
            if ts[2] >= 25:
                table[flux3_name].append(r'$%.2f \pm %.2f$' % (flux[2]/1e-9,flux_err[2]/1e-9))
                table[index3_name].append(r'$%.2f \pm %.2f$' % (index[2], index_err[2]))
            else:
                table[flux3_name].append(r'$<%.2f$' % (ul[2]/1e-9))
                table[index3_name].append(r'\nodata')

    print table
    write_latex(table,
                filebase='each_energy',
                latexdict = dict(#caption=r'Energy bin spectral fit for the %s LAT-detected Pulsars'  % len(pwnlist),
                                 #preamble=r'\tabletypesize{\scriptsize}',
                                 units={
                                     flux1_name:r'($10^{-9}\ \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                     flux2_name:r'($10^{-9}\ \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                     flux3_name:r'($10^{-9}\ \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                 }))

pwnlist=get_pwnlist()
each_energy_table(pwnlist)

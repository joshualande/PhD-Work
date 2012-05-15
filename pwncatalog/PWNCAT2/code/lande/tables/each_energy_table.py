from table_helper import get_pwnlist,get_results,write_latex, write_confluence, BestHypothesis
from table_helper import PWNFormatter
from lande.utilities.tools import OrderedDefaultDict
from numpy import asarray as a
from lande.utilities.table import get_confluence

confluence=get_confluence()

format=PWNFormatter(confluence=confluence, precision=2)

def each_energy_table(pwnlist):

    table = OrderedDefaultDict(list)

    psr_name='PSR'
    TS1_name = r'$\ts_{0.1-1}$' if not confluence else 'TS_(0.1-1)'
    TS2_name = r'$\ts_{1-10}$' if not confluence else 'TS_(1-10)'
    TS3_name = r'$\ts_{10-316}$' if not confluence else 'TS_(10-316)'

    flux1_name = '$F_{0.1-1}$' if not confluence else 'F_(0.1-1)'
    flux2_name = '$F_{1-10}$' if not confluence else 'F_(1-10)'
    flux3_name = '$F_{10-316}$' if not confluence else 'F_(10-316)'

    index1_name = r'$\Gamma_{0.1-1}$' if not confluence else 'Gamma_(0.1-1)'
    index2_name = r'$\Gamma_{1-10}$' if not confluence else 'Gamma_(1-10)'
    index3_name = r'$\Gamma_{10-316}$' if not confluence else 'Gamma_(10-316)'

    for pwn in pwnlist:

        results = get_results(pwn)
        table[psr_name].append(format.pwn(pwn))

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
            print pwn

            b = BestHypothesis(results)
            gtlike = b.gtlike
            pointlike = b.pointlike
            type = b.type

            ts = gtlike['bands']['TS']
            flux = gtlike['bands']['flux']['value']
            flux_err = gtlike['bands']['flux']['error']
            ul = gtlike['bands']['flux']['upper_limit']
            index = -a(gtlike['bands']['index']['value'])
            index_err = -a(gtlike['bands']['index']['error'])

            ts = [i if i > 0 else 0 for i in ts]

            table[TS1_name].append(format.value(ts[0],precision=1))
            if ts[0] >= 25:
                table[flux1_name].append(format.error(flux[0]/1e-9,flux_err[0]/1e-9))
                table[index1_name].append(format.error(index[0], index_err[0]))
            else:
                table[flux1_name].append(format.ul(ul[0]/1e-9))
                table[index1_name].append(format.nodata)


            table[TS2_name].append(format.value(ts[1],precision=1))
            if ts[1] >= 25:
                table[flux2_name].append(format.error(flux[1]/1e-9,flux_err[1]/1e-9))
                table[index2_name].append(format.error(index[1], index_err[1]))
            else:
                table[flux2_name].append(format.ul(ul[1]/1e-9))
                table[index2_name].append(format.nodata)

            table[TS3_name].append(format.value(ts[2], precision=1))
            if ts[2] >= 25:
                table[flux3_name].append(r'$%.2f \pm %.2f$' % (flux[2]/1e-9,flux_err[2]/1e-9))
                table[index3_name].append(r'$%.2f \pm %.2f$' % (index[2], index_err[2]))
            else:
                table[flux3_name].append(format.ul(ul[2]/1e-9))
                table[index3_name].append(format.nodata)

    filebase='each_energy'
    if confluence:
        write_confluence(table,
                    filebase=filebase,
                    units={
                        flux1_name:r'(10^-9 ph cm^-2 s^-1)',
                        flux2_name:r'(10^-9 ph cm^-2 s^-1)',
                        flux3_name:r'(10^-9 ph cm^-2 s^-1)',
                    })
    else:
        write_latex(table,
                    filebase=filebase,
                    preamble=r'\tabletypesize{\scriptsize}',
                    units={
                        flux1_name:r'($10^{-9}\ \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                        flux2_name:r'($10^{-9}\ \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                        flux3_name:r'($10^{-9}\ \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                    })

pwnlist=get_pwnlist()
each_energy_table(pwnlist)

from table_helper import get_pwnlist,get_results,write_latex,write_confluence,BestHypothesis
from table_helper import TableFormatter
from lande.utilities.tools import OrderedDefaultDict

confluence=True

format=TableFormatter(confluence=confluence)

def all_energy_table(pwnlist):

    table = OrderedDefaultDict(list)

    psr_name='PSR'
    flux_name=r'$F_{0.1-316}$' if not confluence else 'F_(0.1-316)'
    energy_flux_name=r'$G_{0.1-316}$' if not confluence else 'G_(0.1-316)'
    ts_name=r'\ts' if not confluence else 'TS'
    gamma_name=r'$\Gamma$' if not confluence else 'Gamma'

    luminosity_name = r'Luminosity'

    nodata = '' if confluence else r'\nodata'

    for pwn in pwnlist:
        table[psr_name].append(format.name(pwn))

        results = get_results(pwn)

        if results is None: 
            table[ts_name].append('None')
            table[flux_name].append('None')
            table[gamma_name].append('None')
            table[luminosity_name].append(r'None')
        else:

            b = BestHypothesis(results)
            gtlike = b.gtlike
            pointlike = b.pointlike
            type = b.type

            ts=max(gtlike['TS'],0)
            table[ts_name].append(format.value(ts, precision=1))

            if type == 'point' or type == 'extended':

                flux=gtlike['flux']['flux']
                flux_err=gtlike['flux']['flux_err']

                eflux=gtlike['flux']['eflux']
                eflux_err=gtlike['flux']['eflux_err']

                table[flux_name].append(format.error(flux/1e-9,flux_err/1e-9))
                table[energy_flux_name].append(format.error(eflux/1e-12,eflux_err/1e-12))

                index=-1*gtlike['model']['Index']
                index_err=-1*gtlike['model']['Index_err']
                table[gamma_name].append(format.error(index,index_err))
                table[luminosity_name].append(r'None')

            else:
                if gtlike['upper_limit'] != None:
                    ul=gtlike['upper_limit']['flux']
                    eul=gtlike['upper_limit']['eflux']
                    table[flux_name].append(format.ul(ul/1e-9))
                    table[energy_flux_name].append(format.ul(eul/1e-12))
                    table[gamma_name].append(nodata)
                    table[luminosity_name].append(r'None')
                else:
                    table[flux_name].append('None')
                    table[energy_flux_name].append('None')
                    table[gamma_name].append(r'None')
                    table[luminosity_name].append(r'None')

    filebase='all_energy'

    if confluence:
        write_confluence(table,
                    filebase=filebase,
                    units={
                        flux_name:r'(10^-9 ph cm^-2 s^-1)',
                        energy_flux_name:r'(10^-12 erg cm^-2 s^-1)',
                        luminosity_name:r'(10^33 erg s^-1)',
                    })
    else:
        write_latex(table,
                    filebase=filebase,
                    units={
                        flux_name:r'($10^{-9}\ \ph\,\cm^{-2}\,\s^{-1}$)',
                        energy_flux_name:r'($10^{-12}\ \erg\,\cm^{-2}\s^{-1}$)',
                        luminosity_name:r'($10^{33}\ \erg\,\s^{-1}$)',
                    })


pwnlist=get_pwnlist()
all_energy_table(pwnlist)

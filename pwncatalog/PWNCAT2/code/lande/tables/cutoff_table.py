from table_helper import get_pwnlist,get_results,write_confluence,write_latex
from table_helper import PWNFormatter
from lande.utilities.tools import OrderedDefaultDict
from lande.utilities.table import get_confluence

confluence=get_confluence()

format=PWNFormatter(confluence=confluence, precision=2)

def cutoff_table(pwnlist):

    table = OrderedDefaultDict(list)

    psr_name='PSR'
    flux_name = r'$F_{0.1-316}$' if not confluence else 'F_(0.1-316)'
    eflux_name = r'$G_{0.1-316}$' if not confluence else 'G_(0.1-316)'
    index_name = r'$\Gamma$' if not confluence else 'Gamma'
    cutoff_name = r'$E_\text{cutoff}$' if not confluence else 'E_cutoff'
    ts_point_name = r'$\ts_\text{point}$' if not confluence else 'TS_point'
    ts_cutoff_name = r'$\ts_\text{cutoff}$' if not confluence else 'TS_cutoff'

    for pwn in pwnlist:
        results = get_results(pwn)
        if results is None: continue

        if not results.has_key('point') or not results['point'].has_key('gtlike'):
            continue

        ts = results['point']['gtlike']['TS']

        if ts < 25:
            continue

        table[psr_name].append(format.pwn(pwn))

        cutoff=results['point']['gtlike']['test_cutoff']

        if cutoff != -1:

            ts_point = results['point']['gtlike']['TS']

            table[ts_point_name].append(format.value(ts_point,precision=1))

            ts_cutoff = max(cutoff['TS_cutoff'],0)
            table[ts_cutoff_name].append(format.value(ts_cutoff,precision=1))

            nodata = '' if confluence else r'\nodata'


            if ts_cutoff >= 16:

                flux=cutoff['flux_1']['flux']
                flux_err=cutoff['flux_1']['flux_err']

                eflux=cutoff['flux_1']['eflux']
                eflux_err=cutoff['flux_1']['eflux_err']
                index=-1*cutoff['model_1']['Index1']
                index_err=cutoff['model_1']['Index1_err']
                cutoff_energy=cutoff['model_1']['Cutoff']
                cutoff_energy_err=cutoff['model_1']['Cutoff_err']

                table[flux_name].append(format.error(flux/1e-9,flux_err/1e-9))
                table[eflux_name].append(format.error(eflux/1e-12,eflux_err/1e-12))
                table[index_name].append(format.error(index,index_err))
                table[cutoff_name].append(format.error(cutoff_energy/1000,cutoff_energy_err/1000))
            else:
                table[flux_name].append(format.nodata)
                table[eflux_name].append(format.nodata)
                table[index_name].append(format.nodata)
                table[cutoff_name].append(format.nodata)
        else:
            table[flux_name].append('None')
            table[eflux_name].append('None')
            table[index_name].append('None')
            table[cutoff_name].append('None')
            table[ts_cutoff_name].append('None')

    filebase = 'cutoff_test'

    if confluence:
        write_confluence(table,
          filebase=filebase,
          units={
              flux_name:r'(10^-9 erg cm^-2 s^-1)',
              eflux_name:r'(10^-12 erg cm^-2 s^-1)',
              cutoff_name:r'(GeV)',
          })
    else:
        write_latex(table,
                    filebase=filebase,
                    preamble=r'\tabletypesize{\tiny}',
                    units={
                        flux_name:r'($10^{-9}$\ erg\,cm$^{-2}$\,s$^{-1}$)',
                        eflux_name:r'($10^{-12}$\ erg\,cm$^{-2}$\,s$^{-1}$)',
                        cutoff_name:r'(GeV)',
                    })


pwnlist=get_pwnlist()
cutoff_table(pwnlist)



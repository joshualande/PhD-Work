from table_helper import get_pwnlist,get_results,table_name,write_latex
from lande.utilities.tools import OrderedDefaultdict

def cutoff_table(pwnlist):

    table = OrderedDefaultdict(list)

    psr_name='PSR'
    flux_name = r'$F_{0.1-316}$'
    eflux_name = r'$G_{0.1-316}$'
    index_name = r'$\Gamma$'
    cutoff_name = r'$E_\text{cutoff}$'
    ts_point_name = r'$\ts_\text{point}$'
    ts_cutoff_name = r'$\ts_\text{cutoff}$'

    for pwn in pwnlist:
        results = get_results(pwn)
        if results is None: continue

        if not results.has_key('point') or not results['point'].has_key('gtlike'):
            continue

        ts = results['point']['gtlike']['TS']

        if ts < 25:
            continue

        table[psr_name].append(table_name(pwn))

        cutoff=results['point']['gtlike']['test_cutoff']

        if cutoff != -1:

            ts_point = results['point']['gtlike']['TS']

            table[ts_point_name].append('%.1f' % ts_point)

            ts_cutoff = max(cutoff['TS_cutoff'],0)
            table[ts_cutoff_name].append('%.1f' % ts_cutoff)


            if ts_cutoff >= 16:

                flux=cutoff['flux_1']['flux']
                flux_err=cutoff['flux_1']['flux_err']

                eflux=cutoff['flux_1']['eflux']
                eflux_err=cutoff['flux_1']['eflux_err']
                index=-1*cutoff['model_1']['Index1']
                index_err=cutoff['model_1']['Index1_err']
                cutoff_energy=cutoff['model_1']['Cutoff']
                cutoff_energy_err=cutoff['model_1']['Cutoff_err']

                table[flux_name].append('$%.2f \pm %.2f$' % (flux/1e-9,flux_err/1e-9))
                table[eflux_name].append('$%.2f \pm %.2f$' % (eflux/1e-12,eflux_err/1e-12))
                table[index_name].append('$%.2f \pm %.2f$' % (index,index_err))
                table[cutoff_name].append('$%.2f \pm %.2f$' % (cutoff_energy/1000,cutoff_energy_err/1000))
            else:
                table[flux_name].append(r'\nodata')
                table[eflux_name].append(r'\nodata')
                table[index_name].append(r'\nodata')
                table[cutoff_name].append(r'\nodata')
        else:
            table[flux_name].append('None')
            table[eflux_name].append('None')
            table[index_name].append('None')
            table[cutoff_name].append('None')
            table[ts_cutoff_name].append('None')

    write_latex(table,
                filebase='cutoff_test',
                latexdict = dict(#caption=r'Spectral fitting of pulsar wind nebula candidates with low energy component.',
                                 #col_align=r'lrrrr',
                                 #preamble=r'\tabletypesize{\scriptsize}',
                                 units={
                                     flux_name:r'($10^{-9}$\ erg\,cm$^{-2}$\,s$^{-1}$)',
                                     eflux_name:r'($10^{-12}$\ erg\,cm$^{-2}$\,s$^{-1}$)',
                                     cutoff_name:r'(GeV)',
                                 }))


pwnlist=get_pwnlist()
cutoff_table(pwnlist)


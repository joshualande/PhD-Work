from table_helper import get_pwnlist,get_results,table_name,write_latex
from lande_toolbag import OrderedDefaultdict

def cutoff_table(pwnlist,looppwn):

    table = OrderedDefaultdict(list)

    flux_name = r'$G_{0.1-316}$'
    index_name = r'$\Gamma$'
    cutoff_name = r'$E_\text{cutoff}$'
    ts_cutoff_name = r'$\text{TS}_\text{cutoff}$'

    for pwn in looppwn:
        results = get_results(pwn)
        if results is None: continue

        table['PSR'].append(table_name(pwn))

        cutoff=results['at_pulsar']['gtlike']['test_cutoff']

        if cutoff != -1:

            flux=cutoff['flux_1']['eflux']
            flux_err=cutoff['flux_1']['eflux_err']
            table[flux_name].append('$%.2f \pm %.2f$' % (flux/1e-12,flux_err/1e-12))
            index=-1*cutoff['model_1']['Index1']
            index_err=cutoff['model_1']['Index1_err']
            table[index_name].append('$%.2f \pm %.2f$' % (index,index_err))
            cutoff_energy=cutoff['model_1']['Cutoff']
            cutoff_energy_err=cutoff['model_1']['Cutoff_err']
            table[cutoff_name].append('$%.2f \pm %.2f$' % (cutoff_energy/1000,cutoff_energy_err/1000))
            ts_cutoff = max(cutoff['TS_cutoff'],0)
            table[ts_cutoff_name].append('%.1f' % ts_cutoff)
        else:
            table[flux_name].append('None')
            table[index_name].append('None')
            table[cutoff_name].append('None')
            table[ts_cutoff_name].append('None')

    write_latex(table,
                filebase='off_peak_cutoff_test',
                latexdict = dict(#caption=r'Spectral fitting of pulsar wind nebula candidates with low energy component.',
                                 #col_align=r'lrrrr',
                                 #preamble=r'\tabletypesize{\scriptsize}',
                                 units={
                                     flux_name:r'($10^{-12}$\,erg\,cm$^{-2}$\,s$^{-1}$)',
                                     cutoff_name:r'(GeV)',
                                 }))


cutoff_candidates = ['PSRJ0034-0534', 
                     'PSRJ0633+1746', 
                     'PSRJ1813-1246', 
                     'PSRJ1836+5925', 
                     'PSRJ2021+4026', 
                     'PSRJ2055+2539', 
                     'PSRJ2124-3358']

pwnlist=get_pwnlist()
cutoff_table(pwnlist, looppwn=cutoff_candidates)


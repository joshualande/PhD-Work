from table_helper import get_pwnlist,get_results,table_name,write_latex
from lande_toolbag import OrderedDefaultdict

def all_energy_table(pwnlist):

    table = OrderedDefaultdict(list)

    flux_name=r'$F_{0.1-316}$'
    ts_name='TS'
    gamma_name=r'$\Gamma$'

    for pwn in pwnlist:
        table['PSR'].append(table_name(pwn))

        results = get_results(pwn)

        if results is None: 
            table[ts_name].append('None')
            table[flux_name].append('None')
            table[gamma_name].append('None')
        else:

            pl=results['at_pulsar']['pointlike']
            gt=results['at_pulsar']['gtlike']

            ts=max(gt['TS'],0)
            table[ts_name].append('%.1f' % ts)

            if ts > 25:
                flux=gt['flux']['flux']
                flux_err=gt['flux']['flux_err']
                table[flux_name].append('$%.2f \pm %.2f$' % (flux/1e-9,flux_err/1e-9) )
            else:
                if gt['upper_limit'] != -1:
                    ul=gt['upper_limit']['flux']
                    table[flux_name].append(r'$<%.2f$' % (ul/1e-9))
                else:
                    table[flux_name].append('None')


            index=-1*gt['model']['Index']
            index_err=-1*gt['model']['Index_err']

            table[gamma_name].append('$%.2f \pm %.2f$' % (index,index_err) if ts > 25 else r'\nodata')

    write_latex(table,
                filebase='off_pulse_all_energy',
                latexdict = dict(#caption=r'All Energy spectral fit for the %s LAT-detected Pulsars'  % len(pwnlist),
                                 #preamble=r'\tabletypesize{\scriptsize}',
                                 units={
                                     flux_name:r'($10^{-9} \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                 }))


pwnlist=get_pwnlist()
all_energy_table(pwnlist)

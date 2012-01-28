from table_helper import get_pwnlist,get_results,table_name,write_latex
from lande_toolbag import OrderedDefaultdict

def all_energy_table(pwnlist):

    table = OrderedDefaultdict(list)

    flux_name=r'$F_{0.1-316}$'
    energy_flux_name=r'$G_{0.1-316}$'
    ts_name=r'\ts'
    gamma_name=r'$\Gamma$'

    luminosity_name = r'Luminosity'

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

                eflux=gt['flux']['eflux']
                eflux_err=gt['flux']['eflux_err']
                table[flux_name].append('$%.2f \pm %.2f$' % (flux/1e-9,flux_err/1e-9) )
                table[energy_flux_name].append('$%.2f \pm %.2f$' % (eflux/1e-12,eflux_err/1e-12))
            else:
                if gt['upper_limit'] != -1:
                    ul=gt['upper_limit']['flux']
                    eul=gt['upper_limit']['eflux']
                    table[flux_name].append(r'$<%.2f$' % (ul/1e-9))
                    table[energy_flux_name].append(r'$<%.2f$' % (eul/1e-12))
                else:
                    table[flux_name].append('None')
                    table[energy_flux_name].append('None')


            index=-1*gt['model']['Index']
            index_err=-1*gt['model']['Index_err']

            table[gamma_name].append('$%.2f \pm %.2f$' % (index,index_err) if ts > 25 else r'\nodata')
            table[luminosity_name].append(r'None')

    write_latex(table,
                filebase='off_peak_all_energy',
                latexdict = dict(#caption=r'All Energy spectral fit for the %s LAT-detected Pulsars'  % len(pwnlist),
                                 #preamble=r'\tabletypesize{\scriptsize}',
                                 units={
                                     flux_name:r'($10^{-9}\ \ph\,\cm^{-2}\,\s^{-1}$)',
                                     energy_flux_name:r'($10^{-12}\ \erg\,\cm^{-2}\s^{-1}$)',
                                     luminosity_name:r'($10^{33}\ \erg\,\s^{-1}$)',
                                 }))


pwnlist=get_pwnlist()
all_energy_table(pwnlist)

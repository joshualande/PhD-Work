from os.path import join as j
import StringIO
import shutil
from toolbag import OrderedDefaultdict
import os.path
import tempfile

import yaml
import asciitable

fitdir='/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v45/analysis/'
savedir='/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v45/'

def write_latex(table, filename, **kwargs):

    outtable=StringIO.StringIO()

    asciitable.write(table, outtable, 
                     Writer=asciitable.AASTex,
                     names=table.keys(),
                     **kwargs
                    )
    t=outtable.getvalue()

    print t
    file=r"""
    \documentclass{aastex}
    \usepackage{amsmath}
    \begin{document}
    %s
    \end{document}
    """ % t

    cwd=os.getcwd()
    tempdir=tempfile.mkdtemp()
    os.chdir(tempdir)
    open('table.tex','w').write(file)

    os.system('pdflatex table.tex')

    os.chdir(cwd)
    shutil.copy('%s/table.pdf' % tempdir,
                filename)


def get_results(pwn):
    f = j(fitdir,pwn,'results_%s.yaml' % pwn)
    if not os.path.exists(f): return None
    results = yaml.load(open(f))

    if not results.has_key('at_pulsar') or not results['at_pulsar'].has_key('gtlike'):
        return None
    return results

def get_sed(pwn,binning,hypothesis):
    filename=j(fitdir,pwn,'seds','sed_gtlike_%s_%s_%s.yaml' % (binning, hypothesis, pwn))
    return yaml.load(open(filename))

def all_energy_table(pwnlist):


    table = OrderedDefaultdict(list)

    flux_name=r'$F_{0.1-316}$'
    gamma_name=r'$\Gamma$'

    for pwn in pwnlist:
        print pwn,j(fitdir,pwn,'results_%s.yaml' % pwn)

        results = get_results(pwn)
        if results is None: continue

        pl=results['at_pulsar']['pointlike']
        gt=results['at_pulsar']['gtlike']

        table['PSR'].append(pwn.replace('PSR',''))
        ts=max(gt['TS'],0)
        table['TS'].append('%.1f' % ts)

        if ts > 25:
            flux=gt['flux']['flux']
            flux_err=gt['flux']['flux_err']
            table[flux_name].append('$%.2f \pm %.2f$' % (flux/1e-9,flux_err/1e-9) )
        else:
            ul=gt['upper_limit']['flux']
            table[flux_name].append('$<%.2f$' % (ul/1e-9))


        index=-1*gt['model']['Index']
        index_err=-1*gt['model']['Index_err']

        table[gamma_name].append('$%.2f \pm %.2f$' % (index,index_err) if ts > 25 else r'\nodata')

    write_latex(table,
                filename='%s/all_energy_table.pdf' % savedir,
                latexdict = dict(caption=r'All Energy spectral fit for the %s LAT-detected Pulsars'  % len(pwnlist),
                                 preamble=r'\tabletypesize{\scriptsize}',
                                 units={
                                     flux_name:r'($10^{-9} \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                 }))

def each_energy_table(pwnlist):

    table = OrderedDefaultdict(list)

    TS1_name = '$TS_{0.1-1}$'
    TS2_name = '$TS_{1-10}$'
    TS3_name = '$TS_{10-316}$'

    flux1_name = '$F_{0.1-1}$'
    flux2_name = '$F_{1-10}$'
    flux3_name = '$F_{10-316}$'

    for pwn in pwnlist:

        results = get_results(pwn)
        if results is None: continue

        sed = get_sed(pwn,'1bpd','at_pulsar')
        ts = sed['Test_Statistic']
        flux = sed['Ph_Flux']['Value']
        flux_err = sed['Ph_Flux']['Error']
        ul = sed['Ph_Flux']['Upper_Limit']

        table['PSR'].append(pwn.replace('PSR',''))

        table[TS1_name].append('%.1f' % ts[0])
        table[flux1_name].append('$%.2f \pm %.2f$' % (flux[0]/1e-9,flux_err[0]/1e-9) if ts[0] > 25 else '$<%.2f$' % (ul[0]/1e-9))

        table[TS2_name].append('%.1f' % ts[1])
        table[flux2_name].append('$%.2f \pm %.2f$' % (flux[1]/1e-9,flux_err[1]/1e-9) if ts[1] > 25 else '$<%.2f$' % (ul[1]/1e-9))

        table[TS3_name].append('%.1f' % ts[2])
        table[flux3_name].append('$%.2f \pm %.2f$' % (flux[2]/1e-9,flux_err[2]/1e-9) if ts[2] > 25 else '$<%.2f$' % (ul[2]/1e-9))

    write_latex(table,
                filename='%s/each_energy_table.pdf' % savedir,
                latexdict = dict(caption=r'Energy bin spectral fit for the %s LAT-detected Pulsars'  % len(pwnlist),
                                 preamble=r'\tabletypesize{\scriptsize}',
                                 units={
                                     flux1_name:r'($10^{-9} \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                     flux2_name:r'($10^{-9} \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                     flux3_name:r'($10^{-9} \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                 }))

def cutoff_table(pwnlist,looppwn):

    table = OrderedDefaultdict(list)

    flux_name = r'$G_{0.1-316}$'
    index_name = r'$\Gamma$'
    cutoff_name = r'$E_\text{cutoff}$'
    ts_cutoff_name = r'$\text{TS}_\text{cutoff}$'

    for pwn in looppwn:
        results = get_results(pwn)
        if results is None: continue

        table['PWN'].append(pwn)


        cutoff=results['at_pulsar']['gtlike']['test_cutoff']

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

    write_latex(table,
                filename='%s/test_cutoff.pdf' % savedir,
                latexdict = dict(caption=r'Spectral fitting of pulsar wind nebula candidates with low energy component.',
                                 col_align=r'lrrrr',
                                 preamble=r'\tabletypesize{\scriptsize}',
                                 units={
                                     flux_name:r'($10^{-12}$\,erg\,cm$^{-2}$\,s$^{-1}$)',
                                     cutoff_name:r'(GeV)',
                                 }))


pwnlist=sorted(yaml.load(open('pwndata/pwncat1_data.yaml')).keys())
all_energy_table(pwnlist)
each_energy_table(pwnlist)
cutoff_table(pwnlist, looppwn=['PSRJ0034-0534', 'PSRJ0633+1746', 'PSRJ1813-1246', 'PSRJ1836+5925', 'PSRJ2021+4026', 'PSRJ2055+2539', 'PSRJ2124-3358'])


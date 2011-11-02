from os.path import join as j
import StringIO
import shutil
from toolbag import OrderedDefaultdict
import os.path
import tempfile

import yaml
import asciitable


def write_latex(table, filename, **kwargs):

    outtable=StringIO.StringIO()

    asciitable.write(table, outtable, 
                     Writer=asciitable.AASTex,
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


def all_energy_table(pwnlist):


    table = OrderedDefaultdict(list)

    flux_name=r'$F_{0.1-316}$'
    gamma_name=r'$\Gamma$'

    for pwn in pwnlist:

        f = j(fitdir,pwn,'results_%s.yaml' % pwn)
        if not os.path.exists(f): continue
        results = yaml.load(open(f))

        if not results.has_key('at_pulsar') or not results['at_pulsar'].has_key('gtlike'):
            continue


        pl=results['at_pulsar']['pointlike']
        gt=results['at_pulsar']['gtlike']

        table['PSR'].append(pwn.replace('PSR',''))
        ts=max(gt['TS'],0)
        table['TS'].append('%.1f' % ts)

        flux=gt['flux']['flux']
        flux_err=gt['flux_err']
        ul=gt['upper_limit']['flux']


        table[flux_name].append(
            '$%.2f \pm %.2f$' % (flux/1e-9,flux_err/1e-9) if ts > 25 else '$<%.2f$' % (ul/1e-9))

        index=gt['model']['Index']
        index_err=gt['model']['Index_err']

        table[gamma_name].append('$%.2f \pm %.2f$' % (index,index_err) if ts > 25 else r'\nodata')

    write_latex(table,
                filename='%s/all_energy_table.pdf' % savedir,
                names=table.keys(),
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

        f = j(fitdir,pwn,'results_%s.yaml' % pwn)
        if not os.path.exists(f): continue
        results = yaml.load(open(f))

        if not results.has_key('at_pulsar') or not results['at_pulsar'].has_key('gtlike'):
            continue

        sed = results['at_pulsar']['gtlike']['sed']['1bpd_at_pulsar']
        ts = sed['Test_Statistic']
        flux = sed['Raw_Flux']
        flux_err = sed['Raw_Flux_Err']
        ul = sed['Flux_UL']

        table['PSR'].append(pwn.replace('PSR',''))

        table[TS1_name].append('%.1f' % ts[0])
        table[flux1_name].append('$%.2f \pm %.2f$' % (flux[0]/1e-9,flux_err[0]/1e-9) if ts[0] > 25 else '$<%.2f$' % (ul[0]/1e-9))

        table[TS2_name].append('%.1f' % ts[1])
        table[flux2_name].append('$%.2f \pm %.2f$' % (flux[1]/1e-9,flux_err[1]/1e-9) if ts[1] > 25 else '$<%.2f$' % (ul[1]/1e-9))

        table[TS3_name].append('%.1f' % ts[2])
        table[flux3_name].append('$%.2f \pm %.2f$' % (flux[2]/1e-9,flux_err[2]/1e-9) if ts[2] > 25 else '$<%.2f$' % (ul[2]/1e-9))

    write_latex(table,
                filename='%s/each_energy_table.pdf' % savedir,
                names=table.keys(),
                latexdict = dict(caption=r'Energy bin spectral fit for the %s LAT-detected Pulsars'  % len(pwnlist),
                                 preamble=r'\tabletypesize{\scriptsize}',
                                 units={
                                     flux1_name:r'($10^{-9} \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                     flux2_name:r'($10^{-9} \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                     flux3_name:r'($10^{-9} \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                 }))

fitdir='/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v21/fits/'
savedir='/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v21/'

pwnlist=sorted(yaml.load(open('pwndata/pwncat1_data.yaml')).keys())
all_energy_table(pwnlist)
each_energy_table(pwnlist)

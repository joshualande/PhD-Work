from os.path import join as j
import StringIO
from textwrap import dedent
import shutil
from lande_toolbag import OrderedDefaultdict
import os.path
import tempfile

import yaml
import asciitable

base='/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v7/'

fitdir=j(base,'analysis_no_plots/')
savedir=j(base,'tables')

if not os.path.exists(savedir): os.makedirs(savedir)

def table_name(pwn):
    pwn = pwn.replace('PSR','')
    pwn = pwn.replace('-','$-$')
    return pwn

def write_latex(table, filebase, **kwargs):

    outtable=StringIO.StringIO()

    asciitable.write(table, outtable, 
                     Writer=asciitable.AASTex,
                     names=table.keys(),
                     **kwargs
                    )
    t=outtable.getvalue()

    lines = t.split('\n')
    if lines[-1] == '': 
        lines=lines[0:-1]

    header = lines[0]
    footer= lines[-1]

    t = '\n'.join(lines[1:-1])


    os.chdir(savedir)

    open('%s.tex' % filebase,'w').write(t)

    open('temp.tex','w').write(dedent(r"""
        \documentclass{aastex}
        \usepackage{amsmath}
        \begin{document}
        %s
        \input{%s}
        %s
        \end{document}""" % (header,filebase,footer)))

    os.system('pdflatex temp.tex')
    shutil.move('temp.pdf','%s.pdf' % filebase)

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
    ts_name='TS'
    gamma_name=r'$\Gamma$'

    for pwn in pwnlist:
        print pwn,j(fitdir,pwn,'results_%s.yaml' % pwn)

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


pwnlist=sorted(yaml.load(open('../../pwndata/pwncat2_data_lande.yaml')).keys())
all_energy_table(pwnlist)

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
                filebase='off_pulse_cutoff_test',
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

pwnlist=sorted(yaml.load(open('../../pwndata/pwncat2_data_lande.yaml')).keys())
cutoff_table(pwnlist, looppwn=cutoff_candidates)


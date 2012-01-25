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
        table['PSR'].append(table_name(pwn))

        if results is None or get_sed(pwn,'1bpd','at_pulsar') == {}: 
            table[TS1_name].append('None')
            table[flux1_name].append('None')

            table[TS2_name].append('None')
            table[flux2_name].append('None')

            table[TS3_name].append('None')
            table[flux3_name].append('None')
        else:

            sed = get_sed(pwn,'1bpd','at_pulsar')
            ts = sed['Test_Statistic']
            flux = sed['Ph_Flux']['Value']
            flux_err = sed['Ph_Flux']['Error']
            ul = sed['Ph_Flux']['Upper_Limit']

            ts = [i if i > 0 else 0 for i in ts]

            table[TS1_name].append('%.1f' % ts[0])
            table[flux1_name].append('$%.2f \pm %.2f$' % (flux[0]/1e-9,flux_err[0]/1e-9) if ts[0] > 25 else '$<%.2f$' % (ul[0]/1e-9))

            table[TS2_name].append('%.1f' % ts[1])
            table[flux2_name].append('$%.2f \pm %.2f$' % (flux[1]/1e-9,flux_err[1]/1e-9) if ts[1] > 25 else r'$<%.2f$' % (ul[1]/1e-9))

            table[TS3_name].append('%.1f' % ts[2])
            table[flux3_name].append('$%.2f \pm %.2f$' % (flux[2]/1e-9,flux_err[2]/1e-9) if ts[2] > 25 else r'$<%.2f$' % (ul[2]/1e-9))

    write_latex(table,
                filebase='off_pulse_each_energy',
                latexdict = dict(#caption=r'Energy bin spectral fit for the %s LAT-detected Pulsars'  % len(pwnlist),
                                 #preamble=r'\tabletypesize{\scriptsize}',
                                 units={
                                     flux1_name:r'($10^{-9} \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                     flux2_name:r'($10^{-9} \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                     flux3_name:r'($10^{-9} \text{ph}\,\text{cm}^{-2}\,\text{s}^{-1}$)',
                                 }))


pwnlist=sorted(yaml.load(open('../../pwndata/pwncat2_data_lande.yaml')).keys())
all_energy_table(pwnlist)
each_energy_table(pwnlist)

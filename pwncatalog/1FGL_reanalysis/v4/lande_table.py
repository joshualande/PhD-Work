from os.path import join as j
import StringIO
from toolbag import OrderedDefaultdict
import os.path
import yaml
import asciitable

allpwn=yaml.load(open('pwndata/pwndata_v1.yaml'))
all_results='/nfs/slac/g/ki/ki03/lande/pwncatalog/1FGL_reanalysis/v4/analyze_v1'

table = OrderedDefaultdict(list)

for pwn in allpwn.keys():

    f = j(all_results,pwn,'results_%s.yaml' % pwn)
    if not os.path.exists(f): continue
    results = yaml.load(open(f))

    pl=results['at_pulsar']['pointlike']

    table['PSR'].append(pwn)
    ts=max(pl['TS'],0)
    table['TS'].append('%.1f' % ts)

    flux=pl['flux']
    flux_err=pl['flux_err']
    ul=pl['upper_limit']

    flux_name=r'F_{0.1-100}'

    table[flux_name].append(
        '%.1e \pm %.1e' % (flux,flux_err) if ts > 25 else '<%.1e' % ul)

    index=pl['Index']
    index_err=pl['Index_err']


    gamma_name=r'$\Gamma'
    table[gamma_name].append('%.1f \pm %.1f' % (index,index_err) if ts > 25 else r'\nodata')


outtable=StringIO.StringIO()

asciitable.write(table, outtable, 
                 Writer=asciitable.AASTex,
                 names=['PSR',flux_name,gamma_name],
                 latexdict = dict(caption=r'Results of hte maximum likelihood\ldots',
                                  units={
                                      flux_name:'ph cm^-2 s',
                                      }))
t=outtable.getvalue()



file=r"""
\documentclass[12pt]{aastex}
\begin{document}
%s
\end{document}
""" % t

print file

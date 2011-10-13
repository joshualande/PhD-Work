print 'run'
from os.path import join as j
import StringIO
from toolbag import OrderedDefaultdict
import os.path
import yaml
import asciitable

allpwn=yaml.load(open('pwndata/pwndata_v1.yaml'))
all_results='/nfs/slac/g/ki/ki03/lande/pwncatalog/1FGL_reanalysis/v4/analyze_v1'

print 'xxx'
table = OrderedDefaultdict(list)

for pwn in allpwn.keys():

    f = j(all_results,pwn,'results_%s.yaml' % pwn)
    if not os.path.exists(f): continue
    results = yaml.load(open(f))

    table['PSR'].append(pwn)
    ts=max(results['at_pulsar']['pointlike']['TS'],0)
    table['TS'].append('%.1f' % ts)

    flux=results['at_pulsar']['pointlike']['flux']
    flux_err=results['at_pulsar']['pointlike']['flux_err']
    ul=results['at_pulsar']['pointlike']['upper limit']

    table[r'F_{0.1-100}\\(10^-9ph)'].append(
        '%.1e \pm %.1e' % (flux,flux_err) if ts > 25 else '%.1e' % ul)

outtable=StringIO.StringIO()

#print table
#asciitable.write(table, outtable, Writer=asciitable.FixedWidth, names=table.keys())

asciitable.write(table, outtable, Writer=asciitable.AASTex,names=table.keys(),
                 latexdict = {'caption': r'Results of hte maximum likelihood\ldots'})

t=outtable.getvalue()



file=r"""
\documentclass[12pt]{aastex}
\begin{document}
%s
\end{document}
""" % t

print file

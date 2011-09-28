import asciitable
import sys
import yaml
import re
from os.path import join,exists
from collections import defaultdict

snrdata=yaml.load(open('snrdata.yaml'))

snrs=snrdata.keys()
snrs.sort(key=lambda x: float(re.split('[G+-]',x)[1]))

base='/nfs/slac/g/ki/ki03/lande/green_catalog/2FGL/v2/analyze_v1/'

table=defaultdict(list)


for snr in snrs:
    file=join(base,snr,'results_%s.yaml' % snr)
    if exists(file):
        results=yaml.load(open(file))

        ts=results['postlocalize_gtlike']['ts']
        if ts < 0: ts=0
        significant = ts>25

        if not significant: continue

        nickname=snrdata[snr]['nickname']
        table['Nickname'].append(nickname if nickname is not None else '')

        table['TS'].append('%.1f' % ts)



        flux=results['postlocalize_gtlike']['flux']
        flux_err=results['postlocalize_gtlike']['flux_err']

        ul=results['upper_limit_gtlike']

        index=-1*results['postlocalize_gtlike']['Index']

        table['Flux'].append('%.2e +/- %.2e' % (flux,flux_err) 
                             if significant else 
                             '<%.2e' % ul)
        table['Index'].append('%.2f' % index if significant else ' ')
        #table['Index'].append(index)
        table['SNR'].append(snr)

names=['SNR','TS','Flux','Index', 'Nickname']

asciitable.write(table, sys.stdout, 
                 delimiter='|', 
                 names=names,
                )

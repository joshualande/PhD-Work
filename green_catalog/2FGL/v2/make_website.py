import asciitable
import sys
import yaml
import re
import os
from os.path import join,exists
from collections import defaultdict

base='/nfs/slac/g/ki/ki03/lande/green_catalog/2FGL/v2/analyze_v3/'

snrdata=yaml.load(open('snrdata.yaml'))

snrs=snrdata.keys()
snrs.sort(key=lambda x: float(re.split('[G+-]',x)[1]))

all_results = dict()
for snr in snrs:
    file=join(base,'fits',snr,'results_%s.yaml' % snr)
    if exists(file):
        all_results[snr]=yaml.load(open(file))

website=join(base,'website')

if not os.path.exists(website):
    os.makedirs(website)


index_t2t = []



def t2t(lines,name): 
    """ create the HTML for a given t2t file. """
    filename = join(website,'%s.t2t' % name)
    
    temp=open(filename,'w')
    temp.write(
        '\n'.join(lines))
    temp.close()
        
    os.system('txt2tags --target html --style color.css --css-sugar %s' % filename)

def format_table(only_significant=False):
    index_t2t.append('')

    table=defaultdict(list)

    format = '| %30s | %30s | %30s | %30s | %30s | %30s |' 

    index_t2t.append(
        format % ('Name','TS','TS_ext','Flux','Index','Nickname')
        )

    for snr in snrs:
        if all_results.has_key(snr):
            results=all_results[snr]

            ts=results['postlocalize_gtlike']['ts']
            if ts < 0: ts=0

            significant = results['status'] != 'insignificant'

            table_ts_ext = '%.1f' % results['ts_ext'] if significant else ''
            

            if only_significant and not significant: continue

            nickname=snrdata[snr]['nickname']
            table_nickname=nickname if nickname is not None else '-'

            table_ts = '%.1f' % ts

            flux=results['postlocalize_gtlike']['flux']
            flux_err=results['postlocalize_gtlike']['flux_err']

            ul=results['upper_limit_gtlike']

            index=-1*results['postlocalize_gtlike']['Index']

            table_flux = '%.2e +/- %.2e' % (flux,flux_err) if significant else '<%.2e' % ul

            table_index = '%.2f' % index if significant else '-'
            table_name = '[%s %s.html]' % (snr,snr)

            index_t2t.append(format % (table_name,table_ts,table_ts_ext,table_flux,table_index,table_nickname))
        elif not only_significant:
            index_t2t.append(format % (snr,'','','','',''))

    index_t2t.append('')
            
index_t2t.append('Green Catalog E>10 GeV')
index_t2t.append('')


index_t2t.append('h2. Significant Detections')

format_table(only_significant=True)

index_t2t.append('h2. All Detections')

format_table(only_significant=False)




t2t(index_t2t, 'index')



def individiual_website(snr):
    snr_t2t = [
        '%s' % snr,
        '',
        '',
    ]

    if all_results.has_key(snr):
        results = all_results[snr]
        snr_t2t += [
            ' * nickname = %s' % snrdata[snr]['nickname'],
            ' * other stuff...',
            '',
        ]

        if results['status'] == 'insignificant':
            when = 'prelocalize'
        else:
            when = 'postlocalize'

        for when in ['postlocalize','prelocalize']:
            snr_t2t += [
                '',
                '== %s ==' % when,
                '',
                '| [../fits/%s/sources_%s_kernel_0.1_%s.png]' % (snr,when,snr)+
                '| [../fits/%s/tsmap_source_%s_%s.png]' % (snr,when,snr) +
                '| [../fits/%s/source_%s_kernel_0.1_%s.png]' % (snr,when,snr)+
                ' |',
                '',
            ]

        file=join(base,'fits',snr,'results_%s.yaml' % snr)
        snr_t2t += [
            '```',
            open(file).read(),
            '```'
        ]

        for when in ['postlocalize','prelocalize']:
            snr_t2t += [
                '',
                '== %s ==' % when,
                '',
                '| [../fits/%s/sources_%s_kernel_0.25_%s.png]' % (snr,when,snr)+
                '| [../fits/%s/tsmap_residual_%s_%s.png]' % (snr,when,snr) +
                '| [../fits/%s/source_%s_kernel_0.25_%s.png]' % (snr,when,snr)+
                ' |',
                '',
            ]



        t2t(snr_t2t, snr)


for snr in snrs:
    individiual_website(snr)

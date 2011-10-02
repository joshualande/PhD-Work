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

class Results(object):
    """ Simple object to load in the yaml file and slice/dice it. """
    def __init__(self,snr):
        self.results = results = all_results[snr]

        extended = results['extended']['gtlike']
        point=results['point']['gtlike']
        radio=results['radio_template']['gtlike']

        self.ts=point['ts']
        if self.ts < 0: self.ts=0

        self.significant = self.ts >= 25
        self.candidate = self.ts >= 9 and self.ts < 25

        self.ts_ext = extended['ts_ext']
        if self.ts_ext < 0: self.ts_ext = 0

        self.nickname=snrdata[snr]['nickname']

        if self.ts_ext > 16:
            self.flux = extended['flux']
            self.flux_err = extended['flux_err']

            self.index=-1*extended['Index']
        else:
            self.flux=point['flux']
            self.flux_err=point['flux_err']

            self.index=-1*point['Index']

        self.ul=radio['upper_limit']

        if self.ts > 25 and self.ts_ext > 16:
            self.category = 'extended'
        elif self.ts > 25:
            self.category = 'point'
        else:
            self.category = 'radio_template'


def format_table(only_significant=False, only_candidates=False):
    index_t2t.append('')

    table=defaultdict(list)

    format = '| %30s | %30s | %30s | %30s | %30s | %30s |' 

    index_t2t.append(
        format % ('Name','TS_point','TS_ext','Flux','Index','Nickname')
        )

    for snr in snrs:
        if all_results.has_key(snr):

            r = Results(snr)
            
            if only_significant and not r.significant: continue
            if only_candidates and not r.candidate: continue

            table_ts_ext = '%.1f' % r.ts_ext if r.significant or r.candidate else ''
            

            table_nickname=r.nickname if r.nickname is not None else '-'

            table_ts = '%.1f' % r.ts


            table_flux = '%.2e +/- %.2e' % (r.flux,r.flux_err) if r.significant else '<%.2e' % r.ul

            table_index = '%.2f' % r.index if r.significant else '-'
            table_name = '[%s %s.html]' % (snr,snr)

            index_t2t.append(format % (table_name,table_ts,table_ts_ext,table_flux,table_index,table_nickname))
        elif not only_significant and not only_candidates:
            index_t2t.append(format % (snr,'','','','',''))

    index_t2t.append('')
            
index_t2t.append('Green Catalog E>10 GeV')
index_t2t.append('')


index_t2t.append('h2. Significant Detections')

format_table(only_significant=True)

index_t2t.append('h2. Not Significant Candidates')

format_table(only_candidates=True)

index_t2t.append('h2. All Detections')

format_table(only_significant=False)

t2t(index_t2t, 'index')


def t2t_table(*args):
    for a in args:
        return '| ' + ' | '.join(a) + ' |'


def individiual_website(snr):

    if not all_results.has_key(snr): 
        return

    r = Results(snr)

    snr_t2t = [
        '%s' % snr,
        '',
        '',
    ]

    snr_t2t += [
        ' - nickname = %s' % r.nickname,
        ' - Category: %s' % r.category,
        ' - ts_point = %.1f' % r.ts,
        ' - ts_ext = %.1f' % r.ts_ext,
    ]

    snr_t2t += [
        '',
        '',
        '== %s ==' % r.category,
        '',
        t2t_table([
        '[../fits/%s/sources_%s_kernel_0.1_%s.png]' % (snr,r.category,snr),
        '[../fits/%s/tsmap_source_%s_%s.png]' % (snr,r.category,snr),
        '[../fits/%s/source_%s_kernel_0.1_%s.png]' % (snr,r.category,snr)
        ]),
        '',
        ]

    file=join(base,'fits',snr,'results_%s.yaml' % snr)
    snr_t2t += [
        '```',
        open(file).read(),
        '```'
    ]

    for category in ['radio_template','point','extended']:
        snr_t2t += [
            '',
            '== %s ==' % category,
            '',
            t2t_table([
                '[../fits/%s/sources_%s_kernel_0.1_%s.png]' % (snr,category,snr),
                '[../fits/%s/tsmap_source_%s_%s.png]' % (snr,category,snr),
                '[../fits/%s/source_%s_kernel_0.1_%s.png]' % (snr,category,snr),
                '[../fits/%s/sources_%s_kernel_0.25_%s.png]' % (snr,category,snr),
                '[../fits/%s/tsmap_residual_%s_%s.png]' % (snr,category,snr),
                '[../fits/%s/source_%s_kernel_0.25_%s.png]' % (snr,category,snr),
            ]),
            '',
        ]



        t2t(snr_t2t, snr)


for snr in snrs:
    individiual_website(snr)

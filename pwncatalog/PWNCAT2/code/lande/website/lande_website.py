import sys
from skymaps import SkyDir
import numpy as np
from glob import glob
import yaml
from StringIO import StringIO
import re
import os
from os.path import join,exists,expandvars
from collections import defaultdict

import asciitable

from lande_toolbag import OrderedDefaultdict

base=expandvars('$pwndata/spectral/v8')


analysis='analysis_plots'
pwnlist=sorted([os.path.basename(i) for i in glob(join(base,analysis,'*')) if os.path.isdir(i)])

website=join(base,'website')

if not os.path.exists(website): os.makedirs(website)



def get_results(pwn):
    f = join(base,analysis.replace('plots','no_plots'),pwn,'results_%s.yaml' % pwn)

    if not os.path.exists(f): return None
    results = yaml.load(open(f))

    for hypothesis in ['at_pulsar', 'point', 'extended']:
        if not results.has_key(hypothesis):
            results[hypothesis]=defaultdict(lambda:-1)
        for t in ['gtlike','pointlike']:
            h=results[hypothesis]
            if not h.has_key(t):
                h[t]=defaultdict(lambda:-1)
            for i in ['model', 'upper_limit', 'flux']:
                if not h[t].has_key(i):
                    h[t][i]=defaultdict(lambda:-1)
    return results

def get_sed(pwn,binning,hypothesis):
    filename=join(base,analysis.replace('plots','no_plots'),pwn,'seds','sed_gtlike_%s_%s_%s.yaml' % (binning, hypothesis, pwn))
    if os.path.exists(filename) and yaml.load(open(filename)) != {}:
        return yaml.load(open(filename))
    elif binning == '1bpd':
        d=defaultdict(lambda: defaultdict(lambda:[-1,-1,-1]))
        d['Test_Statistic']=[-1,-1,-1]
        return d
    else:
        raise Exception("...")



def t2t(lines,name): 
    """ create the HTML for a given t2t file. """
    filename = join(website,'%s.t2t' % name)
    
    temp=open(filename,'w')
    temp.write(
        '\n'.join(lines))
    temp.close()
        
    os.system('txt2tags --target html --style color.css --css-sugar %s' % filename)


class TableFormatter(object):

    def __init__(self, pwnlist):

        table = OrderedDefaultdict(list)

        flux_name=r'F(0.1-316)'
        gamma_name=r'Gamma'

        for pwn in pwnlist:
            print pwn

            results = get_results(pwn)
            if results is None: continue

            table['PSR'].append('[%s %s.html]' % (pwn,pwn))

            gt_at_pulsar=results['at_pulsar']['gtlike']
            gt_point=results['point']['gtlike']
            gt_extended=results['extended']['gtlike']

            pt_at_pulsar=results['at_pulsar']['pointlike']
            pt_point=results['point']['pointlike']
            pt_extended=results['extended']['pointlike']


            ts_at_pulsar=max(gt_at_pulsar['TS'],0)
            ts_point=max(gt_point['TS'],0)
            ts_ext=max(gt_extended['ts_ext'],0)

            if ts_point > 25:
                # source is significant
                if ts_ext > 16:
                    type = 'extended'
                    self.hypothesis = 'extended'
                    gt=gt_extended
                else:
                    type = 'point'
                    self.hypothesis = 'point'
                    gt=gt_point
            else:
                type = 'ul'
                self.hypothesis = 'at_pulsar'
                gt=gt_at_pulsar


            if type == 'point':
                displacement = '%.2f' % np.degrees(SkyDir(*pt_point['equ']).difference(SkyDir(*pt_at_pulsar['equ'])))
            elif type == 'extended':
                displacement = '%.2f' % np.degrees(SkyDir(*pt_extended['equ']).difference(SkyDir(*pt_at_pulsar['equ'])))
            elif type == 'ul':
                displacement = '-'
                
            ts_loc=ts_point-ts_at_pulsar
            

            if ts_point > 25:
                flux=gt['flux']['flux']
                flux_err=gt['flux']['flux_err']
            else:
                try:
                    ul=gt['upper_limit']['flux']
                except:
                    ul=-1

            if type != 'ul':

                index=-1*gt['model']['Index']
                index_err=-1*gt['model']['Index_err']


            sed = get_sed(pwn,'1bpd','at_pulsar')
            bandts = map(lambda x: max(x,0), sed['Test_Statistic'])
            bandflux = sed['Ph_Flux']['Value']
            bandflux_err = sed['Ph_Flux']['Error']
            bandul = sed['Ph_Flux']['Upper_Limit']


            table['TS_at_pulsar'].append('%.1f' % ts_at_pulsar)
            table['TS_loc'].append('%.1f' % (ts_loc))
            table['TS_ext'].append('%.1f' % ts_ext)
            table['disp'].append(displacement)

            table[flux_name].append('%.1f +/- %.1f' % (flux/1e-9,flux_err/1e-9) if ts_point>=25 else '<%.1f' % (ul/1e-9))

            table[gamma_name].append('%.1f +/- %.1f' % (index,index_err) if ts_point>=25 else '-')

            table['TS(.1-1)'].append('%.1f' % bandts[0])
            table['Flux(.1-1)'].append('%.1f +/- %.1f' % (bandflux[0]/1e-9,bandflux_err[0]/1e-9) if bandts[0] > 25 else '<%.1f' % (bandul[0]/1e-9))

            table['TS(1-10)'].append('%.1f' % bandts[1])
            table['Flux(1-10)'].append('%.1f +/- %.1f' % (bandflux[1]/1e-9,bandflux_err[1]/1e-9) if bandts[1] > 25 else '<%.1f' % (bandul[1]/1e-9))

            table['TS(10-316)'].append('%.1f' % bandts[2])
            table['Flux(10-316)'].append('%.1f +/- %.1f' % (bandflux[2]/1e-9,bandflux_err[2]/1e-9) if bandts[2] > 25 else '<%.1f' % (bandul[2]/1e-9))

        self.table = table

    def __str__(self):
        return self.get_t2t_table(self.table)

    @staticmethod
    def get_t2t_table(table, **kwargs):

        outtable=StringIO()

        asciitable.write(table, outtable, 
                         Writer=asciitable.FixedWidth,
                         names=table.keys(),
                         **kwargs
                        )
        t=outtable.getvalue()

        # this is required by t2t for tables
        # see for exmaple: http://txt2tags.org/markup.html
        t='||' + t[2:]
        return t

def build_main_website():

    index_t2t = []
    index_t2t.append('PWNCatalog+\n\n')
    t=TableFormatter(pwnlist)
    index_t2t.append(str(t))
    t2t(index_t2t, 'index')

def build_each_page(pwn):
    results = get_results(pwn)
    if results is None: return

    index_t2t = []
    index_t2t.append(pwn+'\n\n')
    t=TableFormatter([pwn])
    index_t2t.append(str(t))
    index_t2t.append('')
    index_t2t.append('[Analysis Folder ../%s/%s]' % (analysis,pwn))
    index_t2t.append('')
    index_t2t.append('[log ../%s/%s/log_%s.txt]' % (analysis,pwn,pwn))

    hypothesis=t.hypothesis

    get_img_table = lambda *args: index_t2t.append('|| ' + ' | '.join(['[../%s/%s/%s]' % (analysis,pwn,i) for i in args]) + ' |\n\n')

    title = lambda i: index_t2t.append('== %s ==' % i)

    title('Phase Info')
    get_img_table(
        'plots/phaseogram_%s.png' % (pwn), 
        'plots/phase_vs_time_%s.png' % (pwn))
            
    title('TS Maps')
    get_img_table(
        'plots/tsmap_source_%s_%s.png' % (hypothesis,pwn),
        'plots/tsmap_residual_%s_%s.png' % (hypothesis,pwn))

    title('Smoothed Counts (0.1)')
    get_img_table(
        'plots/source_0.1_%s_%s.png' % (hypothesis,pwn),
        'plots/sources_0.1_%s_%s.png' % (hypothesis,pwn))

    title('Counts (0.1)')
    get_img_table(
        'plots/counts_residual_0.1_%s_%s.png' % (hypothesis,pwn),
        'plots/counts_source_0.1_%s_%s.png' % (hypothesis,pwn))

    title('Band TS Maps')
    get_img_table(
        'plots/band_tsmap_source_%s_%s.png' % (hypothesis,pwn),
        'plots/band_tsmap_residual_%s_%s.png' % (hypothesis,pwn))


    title('Band Smoothed Counts (0.1)')
    get_img_table(
        'plots/band_source_0.1_%s_%s.png' % (hypothesis,pwn),
        'plots/band_sources_0.1_%s_%s.png' % (hypothesis,pwn))

    get_img_table(
        'seds/sed_gtlike_4bpd_%s_%s.png' % (hypothesis,pwn),
        'seds/sed_gtlike_2bpd_%s_%s.png' % (hypothesis,pwn),
        'seds/sed_gtlike_1bpd_%s_%s.png' % (hypothesis,pwn),
        'seds/sed_gtlike_%s_%s.png' % (hypothesis,pwn),
        'seds/sed_pointlike_%s_%s.png' % (hypothesis,pwn))

    get_img_table(
        'plots/test_cutoff_%s_%s.png' % (hypothesis,pwn))


    title('Extra: Smoothed Counts (0.25)')
    get_img_table(
        'plots/source_0.25_%s_%s.png' % (hypothesis,pwn),
        'plots/sources_0.25_%s_%s.png' % (hypothesis,pwn))

    title('Extra: Counts (0.25)')
    get_img_table(
        'plots/counts_source_0.25_%s_%s.png' % (hypothesis,pwn),
        'plots/counts_residual_0.25_%s_%s.png' % (hypothesis,pwn))

    title('Extra: Band Smoothed Counts (0.25)')
    get_img_table(
        'plots/band_source_0.25_%s_%s.png' % (hypothesis,pwn),
        'plots/band_sources_0.25_%s_%s.png' % (hypothesis,pwn))
    index_t2t.append("""```
%s
```""" % yaml.dump(results))

    t2t(index_t2t, pwn)

def build_all_pages():
    for pwn in pwnlist: build_each_page(pwn)

build_main_website()
build_all_pages()

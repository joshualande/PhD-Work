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

base=expandvars('$pwndata/spectral/v9')
#base=expandvars('$pwndata/spectral/temp')



analysis='analysis_plots'


def get_pwnlist():
    pwnlist=sorted(yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_data_lande.yaml'))).keys())
    return pwnlist

pwnlist=get_pwnlist()

website=join(base,'website')

if not os.path.exists(website): os.makedirs(website)



def get_results(pwn):
    f = join(base,analysis.replace('plots','no_plots'),pwn,'results_%s.yaml' % pwn)

    if not os.path.exists(f): return None
    results = yaml.load(open(f))

    if not results.has_key('at_pulsar') or \
       not results['at_pulsar'].has_key('pointlike') or \
       not results['at_pulsar'].has_key('gtlike'):
        return None
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
            pt_at_pulsar=results['at_pulsar']['pointlike']

            if results.has_key('point') and results['point'].has_key('pointlike') and results['point'].has_key('gtlike'):
                point_finished = True

                gt_point=results['point']['gtlike']
                pt_point=results['point']['pointlike']

                ts_point=max(gt_point['TS'],0)
            else:
                point_finished = False

            if results.has_key('extended') and results['extended'].has_key('pointlike') and results['extended'].has_key('gtlike'):
                ext_finished = True

                gt_extended=results['extended']['gtlike']
                pt_extended=results['extended']['pointlike']

                ts_ext=max(gt_extended['ts_ext'],0)
            else:
                ext_finished = False

            ts_at_pulsar=max(gt_at_pulsar['TS'],0)
            table['TS_at_pulsar'].append('%.1f' % ts_at_pulsar)

            if point_finished:
                ts_loc = ts_point - ts_at_pulsar
                table['TS_loc'].append('%.1f' % (ts_loc))
            else:
                table['TS_loc'].append('None')
                
            if ext_finished:
                table['TS_ext'].append('%.1f' % ts_ext)
            else:
                table['TS_ext'].append('None')


            if ext_finished and ts_point > 25 and ts_ext > 16:
                # is extended
                besttype = 'extended'
                self.hypothesis = 'extended'
                gt=gt_extended
                pt=pt_extended

            elif point_finished and ts_point > 25:
                # is point
                besttype = 'point'
                self.hypothesis = 'point'
                gt=gt_point
                pt=pt_point

            elif (not point_finished) and ts_at_pulsar > 25:
                # is point at_pulsar, only b/c 'point' has not finished
               besttype='point'
               self.hypothesis='at_pulsar'
               gt=gt_at_pulsar
               pt=pt_at_pulsar

            else:
                # upper limit
                besttype = 'ul'
                self.hypothesis = 'at_pulsar'
                gt=gt_at_pulsar
                pt=pt_at_pulsar


            displacement = np.degrees(SkyDir(*pt['equ']).difference(SkyDir(*pt_at_pulsar['equ'])))
            table['disp'].append('%.2f' % displacement)

            if besttype != 'ul':
                flux=gt['flux']['flux']
                flux_err=gt['flux']['flux_err']
                table[flux_name].append('%.1f +/- %.1f' % (flux/1e-9,flux_err/1e-9))
            else:
                if gt.has_key('upper_limit') and \
                   type(gt['upper_limit']) == dict and \
                   gt['upper_limit'].has_key('flux'):
                    ul=gt['upper_limit']['flux']
                    table[flux_name].append('<%.1f' % (ul/1e-9))
                else:
                    table[flux_name].append('-')

            if besttype != 'ul':
                index=-1*gt['model']['Index']
                index_err=-1*gt['model']['Index_err']
                table[gamma_name].append('%.1f +/- %.1f' % (index,index_err))
            else:
                table[gamma_name].append('-')
            
            if gt.has_key('bands'):

                bands=gt['bands']
                if not np.allclose(bands['energy']['lower'], [1e2, 1e3, 1e4]) or \
                   not np.allclose(bands['energy']['upper'], [1e3, 1e4, 10**5.5]):
                    raise Exception("...")

                ts1,ts2,ts3=bands['TS']
                index1,index2,index3=bands['index']['value']
                index_err1,index_err2,index_err3=bands['index']['error']

                flux1,flux2,flux3=bands['flux']['value']
                flux_err1,flux_err2,flux_err3=bands['flux']['error']

                ul1,ul2,ul3=bands['flux']['upper_limit']

                table['TS(.1-1)'].append('%.1f' % ts1)
                if ts1>25:
                    table['F(.1-1)'].append('%.1f +/- %.1f' % (flux1/1e-9,flux_err1/1e-9))
                    table['Index(.1-1)'].append('%.1f +/- %.1f' % (index1,index_err1))
                else:
                    table['F(.1-1)'].append('<%.1f' % (ul1/1e-9))
                    table['Index(.1-1)'].append('-')

                table['TS(1-10)'].append('%.1f' % ts2)
                if ts2>25:
                    table['F(1-10)'].append('%.1f +/- %.1f' % (flux2/1e-9,flux_err2/1e-9))
                    table['Index(1-10)'].append('%.1f +/- %.1f' % (index2,index_err2))
                else:
                    table['F(1-10)'].append('<%.1f' % (ul2/1e-9))
                    table['Index(1-10)'].append('-')

                table['TS(10-316)'].append('%.1f' % ts3)
                if ts3>25:
                    table['F(10-316)'].append('%.1f +/- %.1f' % (flux3/1e-9,flux_err3/1e-9))
                    table['Index(10-316)'].append('%.1f +/- %.1f' % (index3,index_err3))
                else:
                    table['F(10-316)'].append('<%.1f' % (ul3/1e-9))
                    table['Index(10-316)'].append('-')
            else:
                table['F(.1-1)'].append('-')
                table['Index(.1-1)'].append('-')
                table['TS(1-10)'].append('-')
                table['F(1-10)'].append('-')
                table['Index(1-10)'].append('-')
                table['TS(10-316)'].append('-')
                table['F(10-316)'].append('-')
                table['Index(10-316)'].append('-')

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

    all = ['at_pulsar', 'point', 'extended']
            
    title('at_pulsar Source TS Maps')
    get_img_table('plots/tsmap_source_%s_%s.png' % ('at_pulsar',pwn),
                  'plots/band_tsmap_source_%s_%s.png' % ('at_pulsar',pwn),
                 )

    title('Residual TS Maps')
    get_img_table(*['plots/tsmap_residual_%s_%s.png' % (i,pwn) for i in all])

    title('at_pulsar Smoothed Counts Diffuse Subtracted (0.1)')
    get_img_table('plots/sources_0.1_%s_%s.png' % ('at_pulsar',pwn),
                  'plots/band_sources_0.1_%s_%s.png' % ('at_pulsar',pwn))

    title('Smoothed Counts BG Source Subtracted (0.1)')
    get_img_table(*['plots/source_0.1_%s_%s.png' % (i,pwn) for i in all])

    title('Band Residual TS Maps')
    get_img_table(*['plots/band_tsmap_residual_%s_%s.png' % (i,pwn) for i in all])


    title('Band Smoothed Counts BG Source Subtracted (0.1)')
    get_img_table('plots/band_source_0.1_%s_%s.png' % (hypothesis,pwn))

    title('gtlike SED (4bpd')
    get_img_table(*['seds/sed_gtlike_4bpd_%s_%s.png' % (i,pwn) for i in all])

    title('gtlike SED (2bpd')
    get_img_table(*['seds/sed_gtlike_2bpd_%s_%s.png' % (i,pwn) for i in all])

    title('gtlike SED (1bpd')
    get_img_table(*['seds/sed_gtlike_1bpd_%s_%s.png' % (i,pwn) for i in all])

    get_img_table(
        'plots/test_cutoff_%s_%s.png' % (hypothesis,pwn))

    index_t2t.append("""```
%s
```""" % yaml.dump(results))


    title('Pointlike SEDs')
    get_img_table(*['seds/sed_pointlike_%s_%s.png' % (i,pwn) for i in all])

    title('Extra: Smoothed Counts (0.25)')
    get_img_table(*['plots/source_0.25_%s_%s.png' % (i,pwn) for i in all])

    title('Extra: Smoothed Counts (0.25)')
    get_img_table(*['plots/sources_0.25_%s_%s.png' % (i,pwn) for i in all])


    title('Extra: Band Smoothed Counts (0.25)')
    get_img_table(*['plots/band_source_0.25_%s_%s.png' % (i,pwn) for i in all])
    get_img_table(*['plots/band_sources_0.25_%s_%s.png' % (i,pwn) for i in all])

    title('Counts (0.1)')
    get_img_table('plots/counts_residual_0.1_%s_%s.png' % (hypothesis,pwn),
        'plots/counts_source_0.1_%s_%s.png' % (hypothesis,pwn))


    title('Extra: Counts (0.25)')
    get_img_table(
        'plots/counts_source_0.25_%s_%s.png' % (hypothesis,pwn),
        'plots/counts_residual_0.25_%s_%s.png' % (hypothesis,pwn))

    t2t(index_t2t, pwn)

def build_all_pages():
    for pwn in pwnlist: build_each_page(pwn)

build_main_website()
build_all_pages()

import sys
from skymaps import SkyDir
import numpy as np
from glob import glob
import yaml
from StringIO import StringIO
import re
import os
from os.path import join,exists,expandvars
from collections import defaultdict, OrderedDict

import asciitable

from table_helper import BestHypothesis

from lande.utilities.website import t2t

"""
var_version='v10/variability/v3/'
spec_version='v12'
gtlike=True
"""

"""
var_version='v13/variability/v1/'
spec_version='v13'
gtlike=False
"""

var_version='none'
spec_version='temp'
gtlike=True

variability_unix=expandvars('$pwndata/spectral/%s' % var_version)
variability_website=expandvars('../../%s' % var_version)


analysis_plots_unix=expandvars('$pwndata/spectral/%s/analysis_plots' % spec_version)
analysis_no_plots_unix=expandvars('$pwndata/spectral/%s/analysis_no_plots' % spec_version)
website_unix=expandvars('$pwndata/spectral/%s/website' % spec_version)
analysis_plots_website=expandvars('../../%s/analysis_plots' % spec_version)
analysis_no_plots_website=expandvars('../../%s/analysis_no_plots' % spec_version)

def get_pwnlist():
    pwnlist=sorted(yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_data_lande.yaml'))).keys())
    return pwnlist

pwnlist=get_pwnlist()


if not os.path.exists(website_unix): os.makedirs(website_unix)



def get_results(pwn):
    f = join(analysis_no_plots_unix,pwn,'results_%s.yaml' % pwn)

    if not os.path.exists(f): return None
    results = yaml.load(open(f))

    if not results.has_key('at_pulsar') or \
       not results['at_pulsar'].has_key('pointlike'):
       return None

    if gtlike:
        if not results['at_pulsar'].has_key('gtlike'):
            return None
        else:
            return results
    else:
        # Quick fix, if pointlike copy of pointlike stuff into gtlike stuff
        for k in ['at_pulsar', 'point', 'extended']:
            if results.has_key(k):
                results[k]['gtlike'] = results[k]['pointlike']
        return results

def get_variability(pwn):
    f = join(variability_unix, pwn, 'results_%s.yaml' % pwn)
    if not os.path.exists(f): return None
    return yaml.load(open(f))


class TableFormatter(object):

    def __init__(self, pwnlist):

        flux_name=r'F(0.1-100)'
        gamma_name=r'Gamma'

        table = OrderedDict()
        for k in ['PSR', 
                  'TS_at_pulsar', 'TS_loc', 'TS_ext', 'TS_var',
                  'disp', flux_name, gamma_name,
                  'TS(.1-1)', 'F(.1-1)', 'Index(.1-1)',
                  'TS(1-10)', 'F(1-10)', 'Index(1-10)', 
                  'TS(10-100)', 'F(10-100)', 'Index(10-100)']:
            table[k] = ['None']*len(pwnlist)

        for i,pwn in enumerate(pwnlist):
            print pwn

            table['PSR'][i]='[%s %s.html]' % (pwn,pwn)

            results = get_results(pwn)
            if results is None: continue

            gt_at_pulsar=results['at_pulsar']['gtlike']
            pt_at_pulsar=results['at_pulsar']['pointlike']

            if results.has_key('point') and results['point'].has_key('pointlike') and results['point'].has_key('gtlike'):
                point_finished = True

                gt_point=results['point']['gtlike']
                pt_point=results['point']['pointlike']

                ts_point=gt_point['TS']
            else:
                point_finished = False

            if results.has_key('extended') and results['extended'].has_key('pointlike') and results['extended'].has_key('gtlike'):
                ext_finished = True

                gt_extended=results['extended']['gtlike']
                pt_extended=results['extended']['pointlike']

                ts_ext=gt_extended['ts_ext']
            else:
                ext_finished = False

            bold = lambda text, doit=True: '**%s**' % text if doit else text

            ts_at_pulsar=gt_at_pulsar['TS']
            table['TS_at_pulsar'][i] = bold('%.1f' % ts_at_pulsar, ts_at_pulsar>25)


            if point_finished:
                ts_loc = ts_point - ts_at_pulsar
                table['TS_loc'][i] = bold('%.1f' % (ts_loc), ts_point>25)
                
            if ext_finished:
                table['TS_ext'][i] = bold('%.1f' % ts_ext, ts_point > 25 and ts_ext > 16)

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



            displacement = np.degrees(SkyDir(*pt['position']['equ']).difference(SkyDir(*pt_at_pulsar['position']['equ'])))
            table['disp'][i] = '%.2f' % displacement

            if besttype != 'ul':
                flux=gt['flux']['flux']
                flux_err=gt['flux']['flux_err']
                table[flux_name][i] = '%.1f +/- %.1f' % (flux/1e-9,flux_err/1e-9)
            else:
                if gt.has_key('upper_limit') and \
                   type(gt['upper_limit']) == dict and \
                   gt['upper_limit'].has_key('flux'):
                    ul=gt['upper_limit']['flux']
                    table[flux_name][i] = '<%.1f' % (ul/1e-9)

            if besttype != 'ul':
                index=-1*gt['model']['Index']
                index_err=-1*gt['model']['Index_err']
                table[gamma_name][i] = '%.1f +/- %.1f' % (index,index_err)
            else:
                table[gamma_name][i] = '-'
            
            if gt.has_key('bands'):

                bands=gt['bands']
                if not np.allclose(bands['energy']['lower'], [1e2, 1e3, 1e4]) or \
                   not np.allclose(bands['energy']['upper'], [1e3, 1e4, 1e5]):
                    raise Exception("...")

                ts1,ts2,ts3=bands['TS']
                index1,index2,index3=bands['index']['value']
                index_err1,index_err2,index_err3=bands['index']['error']

                flux1,flux2,flux3=bands['flux']['value']
                flux_err1,flux_err2,flux_err3=bands['flux']['error']

                ul1,ul2,ul3=bands['flux']['upper_limit']

                table['TS(.1-1)'][i] = '%.1f' % ts1
                if ts1>25:
                    table['F(.1-1)'][i] = '%.1f +/- %.1f' % (flux1/1e-9,flux_err1/1e-9)
                    table['Index(.1-1)'][i] = '%.1f +/- %.1f' % (index1,index_err1)
                else:
                    table['F(.1-1)'][i] = '<%.1f' % (ul1/1e-9)
                    table['Index(.1-1)'][i] = '-'

                table['TS(1-10)'][i] = '%.1f' % ts2
                if ts2>25:
                    table['F(1-10)'][i] = '%.1f +/- %.1f' % (flux2/1e-9,flux_err2/1e-9)
                    table['Index(1-10)'][i] = '%.1f +/- %.1f' % (index2,index_err2)
                else:
                    table['F(1-10)'][i] = '<%.1f' % (ul2/1e-9)
                    table['Index(1-10)'][i] = '-'

                table['TS(10-100)'][i] = '%.1f' % ts3
                if ts3>25:
                    table['F(10-100)'][i] = '%.1f +/- %.1f' % (flux3/1e-9,flux_err3/1e-9)
                    table['Index(10-100)'][i] = '%.1f +/- %.1f' % (index3,index_err3)
                else:
                    table['F(10-100)'][i] = '<%.1f' % (ul3/1e-9)
                    table['Index(10-100)'][i] = '-'

            var = get_variability(pwn)
            if var is not None:
                table['TS_var'][i] = '%.1f' % var['TS_var']['gtlike']


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
    t2t(index_t2t, join(website_unix,'index.t2t'))

def build_each_page(pwn):
    results = get_results(pwn)
    if results is None: return

    index_t2t = []
    index_t2t.append(pwn+'\n\n')
    index_t2t.append('([back index.html])')
    t=TableFormatter([pwn])
    index_t2t.append(str(t))
    index_t2t.append('')
    index_t2t.append('[Analysis Folder %s/%s]\n' % (analysis_plots_website,pwn))
    index_t2t.append('[log (plots) %s/%s/log.txt]\n' % (analysis_plots_website,pwn))
    index_t2t.append('[log (no plots) %s/%s/log.txt]\n' % (analysis_no_plots_website,pwn))
    index_t2t.append('[Variability %s/%s/]\n' % (variability_website, pwn))

    hypothesis=t.hypothesis

    get_img_table = lambda *args: index_t2t.append('|| ' + ' | '.join(['[%s/%s/%s]' % (analysis_plots_website,pwn,i) for i in args]) + ' |\n\n')
    get_sed_table = lambda *args: index_t2t.append('|| ' + ' | '.join(['[%s/%s/%s]' % (analysis_no_plots_website,pwn,i) for i in args]) + ' |\n\n')

    title = lambda i: index_t2t.append('== %s ==' % i)

    title('Phase Info')
    get_img_table(
        'plots/phaseogram_%s.png' % (pwn), 
        'plots/phase_vs_time_%s.png' % (pwn))

    all = ['at_pulsar', 'point', 'extended']
            
    title('at_pulsar Source TS Maps')
    get_img_table('plots/tsmap_source_%s_%s.png' % ('at_pulsar',pwn),
                  'plots/band_tsmap_source_%s_%s_5deg.png' % ('at_pulsar',pwn),
                 )

    title('Residual TS Maps')
    get_img_table(*['plots/tsmap_residual_%s_%s_5deg.png' % (i,pwn) for i in all])

    title('at_pulsar Smoothed Counts Diffuse Subtracted (0.1)')
    get_img_table('plots/sources_0.1_%s_%s_5deg.png' % ('at_pulsar',pwn),
                  'plots/band_sources_0.1_%s_%s_5deg.png' % ('at_pulsar',pwn))

    title('Smoothed Counts BG Source Subtracted (0.1)')
    get_img_table(*['plots/source_0.1_%s_%s_5deg.png' % (i,pwn) for i in all])

    title('Band Residual TS Maps')
    get_img_table(*['plots/band_tsmap_residual_%s_%s_5deg.png' % (i,pwn) for i in all])


    title('Band Smoothed Counts BG Source Subtracted (0.1)')
    get_img_table('plots/band_source_0.1_%s_%s_5deg.png' % (hypothesis,pwn))

    title('gtlike SED (4bpd')
    get_sed_table(*['seds/sed_gtlike_4bpd_%s_%s.png' % (i,pwn) for i in all])

    title('gtlike SED (2bpd')
    get_sed_table(*['seds/sed_gtlike_2bpd_%s_%s.png' % (i,pwn) for i in all])

    title('gtlike SED (1bpd')
    get_sed_table(*['seds/sed_gtlike_1bpd_%s_%s.png' % (i,pwn) for i in all])

    get_sed_table(
        'plots/test_cutoff_%s_%s.png' % (hypothesis,pwn))

    # Add variability plot
    index_t2t.append('| [%s/%s/variability_%s.png] |' % (variability_website,pwn,pwn))

    index_t2t.append("""```
%s
```""" % yaml.dump(results))


    title('Pointlike SEDs')
    get_sed_table(*['seds/sed_pointlike_%s_%s.png' % (i,pwn) for i in all])

    title('Extra: Smoothed Counts (0.25)')
    get_img_table(*['plots/source_0.25_%s_%s_5deg.png' % (i,pwn) for i in all])

    title('Extra: Smoothed Counts (0.25)')
    get_img_table(*['plots/sources_0.25_%s_%s_5deg.png' % (i,pwn) for i in all])


    title('Extra: Band Smoothed Counts (0.25)')
    get_img_table(*['plots/band_source_0.25_%s_%s_5deg.png' % (i,pwn) for i in all])
    get_img_table(*['plots/band_sources_0.25_%s_%s_5deg.png' % (i,pwn) for i in all])

    title('Counts (0.1)')
    get_img_table('plots/counts_residual_0.1_%s_%s_5deg.png' % (hypothesis,pwn),
        'plots/counts_source_0.1_%s_%s_5deg.png' % (hypothesis,pwn))


    title('Extra: Counts (0.25)')
    get_img_table(
        'plots/counts_source_0.25_%s_%s_5deg.png' % (hypothesis,pwn),
        'plots/counts_residual_0.25_%s_%s_5deg.png' % (hypothesis,pwn))


    var = get_variability(pwn)

    index_t2t.append("""```
%s
```""" % yaml.dump(var))

    t2t(index_t2t, join(website_unix,'%s.t2t' % pwn))

def build_all_pages():
    for pwn in pwnlist: build_each_page(pwn)

build_main_website()
build_all_pages()

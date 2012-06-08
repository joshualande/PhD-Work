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
from itertools import product

import asciitable

from table_helper import BestHypothesis

from lande.utilities.website import t2t

var_version='none'
#spec_version='v19'
spec_version='v22'

variability_unix=expandvars('$pwndata/spectral/%s' % var_version)
variability_website=expandvars('../../%s' % var_version)


analysis_unix=expandvars('$pwndata/spectral/%s/analysis' % spec_version)
website_unix=expandvars('$pwndata/spectral/%s/website' % spec_version)

analysis_website=expandvars('../../%s/analysis' % spec_version)

def get_pwnlist():
    pwnlist=sorted(yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_data_lande.yaml'))).keys())
    return pwnlist

pwnlist=get_pwnlist()


if not os.path.exists(website_unix): os.makedirs(website_unix)



def get_results(pwn):
    f = join(analysis_unix,pwn,'results_%s_pointlike.yaml' % pwn)

    if not os.path.exists(f): return None
    results = yaml.load(open(f))
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
        for k in ['PSR', 'TS_at_pulsar_ptlike', 'TS_loc_ptlike', 'TS_ext_ptlike', 'TS_cutoff_ptlike', 'disp']:
            table[k] = ['None']*len(pwnlist)

        for i,pwn in enumerate(pwnlist):
            print pwn

            table['PSR'][i]='[%s %s.html]' % (pwn,pwn)

            results = get_results(pwn)
            if results is None: continue

            pt_at_pulsar=results['at_pulsar']['pointlike']
            pt_point=results['point']['pointlike']
            pt_extended=results['extended']['pointlike']


            bold = lambda text, doit=True: '**%s**' % text if doit else text

            ts_at_pulsar=pt_at_pulsar['TS']
            ts_point = pt_point['TS']
            ts_gauss = pt_extended['TS']
            ts_ext = ts_gauss - ts_point

            table['TS_at_pulsar_ptlike'][i] = bold('%.1f' % ts_at_pulsar, ts_at_pulsar>25)


            ts_loc = ts_point - ts_at_pulsar
            table['TS_loc_ptlike'][i] = bold('%.1f' % (ts_loc), ts_point>25)
                
            table['TS_ext_ptlike'][i] = bold('%.1f' % ts_ext, ts_point > 25 and ts_ext > 16)


            displacement = np.degrees(SkyDir(*pt_point['position']['equ']).difference(SkyDir(*pt_at_pulsar['position']['equ'])))
            table['disp'][i] = '%.2f' % displacement

            try:
                ts_cutoff = pt_point['test_cutoff']['TS_cutoff']
                table['TS_cutoff_ptlike'][i] = bold('%.1f' % ts_cutoff, ts_cutoff > 16)
            except:
                table['TS_cutoff_ptlike'][i] = 'None'

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
    #results = get_results(pwn)
    #if results is None: return

    index_t2t = []
    index_t2t.append(pwn+'\n\n')
    index_t2t.append('([back index.html])')
    t=TableFormatter([pwn])
    index_t2t.append(str(t))
    index_t2t.append('')
    index_t2t.append('[Analysis Folder %s/%s]\n' % (analysis_website,pwn))
    index_t2t.append('[log (pointlike) %s/%s/log_run_%s.txt]\n' % (analysis_website,pwn,pwn))

    index_t2t.append('[results (pointlike) %s/%s/results_%s_pointlike.yaml]\n' % (analysis_website,pwn,pwn))

    get_img_table = lambda *args: index_t2t.append('|| ' + ' | '.join(['[%s/%s/%s]' % (analysis_website,pwn,i) for i in args]) + ' |\n\n')
    get_sed_table = lambda *args: index_t2t.append('|| ' + ' | '.join(['[%s/%s/%s]' % (analysis_website,pwn,i) for i in args]) + ' |\n\n')

    title = lambda i: index_t2t.append('\n\n== %s ==' % i)

    title('Phase Info')
    get_img_table('plots/phaseogram_%s.png' % (pwn),'plots/phase_vs_time_%s.png' % (pwn))

    all = ['at_pulsar', 'point', 'extended']
            
    title('Source TS Maps')
    get_img_table(*['plots/tsmap_source_%s_%s_5deg.png' % (i,pwn) for i in all])
    get_img_table(*['plots/band_tsmap_source_%s_%s_5deg.png' % (i,pwn) for i in all])

    title('Residual TS Maps')
    get_img_table(*['plots/tsmap_residual_%s_%s_5deg.png' % (i,pwn) for i in all])
    get_img_table(*['plots/band_tsmap_residual_%s_%s_5deg.png' % (i,pwn) for i in all])

    title('at_pulsar Smoothed Counts Diffuse Subtracted (0.1)')
    get_img_table(*['plots/sources_%s_%s_5deg_0.1deg.png' % (i,pwn) for i in all])
    get_img_table(*['plots/band_sources_%s_%s_5deg_0.1deg.png' % (i,pwn) for i in all])

    title('Smoothed Counts BG Source Subtracted (0.1)')
    get_img_table(*['plots/source_%s_%s_5deg_0.1deg.png' % (i,pwn) for i in all])



    title('Band Smoothed Counts BG Source Subtracted (0.1)')
    get_img_table(*['plots/band_source_%s_%s_5deg_0.1deg.png' % (i,pwn) for i in all])

    title('gtlike SED (4bpd)')
    get_sed_table(*['seds/sed_gtlike_4bpd_%s_%s.png' % (i,pwn) for i in all])

    title('gtlike SED (2bpd)')
    get_sed_table(*['seds/sed_gtlike_2bpd_%s_%s.png' % (i,pwn) for i in all])

    title('gtlike SED (1bpd)')
    get_sed_table(*['seds/sed_gtlike_1bpd_%s_%s.png' % (i,pwn) for i in all])

    title('gtlike Cutoff test')
    get_sed_table(*['plots/test_cutoff_%s_%s.png' % (i,pwn) for i in all])

    title('Variability')
    index_t2t.append('| [%s/%s/variability_%s.png] |' % (variability_website,pwn,pwn))

    title('Pointlike SEDs')
    get_sed_table(*['seds/sed_pointlike_%s_%s.png' % (i,pwn) for i in all])

    title('Extra: Source TS Maps (10 deg)')
    get_img_table(*['plots/tsmap_source_%s_%s_10deg.png' % (i,pwn) for i in all])
    get_img_table(*['plots/band_tsmap_source_%s_%s_10deg.png' % (i,pwn) for i in all])

    title('Extra: Residual TS Maps')
    get_img_table(*['plots/tsmap_residual_%s_%s_10deg.png' % (i,pwn) for i in all])
    get_img_table(*['plots/band_tsmap_residual_%s_%s_10deg.png' % (i,pwn) for i in all])


    title('Extra: Smoothed Counts (0.25deg)')
    get_img_table(*['plots/source_0.25_%s_%s_5deg.png' % (i,pwn) for i in all])

    title('Extra: Smoothed Counts (0.25deg)')
    get_img_table(*['plots/sources_0.25_%s_%s_5deg.png' % (i,pwn) for i in all])


    title('Extra: Band Smoothed Counts (0.25)')
    get_img_table(*['plots/band_source_%s_%s_5deg_0.25deg.png' % (i,pwn) for i in all])
    get_img_table(*['plots/band_sources_%s_%s_5deg_0.25deg.png' % (i,pwn) for i in all])

    title('Counts (0.1)')
    get_img_table(*['plots/counts_residual_%s_%s_5deg_0.1deg.png' % (i,pwn) for i in all])

    get_img_table(*['plots/counts_source_%s_%s_5deg_0.1deg.png' % (i,pwn) for i in all])


    title('Extra: Counts (0.25)')
    get_img_table(*['plots/counts_source_%s_%s_5deg_0.25deg.png' % (i,pwn) for i in all])
    get_img_table(*['plots/counts_residual_%s_%s_5deg_0.25deg.png' % (i,pwn) for i in all])


    var = get_variability(pwn)

    index_t2t.append("""```
%s
```""" % yaml.dump(var))

    t2t(index_t2t, join(website_unix,'%s.t2t' % pwn))

def build_all_pages():
    for pwn in pwnlist: build_each_page(pwn)

build_main_website()
build_all_pages()

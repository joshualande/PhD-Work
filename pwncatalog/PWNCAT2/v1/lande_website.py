import sys
from glob import glob
import yaml
from StringIO import StringIO
import re
import os
from os.path import join,exists
from os.path import join as j
from collections import defaultdict

import asciitable

from toolbag import OrderedDefaultdict

#base='/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT1/fits/analyze_v38/'

base='/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analysis/analysis_v1/'
pwnlist=sorted([os.path.basename(i) for i in glob(j(base,'analysis','PSR*'))])

website=join(base,'website')

if not os.path.exists(website): os.makedirs(website)



def get_results(pwn):
    f = j(base,'analysis',pwn,'results_%s.yaml' % pwn)
    if not os.path.exists(f): return None
    results = yaml.load(open(f))

    #for hypothesis in ['at_pulsar', 'point', 'extended']:
    for hypothesis in ['at_pulsar']:
        h=results[hypothesis]
        if not results.has_key(hypothesis):
            results[hypothesis]=defaultdict(lambda:-1),
        for t in ['gtlike','pointlike']:
            if not h.has_key(t):
                h[t]=defaultdict(lambda:-1)
            for i in ['model', 'upper_limit', 'flux']:
                if not h[t].has_key(i):
                    h[t][i]=defaultdict(lambda:-1)
    return results

def get_sed(pwn,binning,hypothesis):
    filename=j(base,'analysis',pwn,'seds','sed_gtlike_%s_%s_%s.yaml' % (binning, hypothesis, pwn))
    if os.path.exists(filename):
        return yaml.load(open(filename))
    elif binning == '1bpd':
        d=defaultdict(lambda: defaultdict(lambda:[-1,-1,-1]))
        d['Test_Statistic']=[-1,-1,-1]
        return d
    else:
        raise Exception("...")

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


def t2t(lines,name): 
    """ create the HTML for a given t2t file. """
    filename = join(website,'%s.t2t' % name)
    
    temp=open(filename,'w')
    temp.write(
        '\n'.join(lines))
    temp.close()
        
    os.system('txt2tags --target html --style color.css --css-sugar %s' % filename)


def format_table(pwnlist):


    table = OrderedDefaultdict(list)

    flux_name=r'F(0.1-316)'
    gamma_name=r'Gamma'

    for pwn in pwnlist:

        results = get_results(pwn)
        if results is None: continue

        gt=results['at_pulsar']['gtlike']

        table['PSR'].append('[%s %s.html]' % (pwn,pwn))

        ts=max(gt['TS'],0)
        table['TS'].append('%.1f' % ts)
        
        try:
            ts_ext=max(results['extended']['gtlike']['ts_ext'],0)
        except:
            ts_ext=-1

        table['TS_ext'].append('%.1f' % ts_ext)


        if ts > 25:
            flux=gt['flux']['flux']
            flux_err=gt['flux']['flux_err']
            table[flux_name].append('%.2f +/- %.2f' % (flux/1e-9,flux_err/1e-9) )
        else:
            ul=gt['upper_limit']['flux']
            table[flux_name].append('<%.2f' % (ul/1e-9))


        index=-1*gt['model']['Index']
        index_err=-1*gt['model']['Index_err']

        table[gamma_name].append('%.2f +/- %.2f' % (index,index_err) if ts>25 else '-')

        sed = get_sed(pwn,'1bpd','at_pulsar')
        bandts = map(lambda x: max(x,0), sed['Test_Statistic'])
        flux = sed['Ph_Flux']['Value']
        flux_err = sed['Ph_Flux']['Error']
        ul = sed['Ph_Flux']['Upper_Limit']

        table['TS(.1-1)'].append('%.1f' % bandts[0])
        table['Flux(.1-1)'].append('%.2f +/- %.2f' % (flux[0]/1e-9,flux_err[0]/1e-9) if bandts[0] > 25 else '<%.2f' % (ul[0]/1e-9))

        table['TS(1-10)'].append('%.1f' % bandts[1])
        table['Flux(1-10)'].append('%.2f +/- %.2f' % (flux[1]/1e-9,flux_err[1]/1e-9) if bandts[1] > 25 else '<%.2f' % (ul[1]/1e-9))

        table['TS(10-316)'].append('%.1f' % bandts[2])
        table['Flux(10-316)'].append('%.2f +/- %.2f' % (flux[2]/1e-9,flux_err[2]/1e-9) if bandts[2] > 25 else '<%.2f' % (ul[2]/1e-9))

    return get_t2t_table(table)

def build_main_website():

    index_t2t = []
    index_t2t.append('PWNCatalog')
    index_t2t.append('')
    index_t2t.append('')
    index_t2t.append(format_table(pwnlist))
    t2t(index_t2t, 'index')

def build_each_page(pwn):
    results = get_results(pwn)
    if results is None: return

    index_t2t = []
    index_t2t.append(pwn)
    index_t2t.append('')
    index_t2t.append('')
    index_t2t.append(format_table([pwn]))
    index_t2t.append('')

    hypothesis='at_pulsar'
    for title,plot in [

        ['Phaseogram','plots/phaseogram_%s.png' % (pwn)],
        ['Phase vs Time','plots/phase_vs_time_%s.png' % (pwn)],

        ['Source Counts %s (.1)' % hypothesis,'plots/source_0.1_%s_%s.png' % (hypothesis,pwn)],
        ['Sources Counts %s (.1)' % hypothesis,'plots/sources_0.1_%s_%s.png' % (hypothesis,pwn)],
        
        ['Source Counts %s (.25)' % hypothesis,'plots/source_0.25_%s_%s.png' % (hypothesis,pwn)],
        ['Sources Counts %s (.25)' % hypothesis,'plots/sources_0.25_%s_%s.png' % (hypothesis,pwn)],

        ['Source TSMap %s' % hypothesis,'plots/source_tsmap_%s_%s.png' % (hypothesis,pwn)],
        ['Residual TSMap %s' % hypothesis,'plots/residual_tsmap_%s_%s.png' % (hypothesis,pwn)],
        ['Band Source TSMap %s' % hypothesis,'plots/band_source_tsmap_%s_%s.png' % (hypothesis,pwn)],
        ['Band Residual TSMap %s' % hypothesis,'plots/band_residual_tsmap_%s_%s.png' % (hypothesis,pwn)],


        ['Counts Residual %s' % hypothesis,'plots/counts_residual_0.1_%s_%s.png' % (hypothesis,pwn)],
        ['Counts Residual %s' % hypothesis,'plots/counts_residual_0.25_%s_%s.png' % (hypothesis,pwn)],

        ['Counts Excess %s' % hypothesis,'plots/counts_excess_0.1_%s_%s.png' % (hypothesis,pwn)],
        ['Counts Excess%s' % hypothesis,'plots/counts_excess_0.25_%s_%s.png' % (hypothesis,pwn)],

        ['SED gtlike 4bpd %s' % hypothesis,'seds/sed_gtlike_4bpd_%s_%s.png' % (hypothesis,pwn)],
        ['SED gtlike 2bpd %s' % hypothesis,'seds/sed_gtlike_2bpd_%s_%s.png' % (hypothesis,pwn)],
        ['SED gtlike 1bpd %s' % hypothesis,'seds/sed_gtlike_1bpd_%s_%s.png' % (hypothesis,pwn)],
        ['Test Cutoff %s' % hypothesis,'plots/test_cutoff_%s_%s.png' % (hypothesis,pwn)],
    ]:
        index_t2t.append("""\

== %s plot for %s ==

[../analysis/%s/%s]""" % (title,pwn,pwn,plot))

    index_t2t.append('')
    index_t2t.append("""```
%s
```""" % yaml.dump(results))


    t2t(index_t2t, pwn)

def build_all_pages():
    for pwn in pwnlist: build_each_page(pwn)

build_main_website()
build_all_pages()

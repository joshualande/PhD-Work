import yaml
import os
from glob import glob
from os.path import join,expandvars,exists,basename

from lande.utilities.website import t2t

version='v6'
website_path=expandvars('$pwn_off_peak_results/%s/website' % version)
analysis_path=expandvars('$pwn_off_peak_results/%s/analysis' % version)


if not exists(website_path): os.makedirs(website_path)

website=expandvars(join(website_path,'index.t2t'))


pwnlist=sorted(yaml.load(open(expandvars('$pwndata/pwncat2_data_lande.yaml'))).keys())

lines = ['Off Peak', '', '']

for pwn in pwnlist:

    temp='%s/%s/results_%s.yaml' % (analysis_path,pwn,pwn)
    if os.path.exists(temp):
        r=yaml.load(open(temp))
        off_peak=r['off_peak_phase']

        lines.append('==%s==' % pwn)
        lines.append('[../analysis/%s/results_%s.png]' % (pwn,pwn))
        lines.append('')
        lines.append('[results ../analysis/%s]' % pwn)
        lines.append('')
        lines.append('Off Peak: """%s"""' % str(off_peak))
        lines.append('===')
    else:
        print 'SKIPPING %s' % pwn

t2t(lines,website)

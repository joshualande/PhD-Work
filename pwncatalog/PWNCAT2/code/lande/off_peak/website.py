import yaml
import os
from glob import glob
from os.path import join,expandvars,exists,basename

from lande.utilities.website import t2t

website_path=expandvars('$pwndata/off_peak/off_peak_bb/pwncat2/v4/website')
analysis_path=expandvars('$pwndata/off_peak/off_peak_bb/pwncat2/v4/analysis')


if not exists(website_path): os.makedirs(website_path)

website=expandvars(join(website_path,'index.t2t'))


pwnlist=sorted(yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_data_lande.yaml'))).keys())

lines = ['Off Peak', '', '']

for pwn in pwnlist:

    r=yaml.load(open('%s/%s/results_%s.yaml' % (analysis_path,pwn,pwn)))
    off_peak=r['off_peak_phase']

    lines.append('==%s==' % pwn)
    lines.append('[../analysis/%s/results_%s.png]' % (pwn,pwn))
    lines.append('')
    lines.append('[results ../analysis/%s]' % pwn)
    lines.append('')
    lines.append('Off Peak: """%s"""' % str(off_peak))
    lines.append('===')

t2t(lines,website)

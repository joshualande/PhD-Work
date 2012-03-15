import yaml
import numpy as np
from os.path import join, expandvars

from uw.utilities.makerec import fitsrec

from lande.utilities.arrays import close

recname = join(expandvars('$tsext_plane_data'), 'v1', 'merged.fits')
r = fitsrec(recname)
print r

index_list = r['index']
ts_point_list = r['ts_point']
ts_ext_list = r['ts_ext']

ts_ext_list = np.where(ts_ext_list > 0, ts_ext_list, 0)

for index in [1.5, 2, 2.5, 3]:

    cut = close(index,index_list)

    print 'index = %s' % index
    print '.. num', sum(cut)
    ts_point = ts_point_list[cut]
    print '.. average ts_point',np.average(ts_point), np.std(ts_point)
    ts_ext = ts_ext_list[cut]
    print '.. average ts_ext',np.average(ts_ext), np.std(ts_ext)
    print 

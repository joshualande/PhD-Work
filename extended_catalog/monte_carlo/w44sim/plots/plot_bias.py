
from os.path import join, expandvars

from lande.utilities.pubplot import set_latex_defaults,get_bw,save

import numpy as np
import h5py
import pylab as P

set_latex_defaults()
bw=get_bw()

savedir = expandvars(join('$w44simdata/','v4', 'merged.hdf5'))
results = h5py.File(savedir, 'r')

r68_Disk = np.asarray(results['r68_Disk'])
r68_Gaussian = np.asarray(results['r68_Gaussian'])
r68_EllipticalDisk = np.asarray(results['r68_EllipticalDisk'])
r68_EllipticalRing = np.asarray(results['r68_EllipticalRing'])

fig=P.figure(None, figsize=(6,6))

axes=fig.add_subplot(221)
axes.hist(ts_point, **hist_kwargs)
axes.xaxis.set_major_locator(MaxNLocator(4))
axes.set_xlabel(r'$\textrm{TS}_\textrm{point}$')

save('w44sim')
save('bias_w44sim')

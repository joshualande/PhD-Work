from matplotlib import rc
rc('ps',usedistiller='xpdf')
rc('text', usetex=True)
rc('font', family='serif', serif="Computer Modern Roman")

import yaml
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pylab import *
from matplotlib.ticker import FuncFormatter
import numpy as np
from mpl_toolkits.axes_grid.axes_grid import Grid
from matplotlib import gridspec


fig=figure(figsize=(4,3))

gs = gridspec.GridSpec(2, 1, height_ratios=[3,2])
ax=plt.subplot(gs[0])
lower_ax = plt.subplot(gs[1], sharex=ax)
fig.subplots_adjust(left=0.20, right=0.95, top=0.95, bottom=0.15)



emin=1000
emax=1000
kwargs=dict(linestyle='-',color='black')

loop_index = 2
diff_factor=10

data=yaml.load(open('extension_sensitivity.yaml'))
exts=np.asarray(data['exts'])
f2yrs=np.asarray(data['f2yrs'])
f10yrs=np.asarray(data['f10yrs'])

ax.fill_between(exts,f2yrs/np.sqrt(5),f2yrs/5, color='lightgrey')

ax.semilogy(exts,f10yrs,**kwargs)

lower_ax.plot(exts,f2yrs/f10yrs,**kwargs)

lower_ax.fill_between(exts,np.sqrt(5),5, color='lightgrey')

# add degrees to the x axis
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, *args: '$%g^\circ$' % x))

ax.set_xlim(0.1,2)

# Use text object for easier alignment

ax.get_xaxis().set_visible(False)

ax.set_ylim(3e-10,2e-8)

ax.set_yscale('log')

ax.set_ylabel('Flux ($\mathrm{ph}\ \mathrm{cm}^{-2}\,\mathrm{s}^{-1}$)')
lower_ax.set_ylabel(r'$\textrm{F}_\textrm{2yr}/\textrm{F}_\textrm{10yr}$')

# align labels: 
#  http://matplotlib.sourceforge.net/faq/howto_faq.html#align-my-ylabels-across-multiple-subplots
lower_ax.yaxis.set_label_coords(-0.15,0.5)
ax.yaxis.set_label_coords(-.15,0.5)

lower_ax.set_xlabel('Extension')

lower_ax.set_ylim(np.sqrt(5)-0.5,5+0.5)
lower_ax.set_xticks([0.1,0.5,1,1.5,2])
lower_ax.set_yticks([2,3,4,5])


savefig('extension_sensitivity.eps')
savefig('extension_sensitivity.pdf')

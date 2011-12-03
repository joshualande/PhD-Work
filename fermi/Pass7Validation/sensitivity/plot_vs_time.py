from matplotlib import rc
rc('ps',usedistiller='xpdf')
rc('text', usetex=True)
rc('font', family='serif', serif="Computer Modern Roman")


from mpl_toolkits.axes_grid1 import make_axes_locatable
from pylab import *
import numpy as N

f=figure(figsize=(6,5))

ax=axes([0.15,0.1,0.8,0.85])


divider = make_axes_locatable(ax)
lower_ax = divider.append_axes("bottom", size=1.2, pad=0.1, sharex=ax)

emin=1000
emax=1000
kwargs=dict(linestyle='-',color='black')

loop_index = 2
diff_factor=10

exts=N.sort(N.append(N.arange(0.1,2.1,0.1),[0.15,0.25,0.35]))

f2yrs=np.asarray([get_sensitivity(e,loop_index,emin,fit_emin,diff_factor,'2') for e in exts])
f10yrs=np.asarray([get_sensitivity(e,loop_index,emin,fit_emin,diff_factor,'10') for e in exts])


ax.fill_between(exts,f2yrs/N.sqrt(5),f2yrs/5,
                  color='lightgrey')

ax.semilogy(exts,f10yrs,**kwargs)

lower_ax.plot(exts,f2yrs/f10yrs,**kwargs)

lower_ax.fill_between(exts,N.sqrt(5),5, color='lightgrey')

# add degrees to the x axis
from uw.like.roi_plotting import DegreesFormatter
ax.xaxis.set_major_formatter(DegreesFormatter)

ax.set_xlim(0.1,2)

# Use text object for easier alignment
ax.text(-0.1, 0.5, 'Flux ($\mathrm{ph}\ \mathrm{cm}^{-2}\mathrm{s}^{-1}$)', transform=ax.transAxes, rotation=90,
        ha='right', va='center')

ax.get_xaxis().set_visible(False)

ax.set_ylim(7e-11,2e-8)

ax.set_yscale('log')


lower_ax.text(-0.1, 0.5, r'$\textrm{F}_\textrm{2yr}/\textrm{F}_\textrm{10yr}$', transform=lower_ax.transAxes, rotation=90,
        ha='right', va='center')

lower_ax.set_ylim(N.sqrt(5)-0.5,5+0.5)
lower_ax.set_xlabel('Extension')

lower_ax.set_xticks([0.1,0.5,1,1.5,2])
lower_ax.set_yticks([2,3,4,5])


savefig('extension_sensitivity.eps')
savefig('extension_sensitivity.pdf')

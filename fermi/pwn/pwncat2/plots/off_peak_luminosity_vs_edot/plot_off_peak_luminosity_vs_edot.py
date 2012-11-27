import pylab as P

import numpy as np

from lande.utilities.plotting import plot_points
from lande.utilities import pubplot
from lande.fermi.pipeline.pwncat2.interp.bigfile import PulsarCatalogLoader

pubplot.set_latex_defaults()

bw = pubplot.get_bw()

cat=PulsarCatalogLoader(
    bigfile_filename='$lat2pc/BigFile/Pulsars_BigFile_v20121108102909.fits',
    off_peak_auxiliary_filename='$lat2pc/OffPeak/tables/off_peak_auxiliary_table.fits')

psrlist = cat.get_off_peak_psrlist()


fig = P.figure(None,(4,4))
axes = fig.add_subplot(111)

axes.set_xscale("log")
axes.set_yscale("log")


classification=np.empty_like(psrlist,dtype=object)
Edot=np.empty_like(psrlist,dtype=float)
luminosity=np.empty_like(psrlist,dtype=float)
luminosity_lower_error=np.empty_like(psrlist,dtype=float)
luminosity_upper_error=np.empty_like(psrlist,dtype=float)
luminosity_ul=np.empty_like(psrlist,dtype=float)
luminosity_significant=np.empty_like(psrlist,dtype=bool)

for i,psr in enumerate(psrlist):
 
    classification[i]=cat.get_off_peak_classification(psr)


    Edot[i]=cat.get_edot(psr)

    y, y_lower_err, y_upper_err, y_ul, significant  = cat.get_luminosity(psr)
    luminosity[i]=y
    luminosity_lower_error[i]=y_lower_err
    luminosity_upper_error[i]=y_upper_err
    luminosity_ul[i]=y_ul
    luminosity_significant[i]=significant

def plot(cut, **kwargs):
    # plot PWN
    print 'kwargs',kwargs
    plot_points(Edot[cut], luminosity[cut],
                xlo=None, xhi=None,
                y_lower_err=luminosity_lower_error[cut],
                y_upper_err=luminosity_upper_error[cut],
                y_ul=luminosity_ul[cut], significant=luminosity_significant[cut],
                axes=axes, **kwargs)

blue = 'blue' if not bw else 'black'
red = 'red' if not bw else 'black'

axes.plot([1e33,1e39],[1e33,1e39], color=blue, zorder=1)
axes.plot([1e33,1e39],[0.1*1e33,0.1*1e39], dashes=[5,3], color=blue, zorder=1)
axes.plot([1e33,1e39],[0.01*1e33,0.01*1e39], dashes=[2,2], color=blue, zorder=1)

plot((classification!='Confused')&(classification!='Pulsar')&(classification!='PWN'),
     marker='None', markersize=5, color='gray', zorder=1.5)
plot(classification=='Confused', color='black', marker='o', markerfacecolor='none', markersize=5, zorder=5)
plot(classification=='Pulsar', color=blue, marker='s', markersize=5, markeredgecolor=blue, markerfacecolor='none', zorder=6)
plot(classification=='PWN', color=red, marker='*', markersize=10, markerfacecolor=red, markeredgecolor=red, zorder=7)

for psr_name,print_name,kwargs in [
    ['J0534+2200', 'Crab Nebula', dict(horizontalalignment='right', verticalalignment='bottom', xytext=(10,10), textcoords='offset points')],
    ['J0835-4510', 'Vela X', dict(horizontalalignment='middle', verticalalignment='top', xytext=(-20,-15), textcoords='offset points')],
    ['J1513-5908', 'MSH 15-52', dict(horizontalalignment='left', verticalalignment='bottom', xytext=(-2,-20), textcoords='offset points')],
    ['J0205+6449', 'J0205', dict(horizontalalignment='left', verticalalignment='bottom', xytext=(3,-10), textcoords='offset points')],
]:
    cut=np.where(psrlist==psr_name)[0][0]
    axes.annotate(print_name,
                  xy=[Edot[cut], luminosity[cut]], xycoords='data',
                  color=red, 
                  zorder=8,
                  **kwargs)



axes.set_xlim(1e33,1e39)
axes.set_ylim(1e31,1e37)

axes.set_xlabel('$\dot E$ [erg s$^{-1}$]')
axes.set_ylabel(r'$L_\mathrm{off\,peak}$ [erg s$^{-1}$]')

fig.tight_layout()

pubplot.save('off_peak_luminosity_vs_edot')

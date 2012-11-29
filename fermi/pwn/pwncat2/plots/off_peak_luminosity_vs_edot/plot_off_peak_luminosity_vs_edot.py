import pylab as P

import numpy as np

from lande.utilities.plotting import plot_points
from lande.utilities import pubplot
from lande.fermi.pipeline.pwncat2.interp.bigfile import PulsarCatalogLoader

pubplot.set_latex_defaults()

bw = pubplot.get_bw()

cat=PulsarCatalogLoader(
    bigfile_filename='$lat2pc/BigFile/Pulsars_BigFile_v20121127171828.fits',
    off_peak_auxiliary_filename='$lat2pc/OffPeak/tables/off_peak_auxiliary_table.fits')

psrlist = cat.get_off_peak_psrlist()


fig = P.figure(None,(6,6))
axes = fig.add_subplot(111)

axes.set_xscale("log")
axes.set_yscale("log")


classification=np.empty_like(psrlist,dtype=object)
Edot=np.empty_like(psrlist,dtype=float)
luminosity=np.empty_like(psrlist,dtype=float)
luminosity_error_statistical=np.empty_like(psrlist,dtype=float)
luminosity_lower_error_systematic=np.empty_like(psrlist,dtype=float)
luminosity_upper_error_systematic=np.empty_like(psrlist,dtype=float)
luminosity_ul=np.empty_like(psrlist,dtype=float)
luminosity_significant=np.empty_like(psrlist,dtype=bool)

for i,psr in enumerate(psrlist):
 
    classification[i]=cat.get_off_peak_classification(psr)


    Edot[i]=cat.get_edot(psr)

    y, y_err_stat, y_lower_err_sys, y_upper_err_sys, y_ul, significant  = cat.get_luminosity(psr)
    luminosity[i]=y
    #luminosity_lower_error[i]=y_lower_err
    #luminosity_upper_error[i]=y_upper_err
    luminosity_error_statistical[i]=y_err_stat
    luminosity_lower_error_systematic[i]=y_lower_err_sys
    luminosity_upper_error_systematic[i]=y_upper_err_sys
    luminosity_ul[i]=y_ul
    luminosity_significant[i]=significant

def plot_stat(cut, **kwargs):
    # plot PWN
    print 'kwargs',kwargs
    plot_points(Edot[cut], luminosity[cut],
                xlo=None, xhi=None,
                y_lower_err=luminosity_error_statistical[cut],
                y_upper_err=luminosity_error_statistical[cut],
                y_ul=luminosity_ul[cut], significant=luminosity_significant[cut],
                axes=axes, **kwargs)

def plot_sys(cut, **kwargs):
    # plot PWN
    print 'sys: kwargs',kwargs
    print luminosity[cut],luminosity_lower_error_systematic[cut],luminosity_upper_error_systematic[cut],
    plot_points(Edot[cut], luminosity[cut],
                xlo=None, xhi=None,
                y_lower_err=luminosity_lower_error_systematic[cut],
                y_upper_err=luminosity_upper_error_systematic[cut],
                y_ul=luminosity_ul[cut], significant=luminosity_significant[cut],
                axes=axes, **kwargs)

black = 'black'
blue = 'blue' if not bw else 'black'
red = 'red' if not bw else 'black'
green = 'green' if not bw else 'black'

axes.plot([1e33,1e39],[1e33,1e39], color=black, zorder=1)
axes.plot([1e33,1e39],[0.1*1e33,0.1*1e39], dashes=[5,3], color=black, zorder=1)
axes.plot([1e33,1e39],[0.01*1e33,0.01*1e39], dashes=[2,2], color=black, zorder=1)

capsize=3

plot_stat((classification!='U')&(classification!='M')&(classification!='M*')&(classification!='W'),
          marker='None', markersize=5, color='gray', zorder=1.5, elinewidth=0.5)

assert np.all(luminosity_significant[classification=='U']==True)
plot_sys(classification=='U', color=black, marker='None', zorder=5-0.1, elinewidth=0.25, capsize=capsize)
plot_stat(classification=='U', color=green, marker='o', markeredgecolor=green, markerfacecolor=green, markersize=5, zorder=5, elinewidth=1.5, capsize=capsize)

plot_sys( ((classification=='M')|(classification=='M*'))&(luminosity_significant==True), color=black, marker='None', zorder=6-0.1, elinewidth=0.25, capsize=capsize)
plot_stat(((classification=='M')|(classification=='M*'))&(luminosity_significant==True), color=blue, marker='s', markerfacecolor=blue, markersize=5, markeredgecolor=blue, zorder=6, elinewidth=1.5, capsize=capsize)
plot_stat(((classification=='M')|(classification=='M*'))&(luminosity_significant==False), color=blue, marker='s', markerfacecolor=blue, markersize=5, markeredgecolor=blue, zorder=6, elinewidth=1.5, capsize=0)

assert np.all(luminosity_significant[classification=='U']==True)
plot_sys(classification=='W', color=black, marker='None', zorder=7-0.1, capsize=capsize, elinewidth=0.25)
plot_stat(classification=='W', color=red, marker='*', markersize=8, 
          markerfacecolor=red, markeredgecolor=red, zorder=7, capsize=capsize, elinewidth=1.5)

for psr_name,print_name,kwargs in [
    ['J0534+2200', 'Crab Nebula', dict(horizontalalignment='right', verticalalignment='bottom', xytext=(10,20), textcoords='offset points')],
    ['J0835-4510', 'Vela X', dict(horizontalalignment='middle', verticalalignment='top', xytext=(-25,-10), textcoords='offset points')],
    ['J1513-5908', 'MSH 15-52', dict(horizontalalignment='left', verticalalignment='bottom', xytext=(10,0), textcoords='offset points')],
    ['J0205+6449', 'J0205', dict(horizontalalignment='left', verticalalignment='bottom', xytext=(8,-5), textcoords='offset points')],
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

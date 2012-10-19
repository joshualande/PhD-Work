import pylab as P
import numpy as np

from lande.utilities import pubplot
from lande.fermi.pipeline.pwncat2.interp.bigfile import PulsarCatalogLoader

pubplot.set_latex_defaults()

bw = pubplot.get_bw()


fig = P.figure(None,(6,6))
axes = fig.add_subplot(111)

axes.set_xscale("log")
axes.set_yscale("log")

cat=PulsarCatalogLoader(
    bigfile_filename='$lat2pc/BigFile/Pulsars_BigFile_v20121002103223.fits',
    off_peak_auxiliary_filename='$lat2pc/OffPeak/tables/off_peak_auxiliary_table.fits')
bigfile_fits = cat.bigfile_fits

psrlist=bigfile_fits.data['PSRJ']
Edot=bigfile_fits.data['Edot'] # erg/s
age=bigfile_fits.data['Age'] # years

dist = bigfile_fits.data['DIST1'] # kpc
#dist = bigfile_fits.data['DPSR_1'] # kpc
#dist=np.asarray([float(i) if i != '' and i[0]!='<' else np.nan for i in dist],dtype=float)

off_peak_psrlist=cat.get_off_peak_psrlist()
classification = np.asarray([ cat.get_off_peak_classification(i) if i in off_peak_psrlist else 'Non_Detected' for i in psrlist])

blue = 'blue' if not bw else 'grey'
red = 'red' if not bw else 'grey'

def plot(cut, **kwargs):
    axes.plot(age[cut],Edot[cut]/dist[cut]**2,'.', **kwargs)

plot(classification=='Non_Detected',color='lightgrey', markersize=10)
plot((classification=='Upper_Limit')|(classification=='Confused'),color='black', markersize=10)
plot(classification=='Pulsar',color=blue, markersize=5, marker='s', markeredgecolor=blue)
plot(classification=='PWN',color=red, markersize=10, marker='*', markeredgecolor=red)

axes.set_xlabel('Age [yr]')
axes.set_ylabel('$\dot E/d^2$ [erg s$^{-1}$ kpc$^{-2}$]')



for psr_name,print_name,kwargs in [
    ['J0534+2200', 'Crab Nebula', dict(horizontalalignment='center', verticalalignment='bottom', xytext=(0,10), textcoords='offset points')],
    ['J0835-4510', 'Vela X', dict(horizontalalignment='left', verticalalignment='middle', xytext=(5,0), textcoords='offset points')],
    ['J1513-5908', 'MSH 15-52', dict(horizontalalignment='right', verticalalignment='middle', xytext=(15,10), textcoords='offset points')],
    ['J0205+6449', 'J0205', dict(horizontalalignment='center', verticalalignment='bottom', xytext=(5,15), textcoords='offset points')],
    ['J1357-6429', 'HESS J1356', dict(horizontalalignment='right', verticalalignment='top', xytext=(5,-10), textcoords='offset points')],
]:
    cut=np.where(psrlist==psr_name)[0][0]
    axes.annotate(print_name,
                  xy=[age[cut],Edot[cut]/dist[cut]**2], xycoords='data',
                  color=red, **kwargs)

pubplot.save('off_peak_edot_d2_vs_age')

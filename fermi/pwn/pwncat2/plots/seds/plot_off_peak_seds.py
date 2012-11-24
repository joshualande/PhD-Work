import math


import pylab as P
import yaml
from os.path import join, expandvars,exists
from matplotlib.offsetbox import AnchoredText
from mpl_toolkits.axes_grid.axes_grid import Grid

from lande.fermi.likelihood.specplot import SpectralAxes,SpectrumPlotter
from lande.utilities.plotting import fix_yaxesgrid, label_axes
from lande.utilities import pubplot
from lande.pysed import units

from lande.fermi.spectra.sed import SED

from lande.fermi.pipeline.pwncat2.interp.loader import PWNResultsLoader
from lande.fermi.pipeline.pwncat2.interp.classify import PWNManualClassifier


pubplot.set_latex_defaults()

bw = pubplot.get_bw()

base='$pwnpipeline/v35/'
fitdir=expandvars(join(base,'analysis'))

loader = PWNResultsLoader(
    pwndata='$pwndata/pwncat2_data_lande.yaml',
    fitdir='$pwnpipeline/v35/analysis',
    #phase_shift='/u/gl/kerrm/pulsar/share/python/checklist.py'
    )

classifier = PWNManualClassifier(loader=loader, 
                                 pwn_classification='$pwnclassify/manual_classifications.yaml')



cutoff_candidates = ['PSRJ0007+7303',
                     'PSRJ0205+6449', 
                     'PSRJ1410-6132',
                     'PSRJ1747-2958',
                     'PSRJ2021+4026', 
                     'PSRJ2124-3358']

binning = '4bpd'

hypothesis='point'


ncols,nrows = 2,3

fig = P.figure(None,(6,6))
grid = Grid(fig, 111, nrows_ncols = (nrows, ncols), 
            axes_pad=0.0,
            axes_class=(SpectralAxes, dict()),
           )


for i,pwn in enumerate(cutoff_candidates):
    print i,pwn

    axes=grid[i]


    r = classifier.get_results(pwn)
    spectrum = r['spectrum']
    sed = r['sed_4bpd']

    s = SED(sed)
    s.plot_points(axes=axes, zorder=2.1)

    sp = SpectrumPlotter(axes=axes)
    sp.plot(spectrum, autoscale=False, color='red', zorder=1.9)

label_axes(grid)

grid[0].set_ylabel('')
grid[4].set_ylabel('')


for i in range(nrows*ncols):
    axes=grid[i]
    #axes.set_xlim_units(10**2*units.MeV,10**5.5*units.MeV)
    axes.set_xlim(10**2,10**5.5)
    #axes.set_ylim_units(1e-13*units.erg/units.cm**2/units.s,1e-9*units.erg/units.cm**2/units.s)
    axes.set_ylim(1e-13,1e-9)
fix_yaxesgrid(grid)

pubplot.save(join(base,'plots','off_peak_seds'))

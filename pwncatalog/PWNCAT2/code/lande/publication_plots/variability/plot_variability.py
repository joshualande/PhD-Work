from os.path import join, expandvars

import yaml

import pylab as P
import numpy as np

from scipy import stats

from lande.utilities import pubplot

pubplot.set_latex_defaults()

outdir = '$pwndata/spectral/v24/plots'

bw = pubplot.get_bw()

d=yaml.load(open(expandvars(join(outdir,'ts_var.yaml'))))
a=np.asarray
ts_var = a(d['ts_var'])
ts_point = a(d['ts_point'])


print np.min(ts_var), np.max(ts_var)
print sorted(ts_var)

fig=P.figure(figsize=(6.5,6))
axes = fig.add_subplot(111)


# Clip out crab, which has way too large TS_var
xmin = 0
xmax = np.max(ts_var[ts_var<200]) + 10

#nbins = 30
nbins = 20
bins = np.linspace(xmin, xmax, nbins + 1)

TS_CUTOFF=4
print 'num significiant',sum(ts_point>=TS_CUTOFF)
print 'num not significiant',sum(ts_point<TS_CUTOFF)
axes.hist(ts_var[ts_point>=TS_CUTOFF], bins=bins, histtype='step', color='black')
axes.hist(ts_var[ts_point<TS_CUTOFF], bins=bins, histtype='step', color='blue')



lower,upper=list(axes.xaxis.get_view_interval())
x=np.linspace(lower,upper,10000)
months=36
chidist = stats.chi2(months-1)
y=chidist.pdf(x)
# Normalize the distribution
y*=sum(ts_point>=TS_CUTOFF)*(bins[1]-bins[0])
axes.plot(x,y, dashes=[5,2], color='red' if not bw else 'black')

axes.set_xlabel(r'$\mathrm{TS}_\mathrm{var}$')
axes.set_ylabel(r'Number')

pubplot.save(join(outdir,'variability'))

import plot_helper

import yaml

import pylab as P
import numpy as np

from scipy import stats

bw = plot_helper.get_bw()

d=yaml.load(open('ts_var.yaml'))
a=np.asarray
ts_var = a(d['ts_var'])
ts_point = a(d['ts_point'])


print np.min(ts_var), np.max(ts_var)
print sorted(ts_var)

fig=P.figure(figsize=(6.5,6))
axes = fig.add_subplot(111)


# Clip out crab, which has way too large TS_var
xmin = 0
xmax = np.max(ts_var[ts_var<400]) + 10

#nbins = 30
nbins = 20
bins = np.linspace(xmin, xmax, nbins + 1)

print 'num significiant',sum(ts_point>=25)
print 'num not significiant',sum(ts_point<25)
axes.hist(ts_var[ts_point>=25], bins=bins, histtype='step', color='black')
axes.hist(ts_var[ts_point<25], bins=bins, histtype='step', color='blue')



lower,upper=list(axes.xaxis.get_view_interval())
x=np.linspace(lower,upper,10000)
months=36
chidist = stats.chi2(months-1)
y=chidist.pdf(x)
# Normalize the distribution
y*=sum(ts_point>=25)*(bins[1]-bins[0])
axes.plot(x,y, dashes=[5,2], color='red' if not bw else 'black')

axes.set_xlabel(r'$\mathrm{TS}_\mathrm{var}$')
axes.set_ylabel(r'Number')

plot_helper.save('variability')

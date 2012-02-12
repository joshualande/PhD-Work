import plot_helper 

import yaml
from os.path import expandvars, join, exists

import pylab as P
import numpy as np

from scipy import stats

bw = plot_helper.get_bw()

# useful discussion of TSvar
#   https://confluence.slac.stanford.edu/display/SCIGRPS/How+to+-+Variability+test

pwnlist = yaml.load(open(expandvars('$pwncode/pwndata/pwncat2_data_lande.yaml')))

def get_ts_var():
    folder = '/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/spectral/v10/variability/v3'

    ts_var = []
    for pwn in pwnlist.keys():

        results = join(folder,pwn,'results_%s.yaml' % pwn)

        assert exists(results)

        f=yaml.load(open(results))

        ts_var.append(f['TS_var']['gtlike'])

    return ts_var

#def get_ts_point():
#    folder = '/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/spectral/v10/analysis_plots/'
#
#    ts_point = []
#    for pwn in pwnlist.keys():
#
#        results = join(folder,pwn,'results_%s.yaml' % pwn)
#
#        assert exists(results)
#
#        f=yaml.load(open(results))
#        print pwn,f['at_pulsar']['gtlike'],f['at_pulsar']['gtlike']['TS']
#
#        ts_point.append(f['at_pulsar']['gtlike']['TS'])
#
#ts_point = get_ts_point()
#ts_point = np.asarray(ts)
#open('ts_var.yaml','w').write(yaml.dump(ts_point,ts_var))

ts_var = get_ts_var()
#ts_var=yaml.load(open('ts_var.yaml'))
ts_var = np.asarray(ts_var)


print np.min(ts_var), np.max(ts_var)

fig=P.figure(figsize=(6.5,6))
axes = fig.add_subplot(111)


# Clip out crab, which has way too large TS_var
xmin = 0
xmax = np.max(ts_var[ts_var<400]) + 10

#nbins = 30
nbins = 10
bins = np.linspace(xmin, xmax, nbins + 1)

axes.hist(ts_var, bins=bins, histtype='step', color='black')



lower,upper=list(axes.xaxis.get_view_interval())
x=np.linspace(lower,upper,10000)
months=36
chidist = stats.chi2(months-1)
y=chidist.pdf(x)
# Normalize the distribution
y*=len(ts_var)*(bins[1]-bins[0])
axes.plot(x,y, dashes=[5,2], color='red' if not bw else 'black')

axes.set_xlabel(r'$\mathrm{TS}_\mathrm{var}$')
axes.set_ylabel(r'Number')

plot_helper.save('variability')

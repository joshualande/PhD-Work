import pylab as P
import yaml
from os.path import join as j
from lande_plotting import plot_gtlike_cutoff_test

fitdir='/nfs/slac/g/ki/ki03/lande/pwncatalog/PWNCAT2/analyze_psr/v6/analysis_no_plots/'

cutoff_candidates = ['PSRJ0034-0534', 
                     'PSRJ0633+1746', 
                     'PSRJ1813-1246', 
                     'PSRJ1836+5925', 
                     'PSRJ2021+4026', 
                     'PSRJ2055+2539', 
                     'PSRJ2124-3358']

pwn = cutoff_candidates[1]

f = j(fitdir,pwn,'results_%s.yaml' % pwn)
print f

binning = '4bpd'

r=yaml.load(open(f))
hypothesis='at_pulsar'

print r[hypothesis]
cutoff_results=r[hypothesis]['gtlike']['test_cutoff']
sed=j(fitdir,pwn,'seds','sed_gtlike_%s_%s_%s.yaml' % (binning, hypothesis, pwn))

fig = P.figure(None,(6,6))
axes = P.gca()

plot_gtlike_cutoff_test(cutoff_results=cutoff_results,sed_results=sed, plot_kwargs=dict(axes=axes))


P.savefig('cutoff_test.pdf')


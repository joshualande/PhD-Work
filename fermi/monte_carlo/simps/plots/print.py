import numpy as np

from lande.utilities.save import loaddict

#results = loaddict('$simpsdata/v7/merged.hdf5')
#results = loaddict('$simpsdata/v6/merged.hdf5')
#results = loaddict('$simpsdata/v9/merged.hdf5')
results = loaddict('$simpsdata/v10/merged.hdf5')

flux_gtlike = np.asarray(results['flux_gtlike'])
flux_gtlike_err = np.asarray(results['flux_gtlike_err'])
flux_pointlike = np.asarray(results['flux_pointlike'])
flux_pointlike_err = np.asarray(results['flux_pointlike_err'])

flux_mc = np.asarray(results['flux_mc'])
glon = np.asarray(results['glon'])
glat = np.asarray(results['glat'])
ra = np.asarray(results['ra'])
dec = np.asarray(results['dec'])
i = np.asarray(results['i'])
phibins = np.asarray(results['phibins'])
position = np.asarray(results['position'])

pull_gtlike = (flux_gtlike-flux_mc)/flux_gtlike_err
perr_gtlike = (flux_gtlike-flux_mc)/flux_mc

pull_pointlike = (flux_pointlike-flux_mc)/flux_pointlike_err
perr_pointlike = (flux_pointlike-flux_mc)/flux_mc

index = np.argsort(np.abs(perr_gtlike))
#index = np.argsort(np.abs(perr_pointlike))
def f(x): 
    x=x[index]
    return x[phibins[index]==9]

glon = f(glon)
glat = f(glat)
ra = f(ra)
dec = f(dec)
pull_gtlike = f(pull_gtlike)
perr_gtlike = f(perr_gtlike)
pull_pointlike = f(pull_pointlike)
perr_pointlike = f(perr_pointlike)
position = f(position)
i = f(i)

for a in zip(i,glon,glat,ra,dec,pull_gtlike, perr_gtlike, pull_pointlike, perr_pointlike, position):
    fmt = lambda a: ' '.join(map(lambda i: '%10.4f' % i if isinstance(i,float) else '%10s' % i,a))
    print fmt(a)

print 'average %error gtlike',np.average(np.abs(perr_gtlike)), 'n', len(perr_gtlike)
print 'average %error pointlike',np.average(np.abs(perr_pointlike)), 'n', len(perr_pointlike)

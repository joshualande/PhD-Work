import numpy as np

from lande.utilities.save import loaddict
from lande.utilities.arrays import almost_equal

#results = loaddict('$simsrcdata/v7/merged.hdf5')
#results = loaddict('$simsrcdata/v6/merged.hdf5')
#results = loaddict('$simsrcdata/v9/merged.hdf5')
#results = loaddict('$simsrcdata/v10/merged.hdf5')

#results = loaddict('$simsrcdata/v11/sim_flux_1e-06_position_allsky_phibins_0_spatial_extended_emin_100_emax_100000_time_2fgl/merged.hdf5')

#results = loaddict('$simsrcdata/v11/sim_flux_1e-06_position_allsky_phibins_0_spatial_point_emin_100_emax_100000_time_2years/merged.hdf5')

#results = loaddict('$simsrcdata/v11/sim_flux_1e-06_position_allsky_phibins_0_spatial_extended_emin_100_emax_100000_time_2years/merged.hdf5')
#results = loaddict('$simsrcdata/v11/sim_flux_1e-06_position_allsky_phibins_0_spatial_point_emin_100_emax_100000_time_2fgl/merged.hdf5')
#results = loaddict('$simsrcdata/v12/merged.hdf5')

#results = loaddict('$simsrcdata/v14/merged.hdf5')
#results = loaddict('$simsrcdata/v17/merged.hdf5')

#results = loaddict('$simsrcdata/v18/merged.hdf5')
#results = loaddict('$simsrcdata/v19/merged.hdf5')
#results = loaddict('$simsrcdata/v20/merged.hdf5')
#results = loaddict('$simsrcdata/v21/merged.hdf5')
results = loaddict('$simsrcdata/v22/merged.hdf5')

print results.keys()
print len(results['flux_gtlike'])

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
time = np.asarray(results['time'])
phibins = np.asarray(results['phibins'])
position = np.asarray(results['position'])
spatial = np.asarray(results['spatial'])
#binsz = np.asarray(results['binsz'])
#rfactor = np.asarray(results['rfactor'])

#cut = (phibins == 0 ) & (time == '2fgl')
#cut = (phibins == 0 ) & (time == '2years')
#cut = (phibins == 5 ) & (time == '2fgl')
#cut = (phibins == 5 ) & (time == '2years')
#cut = (phibins == 9 ) & (time == '2fgl')

#cut = (phibins == 0 ) & (time == '2fgl') & (spatial == 'point')
#cut = (phibins == 9 ) & (time == '2fgl') & (spatial == 'disk')
#cut = (phibins == 9 ) & (time == '2fgl') & (spatial == 'w44')

#cut = (phibins == 9 ) & (spatial == 'point')
#cut = (phibins == 9 ) & (spatial == 'disk')
cut = (phibins == 9 ) & (spatial == 'w44')

#cut = np.ones_like(i).astype(bool)
#cut = almost_equal(binsz,0.1) & almost_equal(rfactor,2)
#cut = almost_equal(binsz,0.025) & almost_equal(rfactor,2)
#cut = almost_equal(binsz,0.025) & almost_equal(rfactor,8)
#cut = almost_equal(binsz,0.025) & almost_equal(rfactor,2)

pull_gtlike = (flux_gtlike-flux_mc)/flux_gtlike_err
perr_gtlike = (flux_gtlike-flux_mc)/flux_mc

pull_pointlike = (flux_pointlike-flux_mc)/flux_pointlike_err
perr_pointlike = (flux_pointlike-flux_mc)/flux_mc

index = np.argsort(np.abs(perr_gtlike))
#index = np.argsort(np.abs(perr_pointlike))
def f(x): 
    x=x[index]
    return x[cut[index]]

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

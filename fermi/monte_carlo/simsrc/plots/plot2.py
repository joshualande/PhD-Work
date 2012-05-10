from lande.utilities.save import loaddict
import numpy as np
import pylab as P

from lande.utilities.arrays import almost_equal

#r = loaddict('$simsrcdata/v22/merged.hdf5')
#r = loaddict('$simsrcdata/v21/merged.hdf5')
r = loaddict('$simsrcdata/v19/merged.hdf5')

ax1=P.subplot(211)
ax2=P.subplot(212)

flux=np.asarray(r['flux_gtlike'])
flux_mc=np.asarray(r['flux_mc'])
flux_err=np.asarray(r['flux_gtlike_err'])
spatial=np.asarray(r['spatial'])
#binsz=np.asarray(r['binsz'])
#rfactor=np.asarray(r['rfactor'])

#for label,cut in [('binsz=0.1 & rfactor=2',(almost_equal(binsz,0.1)&almost_equal(rfactor,2))),
#                  ('binsz=0.05 & rfactor=4',(almost_equal(binsz,0.05)&almost_equal(rfactor,4))),
#                  ('binsz=0.025 & rfactor=8',(almost_equal(binsz,0.025)&almost_equal(rfactor,8)))]:
for label in ['?']:
    cut = spatial == 'w44'

    #P.hist((flux-flux_mc)/flux_err)
    print label
    ax1.hist((flux[cut]-flux_mc[cut])/flux_mc[cut], label=label, histtype='step')
    #ax1.hist((flux[cut]-flux_mc[cut])/flux_err[cut], label=label, histtype='step')

#P.hist(flux)
#P.axvline(flux_mc[0])

    index=np.asarray(r['index_gtlike'])
    index_mc=np.asarray(r['index_mc'])
    index_err=np.asarray(r['index_gtlike_err'])
    #ax2.hist((index[cut]-index_mc[cut])/index_mc[cut], histtype='step', label=label)
    ax2.hist((index[cut]-index_mc[cut])/index_err[cut], histtype='step', label=label)

ax1.legend()
ax2.legend()

P.savefig('plot2.pdf')

from lande.utilities.simtools import SimMerger
keys = dict(TS_point=['point', 'TS'],
            TS_ext=['extended','TS_ext'],
            flux_mc=['mc','flux','flux'],
            index_mc=['mc','model','Index'],
            glon=['mc','position','gal',0],
            glat=['mc','position','gal',1])
m = SimMerger(savedir='$tsext_plane_data/v12', keys=keys)
m.save('$tsext_plane_data/v12/merged.hdf5')

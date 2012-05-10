from lande.utilities.simtools import SimMerger

keys = dict(
    flux_gtlike=['gtlike', 'fit', 'flux', 'flux'],
    flux_gtlike_err=['gtlike', 'fit', 'flux', 'flux_err'],
    flux_pointlike=['pointlike', 'fit', 'flux', 'flux'],
    flux_pointlike_err=['pointlike', 'fit', 'flux', 'flux_err'],
    flux_mc=['gtlike', 'mc', 'flux', 'flux'],

    index_gtlike=['gtlike', 'fit', 'model', 'Index'],
    index_gtlike_err=['gtlike', 'fit', 'model', 'Index_err'],
    index_pointlike=['pointlike', 'fit', 'model', 'Index'],
    index_pointlike_err=['pointlike', 'fit', 'model', 'Index_err'],
    index_mc=['gtlike', 'mc', 'model', 'Index'],

    glon=['pointlike', 'mc', 'position', 'gal', 0],
    glat=['pointlike', 'mc', 'position', 'gal', 1],
    ra=['pointlike', 'mc', 'position', 'equ', 0],
    dec=['pointlike', 'mc', 'position', 'equ', 1],
    i=['i'],
    emin=['emin'],
    emax=['emax'],
    time=['time'],
    phibins=['phibins'],
    spatial=['spatial'],
    position=['position'],
    
    binsz=['binsz'],
    rfactor=['rfactor'],
    )

m = SimMerger(savedir='$simsrcdata/v22/', keys=keys)
m.save('$simsrcdata/v22/merged.hdf5')

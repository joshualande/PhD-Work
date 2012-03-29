from lande.utilities.simtools import SimMerger

keys = dict(
    flux_gtlike=['gtlike', 'fit', 'flux', 'flux'],
    flux_gtlike_err=['gtlike', 'fit', 'flux', 'flux_err'],
    flux_pointlike=['pointlike', 'fit', 'flux', 'flux'],
    flux_pointlike_err=['pointlike', 'fit', 'flux', 'flux_err'],
    flux_mc=['gtlike', 'mc', 'flux', 'flux'],
    glon=['pointlike', 'mc', 'position', 'gal', 0],
    glat=['pointlike', 'mc', 'position', 'gal', 1],
    ra=['pointlike', 'mc', 'position', 'equ', 0],
    dec=['pointlike', 'mc', 'position', 'equ', 1],
    i=['i'],
    emin=['emin'],
    emax=['emax'],
    time=['time'],
    phibins=['phibins'],
    position=['position'],)

m = SimMerger(savedir='$simpsdata/v10/', keys=keys)
m.save('$simpsdata/v10/merged.hdf5')

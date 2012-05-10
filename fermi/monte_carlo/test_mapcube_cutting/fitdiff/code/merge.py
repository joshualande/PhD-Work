from lande.utilities.simtools import SimMerger

keys = dict(
    difftype=['difftype'],
    position=['position'],
    glon=['roi_dir','gal',0],
    glat=['roi_dir','gal',1],
    emin=['emin'],
    emax=['emax'],

    pointlike_norm=['pointlike', 'fit', 
                    ['ring_2year_P76_v0.fits', 'isotrop_2year_P76_source_v0.txt', 'Sreekumar Isotropic','Norm'],
                    ['Scale','Norm']],

    pointlike_norm_err=['pointlike','fit', 
                        ['ring_2year_P76_v0.fits','isotrop_2year_P76_source_v0.txt','Sreekumar Isotropic'],
                        ['Scale_err','Norm_err']],

    pointlike_norm_mc=['pointlike','mc', 
                       ['ring_2year_P76_v0.fits','isotrop_2year_P76_source_v0.txt','Sreekumar Isotropic'],
                       ['Scale','Norm']],

    gtlike_norm=['gtlike','fit', 
                 ['ring_2year_P76_v0.fits', 'isotrop_2year_P76_source_v0.txt', 'Sreekumar Isotropic','Norm'],
                 ['Value','Normalization','Prefactor']],

    gtlike_norm_err=['gtlike','fit',
                     ['ring_2year_P76_v0.fits', 'isotrop_2year_P76_source_v0.txt', 'Sreekumar Isotropic','Norm'],
                     ['Value_err','Normalization_err','Prefactor_err']],

    gtlike_norm_mc=['gtlike','mc',
                    ['ring_2year_P76_v0.fits', 'isotrop_2year_P76_source_v0.txt', 'Sreekumar Isotropic','Norm'],
                    ['Value','Normalization','Prefactor']],
    )

m = SimMerger(savedir='$fitdiffdata/v11/', keys=keys)
m.save('$fitdiffdata/v11/merged.hdf5')

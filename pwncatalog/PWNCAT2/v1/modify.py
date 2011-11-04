
def modify_roi(name,roi):
    """ For each modification, add some justifcaiton for why
        this needs to be done + where you did the analysis
        which convinced you we need to do this to the region. """

    # Examples of modifying an ROI (Nov, 4, 2011 - Joshua Lande):
    #   Modify Position:
    #   >> roi.modify(which='PSRNAME', skydir=SkyDir(...))
    # 
    #   Modify Spectrum
    #   >> from uw.like.Models import PowerLaw
    #   >> roi.modify(which='PSRNAME', model=PowerLaw(norm=1e-11, index=2), keep_old_flux=True)
    #   
    #  Freeze ALL spectral parameters:
    #  >> roi.modify(which='PSRNAME', free=False)
    # 
    #  Freeze only one spectral parameter
    #  >> roi.freeze(which='PSRNAME', free=[True, False]) 
    #  (but, you have to know how many parameters there are in the model)!
    # 
    #  Modify the extension
    #  >> roi.modify(which='PSRNAME', spatial_model=Disk(sigma=0.2, l=347, b=0.1), keep_old_center=False)
    #  >> roi.modify(which='PSRNAME', sigma=0.2)

    print 'Modifying source %s' % name

    # first, modify known pulsars to their fit values from PWNCat1
    for psr,flux,index in [
        ['PSRJ0034-0534',   17.26e-9, 2.27, ],
        ['PSRJ0534+2200',  980.00e-9, 2.15, ],
        ['PSRJ0633+1746', 1115.54e-9, 2.24, ],
        ['PSRJ0835-4510',  405.44e-9, 2.30, ],
        ['PSRJ1023-5746',    1.33e-9, 1.05, ],
        ['PSRJ1813-1246',  295.55e-9, 2.65, ],
        ['PSRJ1836+5925',   579.6e-9, 2.07, ],
        ['PSRJ2021+4026', 1603.00e-9, 2.36, ],
        ['PSRJ2055+2539',   38.41e-9, 2.51, ],
        ['PSRJ2124-3358',   22.78e-9, 2.06, ]]:

        if name == psr:
            model=roi.get_model(which=name)
            model['index']=index
            model.set_flux(flux,emin=100,emax=100000)
            roi.modify(which=name,model=model)

    if name=='PSRJ0835-4510':
        # Vela X is already include in 2FGL and needs to be pruned
        # out of the background model - Nov, 4, 2011 Joshua Lande
        print 'Deleting Vela X from background model!'
        roi.del_source('VelaX')






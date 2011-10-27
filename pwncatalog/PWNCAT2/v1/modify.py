
def modify_roi(name,roi):
    """ For each modification, add some justifcaiton for why
        this needs to be done + where you did the analysis
        which convinced you we need to do this to the region. """

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
            # these modificaitons come from PWN catalog 1
            model=roi.get_model(which=name)
            model['index']=index
            model.set_flux(flux,emin=100,emax=100000)
            roi.modify(which=name,model=model)

    # Here, could modify crab to be a BrokenPowerlaw


    if name=='PSRJ0835-4510':
        print 'Deleting VelaX from background model!'
        roi.del_source('VelaX')

""" Examples of modifying an ROI (Nov, 4, 2011 - Joshua Lande):
    Modify Position:
    >> roi.modify(which='PSRNAME', skydir=SkyDir(...))
    
    Modify Spectrum
    >> from uw.like.Models import PowerLaw
    >> roi.modify(which='PSRNAME', model=PowerLaw(norm=1e-11, index=2), keep_old_flux=True)
      
    Freeze ALL spectral parameters:
    >> roi.modify(which='PSRNAME', free=False)
    
    Freeze only one spectral parameter
    >> roi.freeze(which='PSRNAME', free=[True, False]) 
    (but, you have to know how many parameters there are in the model)!
    
    Modify the extension
    >> roi.modify(which='PSRNAME', spatial_model=Disk(sigma=0.2, l=347, b=0.1), keep_old_center=False)
    >> roi.modify(which='PSRNAME', sigma=0.2)
"""

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
            model=roi.get_model(which=name)
            model['index']=index
            model.set_flux(flux,emin=100,emax=100000)
            roi.modify(which=name,model=model)

    for psr_name, cat_name in [
        ['PSRJ0007+7303','2FGL J0007.0+7303'],
        ['PSRJ0030+0451','2FGL J0030.4+0450'],
        ['PSRJ0034-0534','2FGL J0034.4-0534'],
        ['PSRJ0106+4855','2FGL J0106.5+4854'],
        ['PSRJ0205+6449','2FGL J0205.8+6448'],
        ['PSRJ0218+4232','2FGL J0218.1+4233'],
        ['PSRJ0248+6021','2FGL J0248.1+6021'],
        ['PSRJ0340+4130','2FGL J0340.4+4131'],
        ['PSRJ0357+3205','2FGL J0357.8+3205'],
        ['PSRJ0437-4715','2FGL J0437.3-4712'],
        ['PSRJ0534+2200','2FGL J0534.5+2201'],
        ['PSRJ0610-2100','2FGL J0610.3-2059'],
        ['PSRJ0613-0200','2FGL J0613.8-0200'],
        ['PSRJ0614-3329','2FGL J0614.1-3329'],
        ['PSRJ0622+3749','2FGL J0621.9+3750'],
        ['PSRJ0631+1036','2FGL J0631.5+1035'],
        ['PSRJ0633+0632','2FGL J0633.7+0633'],
        ['PSRJ0633+1746','2FGL J0633.9+1746'],
        ['PSRJ0659+1414','2FGL J0659.7+1417'],
#        ['PSRJ0729-1448','?'],
        ['PSRJ0734-1559','2FGL J0734.6-1558'],
        ['PSRJ0742-2822','2FGL J0742.4-2821'],
        ['PSRJ0751+1807','2FGL J0751.1+1809'],

        # ...

        # Vela X is already include in 2FGL and needs to be pruned out
        # of the background model - Nov, 4, 2011 Joshua Lande
        ['PSRJ0835-4510',['2FGL J0835.3-4510','VelaX']], 

        ['PSRJ0908-4913','2FGL J0908.5-4913'],
        ['PSRJ0940-5428',[]], # no 2FGL source...
        ['PSRJ1016-5857','2FGL J1016.5-5858'],

        # Had problems with a source associated with
        # 1023 which is not removed. Actually two sources are associated
        # to 1023 in the 2FGL - Dec 21 Romain 
        ['PSRJ1023-5746','2FGL J1023.5-5749c'],

        # MSH 15-52 is already included in the 2FGL with a template
        # we nee do delete it from the source model - Dec 09 Romain
        ['PSRJ1513-5908','MSH15-52'],
    ]:

        if name == psr_name: 
            print 'Removing 2FGL source %s because it is duplicating the pulsar %s' % (cat_name, psr_name)
            if isinstance(cat_name,list):
                map(roi.del_source,cat_name)
            else:
                roi.del_source(cat_name)
        

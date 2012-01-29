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

def set_flux_index(roi,name,flux,index,emin=100,emax=10**5.5):
    """ Sets the (100 MeV to 100 GeV) flux and index for a
        given source. """
    model=roi.get_model(which=name)
    model['index']=index
    model.set_flux(flux,emin=emin,emax=emax)
    roi.modify(which=name,model=model,keep_old_flux=False)

def modify_roi(name,roi):
    """ For each modification, add some justifcaiton for why
        this needs to be done + where you did the analysis
        which convinced you we need to do this to the region. """

    print 'Modifying source %s' % name

    if name == 'PSRJ0007+7303':
        roi.del_source('2FGL J0007.0+7303')

    elif name == 'PSRJ0030+0451':
        roi.del_source('2FGL J0030.4+0450')

    elif name == 'PSRJ0034-0534':
        roi.del_source('2FGL J0034.4-0534')
        set_flux_index(roi,'PSRJ0034-0534',17.26e-9, 2.27) # from PWNCAT1

    elif name == 'PSRJ0106+4855':
        roi.del_source('2FGL J0106.5+4854')

    elif name == 'PSRJ0205+6449':
        roi.del_source('2FGL J0205.8+6448')

    elif name == 'PSRJ0218+4232':
        roi.del_source('2FGL J0218.1+4233')

    elif name == 'PSRJ0248+6021':
        roi.del_source('2FGL J0248.1+6021')

    elif name == 'PSRJ0340+4130':
        roi.del_source('2FGL J0340.4+4131')

    elif name == 'PSRJ0357+3205':
        roi.del_source('2FGL J0357.8+3205')

    elif name == 'PSRJ0437-4715':
        roi.del_source('2FGL J0437.3-4712')

    elif name == 'PSRJ0534+2200':
        roi.del_source('2FGL J0534.5+2201')
        set_flux_index('PSRJ0534+2200',980.00e-9, 2.15) # from PWNCAT1

    elif name == 'PSRJ0610-2100':
        roi.del_source('2FGL J0610.3-2059')

    elif name == 'PSRJ0613-0200':
        roi.del_source('2FGL J0613.8-0200')

    elif name == 'PSRJ0614-3329':
        roi.del_source('2FGL J0614.1-3329')

    elif name == 'PSRJ0622+3749':
        roi.del_source('2FGL J0621.9+3750')

    elif name == 'PSRJ0631+1036':
        roi.del_source('2FGL J0631.5+1035')

    elif name == 'PSRJ0633+0632':
        roi.del_source('2FGL J0633.7+0633')

    elif name == 'PSRJ0633+1746':
        roi.del_source('2FGL J0633.9+1746')
        set_flux_index(roi,'PSRJ0633+1746', 1115.54e-9, 2.24) # from PWNCAT1

    elif name == 'PSRJ0659+1414':
        roi.del_source('2FGL J0659.7+1417')

    elif name == 'PSRJ0729-1448':
        # no 2FGL source to delete
        pass

    elif name == 'PSRJ0734-1559':
        roi.del_source('2FGL J0734.6-1558')

    elif name == 'PSRJ0742-2822':
        roi.del_source('2FGL J0742.4-2821')

    elif name == 'PSRJ0751+1807':
        roi.del_source('2FGL J0751.1+1809')

    elif name == 'PSRJ0835-4510':
        # Vela X is already include in 2FGL and needs to be pruned out
        # of the background model - Nov, 4, 2011 Joshua Lande
        roi.del_source('2FGL J0835.3-4510')
        roi.del_source('VelaX')
        set_flux_index(roi,'PSRJ0835-4510',405.44e-9, 2.30) # from PWNCAT1

    elif name == 'PSRJ0908-4913':
        roi.del_source('2FGL J0908.5-4913')

    elif name == 'PSRJ0940-5428':
        # no 2FGL source to delete
        pass

    elif name == 'PSRJ1016-5857':
        roi.del_source('2FGL J1016.5-5858')

    elif name == 'PSRJ1019-5749':
        # no 2FGL source to delete
        pass

    elif name == 'PSRJ1023-5746':
        # Had problems with a source associated with
        # 1023 which is not removed. Actually two sources are associated
        # to 1023 in the 2FGL - Dec 21 Romain 
        roi.del_source('2FGL J1023.5-5749c')
        roi.del_source('2FGL J1022.7-5741')
        set_flux_index(roi,'PSRJ1023-5746',1.33e-9, 1.05) # from PWNCAT1

    elif name == 'PSRJ1024-0719':
        roi.del_source('2FGL J1024.6-0719')

    elif name == 'PSRJ1028-5819':
        roi.del_source('2FGL J1028.5-5819')

    elif name == 'PSRJ1044-5737':
        roi.del_source('2FGL J1044.5-5737')

    elif name == 'PSRJ1048-5832':
        roi.del_source('2FGL J1048.2-5831')

    elif name == 'PSRJ1057-5226':
        roi.del_source('2FGL J1057.9-5226')

    elif name == 'PSRJ1105-6107':
        roi.del_source('2FGL J1105.6-6114')

    elif name == 'PSRJ1119-6127':
        roi.del_source('2FGL J1118.8-6128')

    elif name == 'PSRJ1135-6055':
        roi.del_source('2FGL J1135.3-6054')

    elif name == 'PSRJ1231-1411':
        roi.del_source('2FGL J1231.2-1411')

    elif name == 'PSRJ1357-6429':
        roi.del_source('2FGL J1356.0-6436')

    elif name == 'PSRJ1410-6132':
        roi.del_source('2FGL J1409.9-6129')

    elif name == 'PSRJ1413-6205':
        roi.del_source('2FGL J1413.4-6204')

    elif name == 'PSRJ1418-6058':
        roi.del_source('2FGL J1418.7-6058')

    elif name == 'PSRJ1420-6048':
        roi.del_source('2FGL J1420.1-6047')

    elif name == 'PSRJ1429-5911':
        roi.del_source('2FGL J1430.0-5909')

    elif name == 'PSRJ1459-6053':
        roi.del_source('2FGL J1459.4-6054')

    elif name == 'PSRJ1509-5850':
        roi.del_source('2FGL J1509.6-5850')

    elif name == 'PSRJ1513-5908':
        # MSH 15-52 is already included in the 2FGL with a template
        # we nee do delete it from the source model - Dec 09, 2011 Romain
        roi.del_source('MSH15-52')

    elif name == 'PSRJ1531-5610':
        # no 2FGL source to delete
        pass


    elif name == 'PSRJ1600-3053':
        roi.del_source('2FGL J1600.7-3053')

    elif name == 'PSRJ1614-2230':
        roi.del_source('2FGL J1614.5-2230')

    elif name == 'PSRJ1620-4927':
        roi.del_source('2FGL J1620.8-4928')

    elif name == 'PSRJ1709-4429':
        roi.del_source('2FGL J1709.7-4429')

    elif name == 'PSRJ1713+0747':
        roi.del_source('2FGL J1714.0+0751')

    elif name == 'PSRJ1718-3825':
        roi.del_source('2FGL J1718.3-3827')

    elif name == 'PSRJ1702-4128':
        # no 2FGL source to delete
        pass 

    elif name == 'PSRJ1732-3131':
        roi.del_source('2FGL J1732.5-3131')

    elif name == 'PSRJ1741-2054':
        roi.del_source('2FGL J1741.9-2054')

    elif name == 'PSRJ1744-1134':
        roi.del_source('2FGL J1744.6-1135')

    elif name == 'PSRJ1746-3239':
        roi.del_source('2FGL J1746.5-3238')

    elif name == 'PSRJ1747-2958':
        roi.del_source('2FGL J1747.1-3000')

    elif name == 'PSRJ1803-2149':
        roi.del_source('2FGL J1803.3-2148')

    elif name == 'PSRJ1809-2332':
        roi.del_source('2FGL J1809.8-2332')

    elif name == 'PSRJ1813-1246':
        roi.del_source('2FGL J1813.4-1246')
        set_flux_index(roi,'PSRJ1813-1246', 295.55e-9, 2.65) # from PWNCAT1

    elif name == 'PSRJ1823-3021A':
        roi.del_source('2FGL J1823.4-3014')


    elif name == 'PSRJ1826-1256':
        # Note: PSR J1826-1256 is associated with the PWN HESS J1825-137 - Lande Jan 23, 2012 
        roi.del_source('2FGL J1826.1-1256')
        roi.del_source('HESSJ1825-137')


    elif name == 'PSRJ1836+5925':
        roi.del_source('2FGL J1836.2+5926')
        set_flux_index(roi,'PSRJ1836+5925', 579.6e-9, 2.07) # from PWNCAT1

    elif name == 'PSRJ1846+0919':
        roi.del_source('2FGL J1846.4+0920')

    elif name == 'PSRJ1907+0602':
        roi.del_source('2FGL J1907.9+0602')

    elif name =='PSRJ1939+2134':
        # no 2FGL source to delete
        pass

    elif name == 'PSRJ1952+3252':
        roi.del_source('2FGL J1953.0+3253')

    elif name == 'PSRJ1954+2836':
        roi.del_source('2FGL J1954.3+2836')

    elif name == 'PSRJ1957+5033':
        roi.del_source('2FGL J1957.9+5033')

    elif name == 'PSRJ1958+2846':
        roi.del_source('2FGL J1958.6+2845')

    elif name == 'PSRJ1959+2048':
        roi.del_source('2FGL J1959.5+2047')

    elif name == 'PSRJ2017+0603':
        roi.del_source('2FGL J2017.3+0603')

    elif name == 'PSRJ2021+3651':
        roi.del_source('2FGL J2021.0+3651')

    elif name == 'PSRJ2021+4026':
        roi.del_source('2FGL J2021.5+4026')
        set_flux_index(roi,'PSRJ2021+4026', 1603.00e-9, 2.36) # from PWNCAT1

    elif name == 'PSRJ2028+3332':
        roi.del_source('2FGL J2028.3+3332')

    elif name == 'PSRJ2030+3641':
        roi.del_source('2FGL J2030.0+3640')

    elif name == 'PSRJ2030+4415':
        roi.del_source('2FGL J2030.7+4417')

    elif name == 'PSRJ2032+4127':
        roi.del_source('2FGL J2032.2+4126')

    elif name == 'PSRJ2043+2740':
        roi.del_source('2FGL J2043.7+2743')

    elif name == 'PSRJ2051-0827':
        # no 2FGL source to delete
        pass

    elif name == 'PSRJ2055+2539':
        roi.del_source('2FGL J2055.8+2539')
        set_flux_index(roi,'PSRJ2055+2539', 38.41e-9, 2.51) # from PWNCAT1

    elif name == 'PSRJ2124-3358':
        roi.del_source('2FGL J2124.6-3357')
        set_flux_index(roi,'PSRJ2124-3358', 22.78e-9, 2.06) # from PWNCAT1

    elif name == 'PSRJ2139+4716':
        roi.del_source('2FGL J2139.8+4714')

    elif name == 'PSRJ2214+3000':
        roi.del_source('2FGL J2214.7+3000')

    elif name == 'PSRJ2238+5903':
        roi.del_source('2FGL J2238.4+5902')

    elif name == 'PSRJ2240+5832':
        roi.del_source('2FGL J2239.8+5825')

    elif name == 'PSRJ2302+4442':
        roi.del_source('2FGL J2302.7+4443')

    else:
        # Note, if no changes are needed, then simply put elif ... pass 
        # (like PSRJ0729-1448). This is just a sanity check.
        raise Exception("Unrecognized pulsar %s" % name)

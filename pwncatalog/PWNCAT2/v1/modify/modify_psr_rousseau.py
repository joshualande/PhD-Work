
import modify_psr_base

def modify_roi(name,roi):

    modify_psr_base.modify(name,roi)

    # Change a source into power law cause it seems to me that it should
    # be a power law at least in the off - Romain Dec 21
    if name=="PSRJ1023-5746":
        from uw.like.Models import PowerLaw
        roi.modify(which='2FGL J1045.0-5941', model=PowerLaw(norm=1e-11, index=2), keep_old_flux=True)
        
    #List of sources not well fitted in the run of Dec 05 - Dec 09 Romain
    #List modified on Jan 04 to not include two times the same sources -Romain

    freelist=['2FGL J0017.6-0510', '2FGL J0050.6-0929', '2FGL J0136.9+4751', '2FGL J0222.6+4302', '2FGL 0230.8+4031', '2FGL J0240.5+6113', '2FGL J0308.7+5954', '2FGL J0224.0+6204', '2FGL J0218.7+6208c', '2FGL J0221.4+6257c', '2FGL J0258+6448', '2FGL J0319.8+4130', '2FGL J0358.8+3205', '2FGL J0341.8+3148c', '2FGL J0324.8+3408', 'IC443', '2FGL J0609.6-1847', '2FGL J0634.4+0356c', '2FGL J0631.7+0428', '2FGL J0637.0+0416c', '2FGL J0633.7+0633', '2FGL J0627.1-3258', '2FGL J0602.7-4011', '2FGL J0622.9+3326', '2FGL J0654.2+4514', '2FGL J0659.7+1417', '2FGL J0700.3+1710', '2FGL J0910.4-5050', '2FGL J0842.9-4721', '2FGL J0848.5-4535', '2FGL J1022.7-5741', '2FGL J1019.0-5856', '2FGL J1023.5-5749c', '2FGL J1028.5-5819', '2FGL J1044.5-5737', '2FGL J1057.9-5226', '2FGL J1048.2-5831', '2FGL J1045.0-5941', '2FGL J1103.9-5356', '2FGL J1124.6-5913', '2FGL J1112.1-6040', '2FGL J1105.6-6114', '2FGL J1104.7-6036', '2FGL J1226.7-1331', '2FGL J1241.6-1457', '2FGL J1238.1-1953', '2FGL J1221.4-0633', '2FGL J1422.5-6137c', '2FGL J1418.7-6058', '2FGL J1420.1-6047', '2FGL J1330.1-7002', '2FGL J1405.5-6121', '2FGL J1430.0-5909', '2FGL J1413.4-6204', '2FGL J1521.8-5735', '2FGL J1509.6-5850', '2FGL J1536.4-4949', '2FGL J1514.1-4946', '2FGL J1027.4-5730c', '2FGL J1626.1-2948', '2FGL J1617.6-2526c', '2FGL J1625.7-2526', '2FGL J1627.0-2425c', '2FGL J1718.3-3827', '2FGL J1747.1-3000', '2FGL J1743.9-3039c', '2FGL 1745.5-3028c', 'W28', '2FGL J1809.8-2332', '2FGL J1811.3-2421', '2FGL J1733.1-1307', '2FGL J1813.4-1246', '2FGL J1745.1-1729', '2FGL J1748.7-2020', '2FGL J1749.7-3134c', '2FGL J1737.2-3213', 'W30', '2FGL J1833.6-2104', '2FGL J1823.1-1338c', '2FGL J1826.1-1256', '2FGL J1826.4-1450', '2FGL J1856.2+0450c', '2FGL J1906.5+0720', '2FGL J1907.9+0602', '2FGL J1932.1+1913', '2FGL J1954.3+2836', '2FGL J1953.0+3253', '2FGL J2018.0+3626', '2FGL J2001.1+4352', '2FGL J2030.7+4417', '2FGL J2015.6+3709', '2FGL J2030.0+3640', '2FGL J2025.1+3341', '2FGL J2021.0+3651', '2FGL J0255.8+2539', 'CygnusLoop', '2FGL J2005.6-0736', '2FGL 2043.7+2743']
    
    #Uggly loop to free the sources.-Romain Dec 09
    sources = roi.get_sources()
    for source in sources:
        name2=source.name
        for source2 in freelist:
            if name2.lower()==source2.lower():
                try :
                    roi.freeze(which=name2, free=[True, True])
                except :
                    try :
                        roi.freeze(which=name2, free=[True, True, True])
                    except :
                        try :
                            roi.freeze(which=name2, free=[True, True, True,False])
                        except :
                            try :
                                roi.freeze(which=name2, free=[True, True, True,False,False])
                            except :
                                print "%s is not frozen"%name2
                                
                                

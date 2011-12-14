
def modify_roi(name,roi):

    if name == '0FGL_J0631.8+1034':
        # Remove duplicate source - Dec 10, 2010 - JL
        roi.del_source('2FGL J0631.5+1035')
    
    if name == '0FGL_J1958.1+2848':
        # Remove duplicate source - Dec 10, 2010 - JL
        roi.del_source('2FGL J1958.6+2845')

    if name == 'Boomerang':
        # Remove duplicate source - Dec 10, 2010 - JL
        roi.del_source('2FGL J2229.0+6114')

    if name == 'G292.2-0.5':
        # Remove duplicate source - Dec 10, 2010 - JL
        roi.del_source('2FGL J1118.8-6128')
        
    if name == 'HESS_J1356-645':
        # Remove duplicate source - Dec 10, 2010 - JL
        roi.del_source('2FGL J1356.0-6436')

    if name == 'HESS_J1632-478':
        # this is the HESS source - Dec 10, 2011 - JL
        roi.del_source('2FGL J1632.4-4753c')

    if name == 'HESS_J1640-465':
        # this is the HESS source - Dec 10, 2011 - JL
        roi.del_source('2FGL J1640.5-4633')

    if name == 'HESS_J1718-385':
        # this is the HESS source - Dec 10, 2011 - JL
        roi.del_source('2FGL J1718.3-3827')

    if name == 'Kookaburra':
        # this is the HESS source - Dec 10, 2011 - JL
        roi.del_source('2FGL J1420.1-6047')

    if name == 'Kookaburra_Rabbit':
        # this is the HESS source - Dec 10, 2011 - JL
        roi.del_source('2FGL J1418.7-6058')

    if name == 'Vela_X':
        # Remove 2FGL version of Vela X - Dec, 4, 2011 - JL
        print 'Deleting 2FGL version of Vela X!'
        roi.del_source('VelaX') # remove 2FGL version

    if name == 'MSH_15-52':
        # Remove 2FGL version of MSH15-52 - Dec, 4, 2011 - JL
        print 'Deleting 2FGL version of MSH15-52!'
        roi.del_source('MSH15-52') # remove 2FGL version

    if name == 'HESS_J1303-631':
        # not sure if I should be removing this source. -- Dec 4, 2011 - JL
        roi.del_source('2FGL J1303.7-6316c')


    if name == 'HESS_J1825-137':
        # Remove 2FGL version of Vela X - Dec, 10, 2011 - JL
        print 'Deleting 2FGL version of HESSJ1825-137!'
        roi.del_source('HESSJ1825-137') # remove 2FGL version

    if name == 'HESS_J1616-508':
        # Remove duplicate source - Dec 10, 2010 - JL
        roi.del_source('2FGL J1615.0-5051')

    if name== 'Westerlund_2':
        # Remove nearby sources (not sure if this is good???) - Dec 10, 2010 - JL
        roi.del_source('2FGL J1023.5-5749c')
        roi.del_source('2FGL J1022.7-5741')

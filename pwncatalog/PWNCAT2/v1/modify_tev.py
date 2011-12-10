
def modify_roi(name,roi):

    if name=='Vela_X':
        # Remove 2FGL version of Vela X - Dec, 4, 2011 Joshua Lande
        print 'Deleting Vela X from background model!'
        roi.del_source('VelaX') # remove 2FGL version

    if name=='MSH_15-52':
        # Remove 2FGL version of MSH15-52 - Dec, 4, 2011 Joshua Lande
        print 'Deleting MSH15-52 from background model!'
        roi.del_source('MSH15-52') # remove 2FGL version

    if name=='HESS_J1303-631':
        # not sure if I should be removing this source. -- Dec 4, 2011 Joshua Lande
        roi.del_source('2FGL J1303.7-6316c')









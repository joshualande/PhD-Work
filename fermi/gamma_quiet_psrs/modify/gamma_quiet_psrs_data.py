

def modify_roi(roi, name):

    print 'Running modify_roi on source %s' % name

    deleted_sources = []
    new_sources = []
    
    def delete(name, *args, **kwargs):
        print ' * Deleting from ROI source %s' % name
        source = roi.del_source(name, *args, **kwargs)
        deleted_sources.append(name)

    def add(source, *args, **kwargs):
        print ' * Adding to ROI source %s' % (source.name)
        roi.add_source(source, *args, **kwargs)
        new_sources.append(source.name)


    if name == 'J0855-4644':
        pass
    
    elif name == 'J1341-6220':
        pass
    
    elif name == 'J1400-6325':
        pass
    
    elif name == 'J1437-5959':
        pass

    elif name == 'J1524-5625':
        pass
        
    elif name == 'J1747-2809':
        pass
        
    elif name == 'J1811-1925':
        pass
        
    elif name == 'J1828-1101':
        pass
    
    elif name == 'J1837-0604':
        pass
    
    elif name == 'J1928+1746':
        delete('2FGL J1928.8+1740c')

    elif name == 'J1936+2025':
        pass
        
    elif name == 'J2022+3842':
        delete('2FGL J2022.8+3843c')

    else:
        raise Exception("Unrecognized source %s" % name)

    print 'Done running modify_roi on source %s' % name

    return new_sources, deleted_sources

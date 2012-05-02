
def setup_tev(name, tevsources, fit_emin, fit_emax, extended=False, **kwargs):
    """ Sets up the ROI for studying a TeV Source. """
    tev=yaml.load(open(tevsources))
    source=tev[name]
    l,b=source['gal']
    tev_position=SkyDir(l,b,SkyDir.GALACTIC)

    # data, should be more elegant...
    ft1=e('$FERMILANDE/data/PWNCAT2/nov_30_2011/ft1_PWNCAT2_allsky.fits')
    ft2=e('$FERMILANDE/data/PWNCAT2/nov_30_2011/ft2_PWNCAT2_allsky.fits')
    ltcube=e('$FERMILANDE/data/PWNCAT2/nov_30_2011/ltcube_PWNCAT2_allsky.fits')
    binsperdec=4
    binfile=e('$FERMILANDE/data/PWNCAT2/nov_30_2011/binned_%s.fits' % binsperdec)

    # parse the extension
    ext = source['ext']
    if isnum(ext):
        sigma = ext
    elif isinstance(ext, list) and len(ext) == 2 and isnum(ext[0]) and isnum(ext[1]):
        sigma = np.sqrt(ext[0]*ext[1]) # Same surface area
    elif ext == '?':
        sigma = 0 # best we can do since no published size
    else:
        raise Exception("Unrecogized size %g" % sigma)

    source = get_source(name, 
                        fit_emin=fit_emin, 
                        fit_emax=fit_emax, 
                        position = tev_position, sigma = sigma,
                        extended=extended)

    roi = setup_region(name, 
                       phase = PhaseRange(0,1),
                       ft1=ft1, 
                       ft2=ft2, 
                       ltcube=ltcube, 
                       binsperdec=binsperdec,
                       binfile=binfile,
                       roi_dir=tev_position,
                       fit_emin=fit_emin, 
                       fit_emax=fit_emax, 
                       sources = [source],
                       savedir = None,
                       **kwargs)
    return roi

def plots(roi, hypothesis, size=5):
    print 'Making plots for hypothesis %s' % hypothesis
    roi.plot_tsmap(filename='residual_tsmap_%s_%s.png' % (hypothesis,name), size=size, pixelsize=0.1)
    for pixelsize in [0.1,0.25]:
        roi.plot_counts_map(filename="counts_%.g_%s_%s.png"%(pixelsize,hypothesis,name),
                            countsfile="counts_%.g_%s_%s.fits"%(pixelsize,hypothesis,name),
                            modelfile="model_%.g_%s_%s.fits"%(pixelsize,hypothesis,name),
                            pixelsize=pixelsize,size=size)
    roi.zero_source(which=name)
    roi.plot_tsmap(filename='source_tsmap_%s_%s.png' % (hypothesis, name), size=size, pixelsize=0.1)
    for pixelsize in [0.1,0.25]:
        roi.plot_counts_map(filename="counts_excess_%.g_%s_%s.png"%(pixelsize,hypothesis,name),
                            countsfile="counts_excess_%.g_%s_%s.fits"%(pixelsize,hypothesis,name),
                            modelfile="model_%.g_%s_%s.fits"%(pixelsize,hypothesis,name),
                            pixelsize=pixelsize,size=size)
    roi.unzero_source(which=name)

    roi.plot_source(which=name,filename='source_%s_%s.png' % (hypothesis, name), 
                    size=size, label_psf=False)
    roi.plot_sources(which=name,filename='sources_%s_%s.png' % (hypothesis, name), 
                     size=size, label_psf=False)

    roi.toRegion('Region_file_%s.reg'%name)
    roi.toXML(filename="srcmodel_res_%s_%s.xml"%(hypothesis, name))
    roi.plot_slice(which=name,filename="outslice_%s_%s.png"%(hypothesis, name),datafile='slice_points_%s_%s.out'%(hypothesis, name))
    #plot_all_seds(roi, filename="allsed_%s_%s.png"%(hypothesis, name))
    roi.plot_counts_spectra(filename="Spectra_%s_%s.png"%(hypothesis, name))


def pointlike_analysis(roi, hypothesis, upper_limit=False, localize=False, fit_extension=False, extension_upper_limit=False, cutoff=False):
    print 'Performing Pointlike analysis for %s' % hypothesis

    print_summary = lambda: roi.print_summary(galactic=True)
    print_summary()

    print roi

    def fit():
        """ Convenience function incase fit fails. """
        try:
            roi.fit(method="minuit",use_gradient=True)
        except Exception, ex:
            print 'ERROR spectral fitting: ', ex
        print_summary()

    fit()

    if localize:
        try:
            roi.localize(name, update=True)
        except Exception, ex:
            print 'ERROR localizing: ', ex
        fit()

    if fit_extension:
        try:
            roi.fit_extension(name)
            roi.localize(name, update=True)
        except Exception, ex:
            print 'ERROR localizing: ', ex
        fit()

    p = sourcedict(roi, name)

    if extension_upper_limit:
        print 'Calculating extension upper limit'
        p['extension_upper_limit']=roi.extension_upper_limit(which=name, confidence=0.95, spatial_model=Gaussian(), npoints=10)

    if upper_limit:
        p['upper_limit'] = powerlaw_upper_limit(roi, name, emin=emin, emax=emax, cl=.95)
    if cutoff:
        p['test_cutoff']=test_cutoff(roi,name)

    roi.plot_sed(which=name,filename='sed_pointlike_%s_%s.pdf' % (hypothesis,name), use_ergs=True)
 
    roi.save('roi_%s_%s.dat' % (hypothesis,name))

    if do_plots: plots(roi, hypothesis)
    return p

def gtlike_analysis(roi, hypothesis, upper_limit=False, cutoff=False):
    print 'Performing Gtlike crosscheck for %s' % hypothesis

    gtlike=Gtlike(roi)
    like=gtlike.like
    like.fit(covar=True)

    r=sourcedict(like, name)

    if upper_limit:
        r['upper_limit'] = powerlaw_upper_limit(like, name, emin=emin, emax=emax, cl=.95)
    
    if cutoff:
        r['test_cutoff']=test_cutoff(like,name)

    for kind, kwargs in [['4bpd',dict(bin_edges=np.logspace(2,5,13))],
                         ['1bpd',dict(bin_edges=np.logspace(2,5,4))]]:

        print 'Making %s SED' % kind
        sed = SED(like, name, **kwargs)
        sed.plot('sed_gtlike_%s_%s_%s.png' % (kind,hypothesis,name)) 
        sed.verbosity=True
        sed.save('sed_gtlike_%s_%s_%s.dat' % (kind,hypothesis,name))

    return r
    
def save_results(): 
    open('results_%s.yaml' % name,'w').write(
        yaml.dump(tolist(results)))


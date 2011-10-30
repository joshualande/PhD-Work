
def plot_profile(self,which,filename="profile.png", datafile="profile.yaml", figsize=(4,4),**kwargs):

    extension_list,TS_spectral,TS_bandfits = \
            self.extension_profile(which=which,filename=datafile,**kwargs)

    P.figure(figsize=figsize)
    P.clf()
    P.plot(extension_list,TS_spectral)
    P.xlabel('extension (degrees)')
    P.ylabel('Source TS')

    source=self.get_source(which)
    P.title('Extension profile %s' % source.name)

    P.savefig(filename)

def extension_profile(roi,which,filename='profile.yaml',
        num_points=15,lower_limit=None,upper_limit=None,
        quick=True,use_gradient=True):
    """ Perform a scan in extension. 

        which is the source to calculate the profile of. Note that extension
        profiles can only be calculated for sources. """

    manager,index=roi.mapper(which)

    if manager != roi.dsm: 
        raise Exception("An extension profile can only be calculated for diffuse sources.")
    ds=manager.diffuse_sources[index]
    esm=manager.bgmodels[index]

    if not roi.quiet: print 'Calculating extension profile for %s' % ds.name

    if not isinstance(ds,ExtendedSource): 
        raise Exception("An extension profile can only be calculated for extended sources")

    sm=ds.spatial_model
    if not len(sm.p)==3: 
        raise Exception("An extension profile can only be calculated for extended sources with 3 parameters (position + one extension)")

    # save spatial parameters
    old_sm_p    = sm.p.copy()
    old_sm_cov    = sm.cov_matrix.copy()

    # save spectral parameters
    old_roi_p = roi.get_parameters().copy()

    # Keep the TS function quiet
    old_quiet=roi.quiet
    roi.quiet=True

    p,plo,phi=sm.statistical(absolute=True,two_sided=True)

    x,y,ext=p
    upper_limit = min(p[2] + max(3*phi[2],p[2]),3) if upper_limit is None else upper_limit
    if lower_limit is None:
        lower_limit = float(upper_limit)/num_points/10.0 # make the bottom point ~ 0.1xfirst point
    extension_list=np.linspace(lower_limit,upper_limit,num_points).tolist()

    TS_spectral=[]
    TS_bandfits=[]

    TS_bin={}
    roi.setup_energy_bands()
    for band in roi.energy_bands:
        TS_bin[band.emin,band.emax]=[]

    if not old_quiet: print '%20s %20s %20s' % ('extension','TS_spectral','TS_bandfits')
    for i,extension in enumerate(extension_list):
        sm.set_parameters(p=[x,y,extension],absolute=True)
        esm.initialize_counts(roi.bands)
        roi.update_counts()

        # Here the strategy is to try localizing and then
        # try localizing again from the starting spectral
        # value. The best fit from both is kepth. """
        roi.fit(estimate_errors=False,use_gradient=use_gradient)
        params=roi.parameters()
        ll_a=-1*roi.logLikelihood(roi.parameters())
        roi.update_counts(old_roi_p)
        roi.fit(estimate_errors=False,use_gradient=use_gradient)
        ll_b=-1*roi.logLikelihood(roi.parameters())
        if ll_a > ll_b: roi.update_counts(params)

        TS_spectral.append(float(roi.TS(which=which,quick=True)))
        TS_bandfits.append(float(roi.TS(which=which,quick=True,bandfits=True)))
        if not old_quiet: print '[ %20s ] %20g %20g' % (sm.pretty_spatial_string(),TS_spectral[i],TS_bandfits[i])
        for band in roi.energy_bands: TS_bin[float(band.emin),float(band.emax)].append(float(band.ts))
    
    # set back spatial parameters
    sm.set_parameters(old_sm_p,absolute=False)
    sm.cov_matrix = old_sm_cov

    # set back spectral parameters
    roi.set_parameters(old_roi_p)
    roi.__set_error__()

    # reset counts

    esm.initialize_counts(roi.bands)
    roi.__update_state__()

    roi.quiet=old_quiet

    save_dict=[]

    save_dict={'extension':extension_list,
               'TS_spectral':TS_spectral,
               'TS_bandfits':TS_bandfits,
               'bins':roi.bin_edges.tolist()}
    save_dict['TS_bands']=[]
    for (emin,emax),TS in TS_bin.items():
        save_dict['TS_bands'].append({'emin':emin,'emax':emax,'TS':TS})
    file=open(filename,'w')
    file.write(yaml.dump(save_dict))

    return extension_list,TS_spectral,TS_bandfits

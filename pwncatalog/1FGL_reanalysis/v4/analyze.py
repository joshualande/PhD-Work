#!/usr/bin/env python

# Not entirely sure why, but pyLikelihood
# will get a swig::stop_iteraiton error
# unless it is imported first.
from roi_gtlike import Gtlike

from uw.like.sed_plotter import plot_sed

from setup_pwn import setup_pwn,get_source
from uw.like.SpatialModels import Gaussian
from uw.like.roi_tsmap import TSCalc,TSCalcPySkyFunction
from argparse import ArgumentParser
from skymaps import SkyImage,SkyDir
import yaml
from SED import SED

from toolbag import tolist
from likelihood_tools import sourcedict,powerlaw_upper_limit, test_cutoff
from collections import defaultdict
import numpy as np
np.seterr(all='ignore')

parser = ArgumentParser()
parser.add_argument("--pwndata", required=True)
parser.add_argument("-p", "--pwnphase", required=True)
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
parser.add_argument("--emin", default=1e2, type=float)
parser.add_argument("--emax", default=1e5, type=float)
parser.add_argument("--no-point", default=False, action="store_true")
parser.add_argument("--no-extended", default=False, action="store_true")
parser.add_argument("--no-gtlike", default=False, action="store_true")
parser.add_argument("--no-plots", default=False, action="store_true")
parser.add_argument("--no-cutoff", default=False, action="store_true")
parser.add_argument("--no-extension-upper-limit", default=False, action="store_true")
args=parser.parse_args()

do_point = not args.no_point
do_extended = not args.no_extended
do_gtlike = not args.no_gtlike
do_plots = not args.no_plots
do_cutoff = not args.no_cutoff
do_extension_upper_limit = not args.no_extension_upper_limit


name=args.name
emin=args.emin
emax=args.emax

phase=yaml.load(open(args.pwnphase))[name]['phase']
roi=setup_pwn(name,args.pwndata,phase)


def customize_roi(name,roi):
    """ For each modification, add some justifcaiton for why
        this needs to be done + where you did the analysis
        which convinced you we need to do this to the region. """

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

customize_roi(name,roi)

results=r=defaultdict(lambda: defaultdict(dict))


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

    def fit():
        """ Convenience function incase fit fails. """
        try:
            roi.fit(use_gradient=False)
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

r['at_pulsar']['pointlike']=pointlike_analysis(roi, 'at_pulsar', upper_limit=True, cutoff=do_cutoff)
save_results()
if do_gtlike: r['at_pulsar']['gtlike']=gtlike_analysis(roi, 'at_pulsar', upper_limit=True, cutoff=do_cutoff)

if do_point:
    r['point']['pointlike']=pointlike_analysis(roi, 'point', localize=True, cutoff=do_cutoff, extension_upper_limit=do_extension_upper_limit)
    save_results()
    if do_gtlike: r['point']['gtlike']=gtlike_analysis(roi, 'point', cutoff=do_cutoff)

if do_extended:
    roi.del_source(name)
    roi.add_source(get_source(name,args.pwndata, extended=True))

    r['extended']['pointlike']=pointlike_analysis(roi, 'point', cutoff=do_cutoff, fit_extension=True)
    save_results()
    if do_gtlike: r['extended']['gtlike']=gtlike_analysis(roi, 'point', cutoff=do_cutoff)

    for which in ['pointlike','gtlike']:
        results['extended'][which]['ts_ext'] = \
                2*(results['extended'][which]['logLikelihood'] - \
                   results['point'][which]['logLikelihood'])

save_results()

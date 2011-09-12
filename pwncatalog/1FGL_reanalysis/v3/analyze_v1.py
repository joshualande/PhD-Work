#!/usr/bin/env python

# Not entirely sure why, but pyLikelihood
# will get a swig::stop_iteraiton error
# unless it is imported first.
from roi_gtlike import Gtlike

from uw.like.sed_plotter import plot_sed

from setup_pwn import setup_pwn
from uw.like.SpatialModels import Disk
from uw.like.roi_tsmap import TSCalc,TSCalcPySkyFunction
from argparse import ArgumentParser
from skymaps import SkyImage,SkyDir
import yaml
from SED import SED

from toolbag import sourcedict,tolist

parser = ArgumentParser()
parser.add_argument("--pwndata", required=True)
parser.add_argument("-p", "--pwnphase", required=True)
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
args=parser.parse_args()
  
name=args.name

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

    # Or Vela X to be an exended source

customize_roi(name,roi)

results=r={}

roi.print_summary()
    
roi.fit(use_gradient=True)

roi.print_summary()
roi.plot_sed(which=name,filename='sed_pointlike_%s.pdf' % name, use_ergs=True)

r['pointlike']=sourcedict(roi,name,'_at_pulsar')

gtlike=Gtlike(roi)
like=gtlike.like
like.fit(covar=True)

r['gtlike']=sourcedict(like,name,'_at_pulsar')

# calculate gtlike upper limits ...

# calculate TScutoff ...

roi.save('roi_%s.dat' % name)

open('results_%s.yaml' % name,'w').write(
    yaml.dump(
        tolist(results)
        )
    )

# save stuff out
roi.plot_tsmap(filename='residual_tsmap_%s.pdf' % name, size=8)

roi.zero_source(which=name)
roi.plot_tsmap(filename='source_tsmap_%s.pdf' % name, size=8)
roi.unzero_source(which=name)

roi.plot_sources(filename='sources_%s.pdf' % name, size=8, label_psf=False)

sed = SED(like,name, verbosity=True)
sed.save('sed_gtlike_%s.dat' % name)
sed.plot('sed_gtlike_%s.pdf' % name) 

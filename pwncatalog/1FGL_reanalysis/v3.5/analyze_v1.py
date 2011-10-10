#!/usr/bin/env python

# Not entirely sure why, but pyLikelihood
# will get a swig::stop_iteraiton error
# unless it is imported first.
#print "Coucou1"
import matplotlib as mpl
mpl.rcParams['backend'] = 'Agg'
mpl.use("Agg")
#print "Coucou2"

from roi_gtlike import Gtlike

from uw.like.sed_plotter import plot_sed

from setup_pwn import setup_pwn
from uw.like.SpatialModels import Disk
from uw.like.roi_tsmap import TSCalc,TSCalcPySkyFunction
from argparse import ArgumentParser
from skymaps import SkyImage,SkyDir
import yaml
from SED import SED
from uw.like.roi_analysis import *

from toolbag import sourcedict,tolist
from numpy import pi

#gtlike upperlimits
from UpperLimits import UpperLimits
from IntegralUpperLimit import *

#import mathematic library to have function cos,acos,sin,sqrt...
from math import *
from localize_loop import *

parser = ArgumentParser()
parser.add_argument("--pwndata", required=True)
parser.add_argument("-p", "--pwnphase", required=True)
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
parser.add_argument("-emin", "--emin",  default=1.0e2, type=float)
parser.add_argument("-emax", "--emax",  default=1.0e5, type=float)
parser.add_argument("-model", "--model")

args=parser.parse_args()
  
name=args.name

phase=yaml.load(open(args.pwnphase))[name]['phase']

#####setup the roi testing if we want to use a model or a catalog


if args.model != "None":
    #Include an existing sourcemodel
    modelloc=args.model+"/%s/srcmodel_%s.xml"
    roi=setup_pwn(name,args.pwndata,phase,emin=args.emin,emax=args.emax,model=modelloc,maxroi=maxroi)
else :
    #Create a source model such as less than 20 parameters still free
    maxroi=10.0
    free_radius=5.0
    roi=setup_pwn(name,args.pwndata,phase,emin=args.emin,emax=args.emax,free_radius=free_radius,maxroi=maxroi)

    while len(roi.parameters())>19 and free_radius>0.5:
        free_radius*=0.9
        roi=setup_pwn(name,args.pwndata,phase,emin=args.emin,emax=args.emax,free_radius=free_radius,maxroi=maxroi)
        
def get_spec_par(like,srcname):
    """Function to obtain the spectral parameters of a source using the like object"""
    #Call the function
    funcs = like[srcname].src.getSrcFuncs()
    
    param=[]
    liste_param=[]
    
    #spectral function :
    spectype=funcs['Spectrum'].genericName()
    print srcname
    print spectype
    
    if spectype=="PowerLaw":
        liste_param=["Prefactor","Index","Scale"]
    elif spectype=="BrokenPowerLaw":
        liste_param=["Prefactor","Index1","BreakValue","Index2"]
    elif spectype=="PowerLaw2":
        liste_param=["Integral","Index","LowerLimit","UpperLimit"]
    elif spectype=="BrokenPowerLaw2":
        liste_param=["Integral","Index1","Index2","BreakValue","LowerLimit","UpperLimit"]
    elif spectype=="LogParabola":
        liste_param=["norm","alpha","Eb","beta"]
    elif spectype=="ExpCutoff":
        liste_param=["Prefactor","Index","Scale","Ebreak","P1","P2","P3"]
    elif spectype=="BPLExpCutoff":
        liste_param=["Prefactor","Index1","Index2","BreakValue","Eabs","P1"]
    elif spectype=="Gaussian":
        liste_param=["Prefactor","Mean","Sigma"]
    elif spectype=="ConstantValue":
        liste_param=["Value"]
    elif spectype=="BandFunction":
        liste_param=["norm","alpha","beta","Ep"]
    elif spectype=="PLSuperExpCutoff":
        liste_param=["Prefactor","Index1","Scale","Cutoff","Index2"]
    else :
        print "Did not found the model"
        
    for i in range(len(liste_param)):
        param.append(float(funcs['Spectrum'].getParam(liste_param[i]).getValue())*float(funcs['Spectrum'].getParam(liste_param[i]).getScale()))
            
    return spectype,param,liste_param
        
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

def gtlike_ul(like,emin,emax,name,sigma=2):
    """Function to compute the upperlimit using the like object and steeve's bayesian algorithm
    __________________________________________________________________________________________
    like : like object
    emin,emax : minimum and maximum of the energy range on which compute the upperlimit
    name : name of the source
    sigma : number of sigma corresponding to the confidence level. sigma must be 1,2 or 3.
            otherwise, the confidence level is set at 90%
    __________________________________________________________________________________________"""

    if sigma==1:
        conf=0.6827
    elif sigma==2:
        conf=0.9545
    elif sigma==3:
        conf=0.9973
    else :
        print "90% confidence level"
        conf=0.90
    
    if like.Ts(name, reoptimize=False) < 25 and like.Ts(name, reoptimize=False) >= 1:
        ul = UpperLimits(like)
        limit, xx = ul[name].compute(emin=emin, emax=emax)
    elif like.Ts(name, reoptimize=False) < 1:
        ul = UpperLimits(like)
        limit, xx = ul[name].bayesianUL(cl=conf, emin=float(emin), emax=float(emax))
    else :
        print 'Je ne suis pas rentre dans les conditions :'
        print like.Ts(name, reoptimize=False)

    return limit,xx

def renorm(roi):
    """Function to renormalize the source model"""
    for names in roi.get_names():
        try :
            roi.modify(names,Norm=roi.get_model(names)[0]*roi.phase_factor)
        except :
            try :
                roi.modify(names,Int_flux=roi.get_model(names)[0]*roi.phase_factor)
            except :
                try :
                    roi.modify(names,Norm=roi.get_model(names)[0]*roi.phase_factor)
                except :
                    print names
                
            

#customize_roi(name,roi)

results=r={}

#pointlike_fit


#Renormalize the model only if it was just created cause it has already been done in a previous srcmodel.

print roi
print "args.model"
print args.model
#if args.model != "None":
#renorm(roi)

#print controls befor to begin with the analysis

print roi

roi.print_summary()

#Get the xml before the fit.

roi.toXML(filename="srcmodel_prefit_%s.xml"%name,convert_extended=True)

#fit
    
roi.fit(method="minuit",use_gradient=True)

#obtain all the controls after the first fit

roi.print_summary()
TS_pointlike=roi.TS(which=name,quick=False,method="minuit")

r['pointlike']=sourcedict(roi,name,'_at_pulsar')

roi.save("temp_roi.dat")
renorm(roi)

#gtlike fit using the same logic

gtlike=Gtlike(roi)
roi=load("temp_roi.dat")
os.system("rm -rf temp_roi.dat")
like=gtlike.like

try :
    gtlike.like[gtlike.like.par_index(name, 'Prefactor')].setBounds(0.0,1.0e5)
except :
    gtlike.like[gtlike.like.par_index(name, 'Integral')].setBounds(0.0,1.0e5)
print like.model

like.fit(covar=True)

print like.model

#freezing all the other source.

liste_source=like.sourceNames()
for i in range(len(liste_source)):
    spec,lis,lisname=get_spec_par(like,liste_source[i])
    if liste_source[i]!=name:
        for j in range(len(lisname)):
            param=like.par_index(liste_source[i],lisname[j])
            like.freeze(param)
print "Repere 1"
print like.model


like.fit(covar=True)

print "Repere 2"
print like.model
            
r['gtlike']=sourcedict(like,name,'_at_pulsar')

TS_gtlike=gtlike.like.Ts(name,reoptimize=True)

print "TS_gtlike=%.2f"%TS_gtlike

roi.save("roi_puls_%s.dat"%name)

##################################################################################Morphology###################################################################################


#Test position

#pointlike
#roi=test_location(roi,name,3,0.5,gradient=True,update=True,bandfits=True)

#TS_p=roi.TS(which=name,quick=False,method="minuit")
#roi.save("roi_point_%s.dat"%name)
#r['pointlike']=sourcedict(roi,name,'_localized')

#gtlike

#gtlike=Gtlike(roi)
#like=gtlike.like
#like.fit(covar=True)

#r['gtlike']=sourcedict(like,name,'_localized')

#TS_p_gtlike=gtlike.like.Ts(name,reoptimize=True)

###############################################################################Need to convert point source into a gaussian#
#roi.modify(which=name,spatial_model=Gaussian(0.1))
#roi=ext_func(roi,name,3,gradient=True,bandfits=True)

#TS_gaus=roi.TS(which=name,quick=False,method="minuit")
#roi.save("roi_gauss_%s.dat"%name)
#r['pointlike']=sourcedict(roi,name,'_gaussian')

#gtlike

#gtlike=Gtlike(roi)
#like=gtlike.like
#like.fit(covar=True)

#r['gtlike']=sourcedict(like,name,'_gaussian')

#TS_g_gtlike=gtlike.like.Ts(name,reoptimize=True)

###############################################################################Need to convert gaussian into a disk

#roi.modify(which=name,spatial_model=Disk(0.1))
#roi=ext_func(roi,name,3,gradient=True,bandfits=True)

#TS_disk=roi.TS(which=name,quick=False,method="minuit")
#roi.save("roi_disk_%s.dat"%name)
r['phase_factor']=roi.phase_factor
#r['pointlike']=sourcedict(roi,name,'_Disk')

#gtlike

#gtlike=Gtlike(roi)
#like=gtlike.like
#like.fit(covar=True)

#r['gtlike']=sourcedict(like,name,'_gaussian')

#TS_d_gtlike=gtlike.like.Ts(name,reoptimize=True)


#######################################################################################Spectrum##############################################################################

#######################################################################################Gtlike analysis#######################################################################

#name_roi="roi_puls_%s.dat"%name
#if TS_p_gtlike>TS_gtlike:
#    name_roi="roi_point_%s.dat"%name
#if TS_g_gtlike>(TS_p_gtlike+25.0) and TS_g_gtlike>(TS_gtlike+25.0) :
#    name_roi="roi_gauss_%s.dat"%name
#if TS_d_gtlike>(TS_p_gtlike+25.0) and TS_d_gtlike>(TS_gtlike+25.0) and TS_d_gtlike>TS_g_gtlike :
#    name_roi="roi_disk_%s.dat"%name
#roi=load(roi)
   
#roi.fit(method="minuit",bandfits=True,gradient=True)


####add pointlike upperlimit

#gtlike=Gtlike(roi)
#like=gtlike.like
#like.fit(covar=True)


#TS_gtlike=gtlike.like.Ts(name,reoptimize=False)

# calculate gtlike upper limits ...
if TS_gtlike<25.0:
    liste_source=like.sourceNames()
    for i in range(len(liste_source)):
        spec,lis,lisname=get_spec_par(like,liste_source[i])
        if liste_source[i]!=name:
            for j in range(len(lisname)):
                param=like.par_index(liste_source[i],lisname[j])
                like.freeze(param)

    ul,xx=gtlike_ul(like,args.emin,args.emax,name,sigma=2)
    r['gtlike_ul']=ul
    
# calculate TScutoff ...

#roi.save('roi_%s.dat' % name)

open('results_%s.yaml' % name,'w').write(
    yaml.dump(
        tolist(results)
    )
)

# save stuff out
roi.plot_tsmap(filename='residual_tsmap_0.1_%s.pdf' % name,pixelsize=0.10,size=8)
roi.plot_tsmap(filename='residual_tsmap_0.25_%s.pdf' % name,pixelsize=0.25,size=8)

roi.toRegion('Region_file_%s.reg'%name)

roi.plot_sources(filename='sources_%s.pdf' % name, size=8, label_psf=False)

roi.toXML(filename="srcmodel_res_%s"%name,convert_extended=True)

roi.plot_sed(which=name,filename="sed_%s.png"%name)

#plot_all_seds(roi, filename="allsed_%s.png"%name)

roi.plot_counts_map(filename="cnts_%s.png"%name,countsfile="counts_file_0.1_%s.fits"%name,modelfile="model_file_0.1_%s.fits"%name,pixelsize=0.1,size=10)
roi.zero_source(which=name)
roi.plot_counts_map(filename="cnts_%s.png"%name,countsfile="counts_file_excess_0.1_%s.fits"%name,modelfile="model_file_excess_0.1_%s.fits"%name,pixelsize=0.10,size=10)
roi.plot_tsmap(filename='source_tsmap_0.10%s.pdf' % name, pixelsize=0.10,size=10)
roi.unzero_source(which=name)


roi.plot_counts_map(filename="cnts_%s.png"%name,countsfile="counts_file_%s.fits"%name,modelfile="model_file_%s.fits"%name,pixelsize=0.25,size=10)
roi.zero_source(which=name)
roi.plot_counts_map(filename="cnts_%s.png"%name,countsfile="counts_file_excess_%s.fits"%name,modelfile="model_file_excess_%s.fits"%name,pixelsize=0.25,size=10)
roi.plot_tsmap(filename='source_tsmap_0.25%s.pdf' % name,pixelsize=0.25, size=8)
roi.unzero_source(which=name)

roi.plot_slice(which=name,filename="outslice_%s.png"%name,datafile='slice_points_%s.out'%name)

roi.plot_counts_spectra(filename="Spectra_%s.png"%name)

#sed = SED(like,name, verbosity=True)
#sed.save('sed_gtlike_%s.dat' % name)
#sed.plot('sed_gtlike_%s.pdf' % name) 

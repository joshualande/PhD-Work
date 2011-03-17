from setup_pwn import setup_pwn
from uw.like.SpatialModels import Disk
from uw.like.roi_tsmap import TSCalc,TSCalcPySkyFunction
from argparse import ArgumentParser
from skymaps import SkyImage,SkyDir

from uw.like.sed_plotter import plot_sed
    

parser = ArgumentParser()
parser.add_argument("-l", "--list", required=True, help="List of all yaml sources")
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
args=parser.parse_args()
  
name=args.name

roi=setup_pwn(name,args.list)

p=lambda: roi.print_summary(title='')

# First, calculate upper limit

fit=lambda: roi.fit(method='minuit')
    
fit()

p()

roi.localize(update=True)

p()

if roi.TS(which=name,quick=False) > 16:

    source = roi.get_source(which=name)
    point_position = source.skydir

    roi.modify(which=name,spatial_model=Disk())

    roi.fit_extension(which=name,use_gradient=True)

    ts_ext=roi.TS_ext(which=name,use_gradient=True)

    print 'ts_ext = ',ts_ext

    if ts_ext<16:
        roi.modify(which=name,spatial_model=point_position)

    fit()

    p()

    # save localization results

    



    # make SED

    sedfile="SED_%s.png" % name

    plot_sed(roi,which=name,outdir=sedfile)

    # save spectral values

    model = roi.get_model(which=name)

    print model.i_flux(100,100000,error=True)


    # fit in different energy ranges.


    E_range=[[100.0,1000.0],[1000.0,10000.0],[10000.0,100000.0]]

    for emin,emax in E_range:
        roi.change_binning(fit_emin=emin,fit_emax=emax)

        fit()

        p()

        print "Energy range : emin= %.2f \t emax= %.2f" % (emin,emax)

        ts=roi.TS(which="",quick=False)

        model = roi.get_model(which=name)
        
        p,p_err=model.statistical(absolute=True)

        flux,fluxerr=model.i_flux(emin,emax,error=True)
        print flux

        index,indexerr=p[1],p_err[1]
            
        print "index = %g +/- %g" % (index,indexerr)

    # make 'source' TS map

    roi.change_binning(fit_emin=100,fit_emax=100000)

    roi.zero_source(which=name)

    roi.plot_tsmap(filename='res_tsmap_%s.png' % name,
                   fitsfile='res_tsmap_%s.fits' % name,
                   size=5,title='Residual TS for %s' % name)

    roi.unzero_source(which=name)
    

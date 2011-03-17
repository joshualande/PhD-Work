from setup_pointlike import setup_pointlike
from uw.like.SpatialModels import Disk
from uw.like.roi_tsmap import TSCalc,TSCalcPySkyFunction
from argparse import ArgumentParser
from skymaps import SkyImage,SkyDir
import yaml

from uw.like.sed_plotter import plot_sed
    

parser = ArgumentParser()
parser.add_argument("-l", "--list", required=True, help="List of all yaml sources")
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
args=parser.parse_args()
  
name=args.name

roi=setup_pointlike(name,args.list)

p=lambda: roi.print_summary(title='')

# First, calculate upper limit

fit=lambda: roi.fit(method='minuit')

source=roi.get_source(which=name)
pulsar_position=source.skydir
    
fit()

p()

ts=roi.TS(which=name,quick=False)
print 'Before localizing, the TS is ',ts

roi.zero_source(which=name)
roi.plot_tsmap(filename='res_tsmap_%s.png' % name,
               fitsfile='res_tsmap_%s.fits' % name,
               size=5,title='Residual TS for %s' % name)
roi.unzero_source(which=name)

localize_succeed=True
try:
    roi.localize(which=name,update=True,bandfits=True)
except Exception, err:
    print 'error localizing: %s' % (str(err))
    localize_succeed=True
    print 'Moving back to starting position'
    roi.modify(which=name,skydir=pulsar_position)

roi.save('fit_point_%s.dat' % name)

p()

source=roi.get_source(which=name)
best_fit_point=source.skydir

roi.modify(which=name,spatial_model=Disk())

roi.fit_extension(which=name,bandfits=True)

ts_ext=roi.TS_ext(which=name,bandfits=True)

source=roi.get_source(which=name)
best_fit_extended=source.skydir

roi.save('fit_disk_%s.dat' % name)

print 'ts_ext = ',ts_ext

if ts_ext<16:
    roi.modify(which=name,spatial_model=best_fit_point)

fit()

p()


plot_sed(roi,which=name,outdir="SED_%s.png" % name)

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

    ts=roi.TS(which=name,quick=False)

    model = roi.get_model(which=name)
    
    p,p_err=model.statistical(absolute=True)

    flux,fluxerr=model.i_flux(emin,emax,error=True)
    print flux

    index,indexerr=p[1],p_err[1]
        
    print "index = %g +/- %g" % (index,indexerr)

    roi.zero_source(which=name)
    roi.plot_tsmap(filename='res_tsmap_%s.png' % name,
                   fitsfile='res_tsmap_%s.fits' % name,
                   size=5,title='Residual TS for %s' % name)
    roi.unzero_source(which=name)

# make 'source' TS map

roi.change_binning(fit_emin=100,fit_emax=100000)

    
results=dict(
    pulsar_position_gal=[pulsar_position.l(),pulsar_position.b()],
    name=name,
    localize_succeed=localize_succeed,
    ts_ext=ts_ext,
    best_fit_point_gal=[best_fit_point.l(),best_fit_point.b()],
    best_fit_extended_gal=[best_fit_extended.l(),best_fit_extended.b()]
)

open('results_%s.yaml' % name,'w').write(
    yaml.dump(
        results
    )
)

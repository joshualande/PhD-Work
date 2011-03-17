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


# First, calculate upper limit

fit=lambda: roi.fit(method='minuit')

source=roi.get_source(which=name)
pulsar_position=source.skydir
    
fit()

roi.print_summary()

ts=roi.TS(which=name,quick=False,quiet=True)
print 'Before localizing, the TS is ',ts

roi.zero_source(which=name)
roi.plot_tsmap(filename='res_tsmap_%s.png' % name,
               fitsfile='res_tsmap_%s.fits' % name,
               size=5,title='TS Map of %s' % name)
roi.unzero_source(which=name)

localize_succeed=True
try:
    roi.localize(which=name,update=True,bandfits=True)
except Exception, err:
    print 'error localizing: %s' % (str(err))
    localize_succeed=True
    print 'Moving back to starting position'
    roi.modify(which=name,skydir=pulsar_position)

ts_point = roi.TS(which=name,quick=False,quiet=True)
roi.save('fit_point_%s.dat' % name)

roi.print_summary()

source=roi.get_source(which=name)
best_fit_point=source.skydir

roi.modify(which=name,spatial_model=Disk())

roi.fit_extension(which=name,bandfits=True)

ts_ext=roi.TS_ext(which=name,bandfits=True)
ts_disk = roi.TS(which=name,quick=False,quiet=True)

source=roi.get_source(which=name)
best_fit_extended=source.skydir

roi.save('fit_disk_%s.dat' % name)

p,p_err=source.model.statistical(absolute=True)
flux=source.model.i_flux(100,100000,error=True)
index=[p[1],p_err[1]]

print 'ts_ext = ',ts_ext

if ts_ext<16:
    roi.modify(which=name,spatial_model=best_fit_point)

fit()

roi.print_summary()

plot_sed(roi,which=name,outdir="SED_%s.png" % name)

# save spectral values

model = roi.get_model(which=name)

print model.i_flux(100,100000,error=True)


# fit in different energy ranges.

results=dict(
    pulsar_position_gal=[pulsar_position.l(),pulsar_position.b()],
    name=name,
    localize_succeed=localize_succeed,
    ts_ext=ts_ext,
    best_fit_point_gal=[best_fit_point.l(),best_fit_point.b()],
    best_fit_extended_gal=[best_fit_extended.l(),best_fit_extended.b()],
    flux=flux,
    index=index,
    ts_point=ts_point,
    ts_disk=ts_disk,
    phase_factor=roi.phase_factor
)


E_range=[[100,1000],[1000,10000],[10000,100000]]

for emin,emax in E_range:
    roi.change_binning(fit_emin=emin,fit_emax=emax)

    fit()

    roi.print_summary()

    print "Energy range : emin= %.2f \t emax= %.2f" % (emin,emax)

    results['ts_%g_%g' % (emin,emax)]=roi.TS(which=name,quick=False,quiet=True)

    model = roi.get_model(which=name)
    
    p,p_err=model.statistical(absolute=True)
    results['flux_%g_%g' % (emin,emax)]=model.i_flux(emin,emax,error=True)
    results['index_%g_%g' % (emin,emax)]=[p[1],p_err[1]]

    roi.zero_source(which=name)
    roi.plot_tsmap(filename='res_tsmap_%g_%g_%s.png' % (emin,emax,name),
                   fitsfile='res_tsmap_%g_%g_%s.fits' % (emin,emax,name),
                   size=5,title='TS Map of %s %gMeV to %gMeV' % (name,emin,emax))
    roi.unzero_source(which=name)

roi.change_binning(fit_emin=100,fit_emax=100000)
    

open('results_%s.yaml' % name,'w').write(
    yaml.dump(
        results
    )
)

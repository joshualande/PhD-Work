from setup_pwn import setup_pwn
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

roi=setup_pwn(name,args.list)


results=r={}



source=roi.get_source(which=name)
pulsar_position=source.skydir
    
roi.fit(use_gradient=False)

roi.print_summary()

r['ts_at_pulsar'] = roi.TS(which=name,quick=False,quiet=True)
r['flux_at_pulsar'],r['flux_at_pulsar_err']=source.model.i_flux(100,100000,error=True)
r['index_at_pulsar'],r['index_at_pulsar_err']=source.model['index'],source.model.error('index')

roi.plot_tsmap(filename='residual_tsmap_%s.pdf' % name, size=8)
roi.zero_source(which=name)
roi.plot_tsmap(filename='source_tsmap_%s.pdf' % name, size=8)
roi.unzero_source(which=name)

roi.plot_sources(filename='sources_%s.pdf' % name, size=8, label_psf=False)

roi.plot_sed(which=name,filename='sed_%s.pdf' % name)

roi.save('roi_%s.dat' % name)

open('results_%s.yaml' % name,'w').write(
    yaml.dump(
        results
        )
    )

from setup_pwn import setup_pwn
from uw.like.SpatialModels import Disk

from argparse import ArgumentParser

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

    # get spectral values

    model = roi.get_model(which=name)

    print model.i_flux(100,100000)

    # make residual TS map


    # fit in different energy ranges.

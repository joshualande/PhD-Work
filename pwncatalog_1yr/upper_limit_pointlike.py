from argparse import ArgumentParser
from setup_pointlike import setup_pointlike
import yaml

parser = ArgumentParser()
parser.add_argument("-l", "--pwnlist", required=True, help="List of all yaml sources")
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
args=parser.parse_args()

fit=lambda: roi.fit(method='minuit')

name=args.name
pwnlist=args.pwnlist

roi=setup_pointlike(name,pwnlist)

model=roi.get_model(which=name)
model.setp(1,2)
model.freeze(1)
roi.modify(which=name,model=model)

roi.print_summary()

fit()

roi.print_summary()

ul=roi.upper_limit(which=args.name)
ts=roi.TS(which=name,quick=False,quiet=True)


results=dict(
    name=name,
    upper_limit=float(ul),
    TS=float(ts)
)

print "upperlimit = %g" % ul

E_range=[[100,1000],[1000,10000],[10000,100000]]

for emin,emax in E_range:
    roi.change_binning(fit_emin=emin,fit_emax=emax)
    fit()

    ul=roi.upper_limit(which=args.name)
    ts=roi.TS(which=name,quick=False,quiet=True)

    results['upper_limit_%g_%g' % (emin,emax)] = float(ul)
    results['TS_%g_%g' % (emin,emax)] = float(ts)

    print "upperlimit (%g to %g) = %g" % (emin,emax,ul)
roi.change_binning(fit_emin=100,fit_emax=100000)

open('results_%s.yaml' % name,'w').write(
    yaml.dump(
        results
    )
)

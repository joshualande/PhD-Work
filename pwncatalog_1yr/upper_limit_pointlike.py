from argparse import ArgumentParser
from setup_pointlike import setup_pointlike
import yaml

parser = ArgumentParser()
parser.add_argument("-l", "--pwnlist", required=True, help="List of all yaml sources")
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
args=parser.parse_args()

print "----Upperlimit with phase cut----"

name=args.name
pwnlist=args.pwnlist

roi=setup_pointlike(name,pwnlist)

roi.print_summary()

roi.fit(method='minuit')

roi.print_summary()

ul=roi.upper_limit(which=args.name)
ts=roi.TS(which=name,quick=False,quiet=True)

print "upperlimit with phase cut = %g" % ul

results=dict(
    name=name,
    ul_100_100000=ul,
    TS_100_100000=ts
)

open('results_%s.yaml' % name,'w').write(
    yaml.dump(
        results
    )
)

#print "Upperlimit without phase cut----"

#roi=setup_pwn(args.name,args.list,phasing=False)

#roi.fit

#ul2=roi.upperlimit(which='args.name')

#print "upperlimit without phasecut=%.2f"%(ul2)

#a=[ul,ul2]

#uplim=min(a)

#print "Upperlimit = %.2f"%(uplim)

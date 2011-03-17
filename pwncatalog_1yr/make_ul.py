from argparse import ArgumentParser
from setup_pwn import setup_pwn

parser = ArgumentParser()
parser.add_argument("-l", "--pwnlist", required=True, help="List of all yaml sources")
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
args=parser.parse_args()

print "----Upperlimit with phase cut----"

name=args.name
pwnlist=args.pwnlist

roi=setup_pwn(name,pwnlist)

roi.fit(method='minuit')

ul=roi.upper_limit(which=args.name)
ts=roi.TS(which=name,quick=False)

print "upperlimit with phase cut= %.2f"%(ul)

results={'ul_100_100000':ul,'TS':ts}

open('results_%s.yaml' % name).write(
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

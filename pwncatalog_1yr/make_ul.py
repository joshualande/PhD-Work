from argparse import ArgumentParser
from setup_pwn import setup_pwn

parser = ArgumentParser()
parser.add_argument("-l", "--list", required=True, help="List of all yaml sources")
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
args=parser.parse_args()

print "----Upperlimit with phase cut----"

roi=setup_pwn(args.name,args.list)

roi.fit(method='minuit')

ul=roi.upper_limit(which=args.name)
print "upperlimit with phase cut= %.2f"%(ul)

#print "Upperlimit without phase cut----"

#roi=setup_pwn(args.name,args.list,phasing=False)

#roi.fit

#ul2=roi.upperlimit(which='args.name')

#print "upperlimit without phasecut=%.2f"%(ul2)

#a=[ul,ul2]

#uplim=min(a)

#print "Upperlimit = %.2f"%(uplim)

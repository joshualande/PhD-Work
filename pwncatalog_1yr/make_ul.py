from argparse import ArgumentParser
from setup_pwn import setup_pwn

parser = ArgumentParser()
parser.add_argument("-l", "--list", required=True, help="List of all yaml sources")
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
args=parser.parse_args()

roi=setup_pwn(args.name,args.list)

roi.fit()

ul=roi.upper_limit(which='args.name')
print ul

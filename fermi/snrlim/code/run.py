from argparse import ArgumentParser

from lande.fermi.pipeline.snrlim.main import run

parser = ArgumentParser()
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
parser.add_argument("--snrdata", required=True)
parser.add_argument("--latdata", required=True)
args=parser.parse_args()

run(name=args.name, snrdata=args.snrdata, latdata=args.latdata)

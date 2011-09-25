from argparse import ArgumentParser
import yaml

parser = ArgumentParser()
parser.add_argument("--snrdata", required=True)
parser.add_argument("--snr", required=True)
args=parser.parse_args()

snr=args.snr
snrdata=args.snrdata

from setup_snr import setup_snr
roi=setup_snr(snr,snrdata)


roi.print_summary()

roi.fit()

roi.print_summary()


f=open('results_%s.yaml' % snr)
yaml.dump(
    dict(
        name=snr
        ),
    f)


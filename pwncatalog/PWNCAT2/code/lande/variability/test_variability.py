import yaml
import numpy as np
np.seterr(all='ignore')

from argparse import ArgumentParser

import lande_variability

from uw.like.roi_save import load

parser = ArgumentParser()
parser.add_argument("--pwndata", required=True)
parser.add_argument("-n", "--name", required=True)
parser.add_argument("--analysis-dir", required=True)
args=parser.parse_args()


name=args.name
roi = load('%s/%s/roi_at_pulsar_%s.dat' % (args.analysis_dir,name,name))

roi.print_summary()
roi.fit(use_gradient=False)
roi.print_summary()

v = lande_variability.VariabilityTester(roi,name,
                                        nbins=36)

print v.todict()

d=v.todict()
open('results_%s.yaml' % name,'w').write(
    yaml.dump(d)
)

v.plot(filename='variability_%s.pdf' % name)

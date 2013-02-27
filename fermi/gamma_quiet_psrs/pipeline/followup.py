#!/usr/bin/env python

from argparse import ArgumentParser

from lande.utilities.argumentparsing import parse_strip_known_args

from lande.fermi.pipeline.gamma_quiet_psrs.analysis.pipeline import Pipeline

parser = ArgumentParser()
parser.add_argument("--hypothesis", required=True, choices=['at_pulsar', 'point', 'extended'])
parser.add_argument("--followup", required=True, choices=['tsmaps','plots', 'gtlike'])
parser.add_argument("--size", type=float)
followup_args = parse_strip_known_args(parser)
hypothesis = followup_args.hypothesis
followup =followup_args.followup
size = followup_args.size

kwargs = Pipeline.get_kwargs()

pipeline=Pipeline(**kwargs)

if followup == 'gtlike':
    pipeline.gtlike_followup(hypothesis=hypothesis)
elif followup == 'variability':
    pipeline.variability_followup(hypothesis=hypothesis)
elif followup == 'tsmaps':
    pipeline.tsmaps_followup(hypothesis=hypothesis, size=size)
elif followup == 'plots':
    pipeline.plots_followup(hypothesis=hypothesis, size=size)

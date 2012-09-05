#!/usr/bin/env python

from argparse import ArgumentParser

from lande.utilities.argumentparsing import parse_strip_known_args

from lande.fermi.pipeline.pwncat2.analysis.pipeline import Pipeline


parser = ArgumentParser()
parser.add_argument("--hypothesis", required=True, choices=['at_pulsar', 'point', 'extended'])
parser.add_argument("--followup", required=True, choices=['tsmaps','plots', 'gtlike', 'variability','extul'])
followup_args = parse_strip_known_args(parser)
hypothesis = followup_args.hypothesis
followup =followup_args.followup

kwargs = Pipeline.get_kwargs()

pipeline=Pipeline(**kwargs)

if followup == 'gtlike':
    pipeline.gtlike_followup(hypothesis=hypothesis)
elif followup == 'variability':
    pipeline.variability_followup(hypothesis=hypothesis)
elif followup == 'tsmap':
    pipeline.tsmap_followup(hypothesis=hypothesis)
elif followup == 'plots':
    pipeline.plots_followup(hypothesis=hypothesis)
elif followup == 'extul':
    pipeline.extul_followup(hypothesis=hypothesis)

#!/usr/bin/env python

from argparse import ArgumentParser

from lande.fermi.pipeline.radiopsrs.analysis.pipeline import Pipeline

kwargs = Pipeline.get_kwargs()

pipeline=Pipeline(**kwargs)
pipeline.main()

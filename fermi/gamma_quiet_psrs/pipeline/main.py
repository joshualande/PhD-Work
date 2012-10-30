#!/usr/bin/env python

from argparse import ArgumentParser

from lande.fermi.pipeline.gamma_quiet_psrs.analysis.pipeline import Pipeline

kwargs = Pipeline.get_kwargs()

pipeline=Pipeline(**kwargs)
pipeline.main()

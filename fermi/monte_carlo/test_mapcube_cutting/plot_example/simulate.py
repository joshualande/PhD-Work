#!/usr/bin/env python

from argparse import ArgumentParser
import shutil
from tempfile import mkdtemp
from os.path import join

import yaml
import numpy as np

from skymaps import SkyDir

from uw.like.Models import Constant
from uw.like.roi_monte_carlo import SpectralAnalysisMC
from uw.like.pointspec import DataSpecification


from lande.fermi.data.catalogs import get_2fgl
from lande.fermi.likelihood.diffuse import get_background, get_sreekumar
from lande.fermi.likelihood.save import diffusedict, skydirdict
from lande.utilities.random import random_on_sphere
from lande.utilities.tools import savedict



np.random.seed(0)

emin=1e2
emax=1e5

diffdir='/afs/slac/g/glast/groups/diffuse/rings/2year/'

diffuse = get_dfeault_diffuse
iso = get_background(join(diffdir,'isotrop_2year_P76_source_v0.txt'))
ring = get_background(join(diffdir,'ring_2year_P76_v0.fits'))
sreekumar = get_sreekumar(diff_factor=1)

catdict = get_2fgl()
ft2 = catdict['ft2'],
ltcube = catdict['ltcube'],

roi_dir = SkyDir(0,0, SkyDir.GALACTIC)

ft1='ft1.fits',
m=MonteCarlo(
    emin = emin,
    emax = emax,
    irf='P7SOURCE_V6',
    roi_dir=roi_dir,
    maxROI=10,
    seed=0,
    ft1=ft1,
    ft2=ft2,
    gtifile = ltcube,
    savedir='data'
    )

ds = DataSpecification(
    ft1files = join(tempdir,'ft1.fits'),
    ft2files = ft2,
    ltcube = ltcube,
    binfile = join(tempdir,'binned.fits'))


sa = SpectralAnalysis(ds,
    emin = emin,
    emax = emax,
    irf='P7SOURCE_V6',
    roi_dir=roi_dir,
    minROI=10,
    maxROI=10,
)

roi = sa.roi(roi_dir=roi_dir, diffuse_sources = diffuse_sources)

roi.plot_counts_map(filename='counts_map_%s.png'  % istr, **plot_kwargs)


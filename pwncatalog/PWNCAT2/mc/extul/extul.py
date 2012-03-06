from os.path import join
import yaml
import traceback
import sys
from argparse import ArgumentParser
from tempfile import mkdtemp
from shutil import rmtree

import numpy as np
np.seterr(all='ignore')

from skymaps import SkyDir
from skymaps import IsotropicPowerLaw

from uw.like.roi_diffuse import DiffuseSource
from uw.like.roi_extended import ExtendedSource
from uw.like.Models import PowerLaw
from uw.like.SpatialModels import Disk
from uw.like.roi_monte_carlo import MonteCarlo
from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.pointspec_helpers import PointSource

from lande.utilities.tools import savedict
from lande.fermi.likelihood.diffuse import get_sreekumar
from lande.fermi.likelihood.catalogs import get_2fgl
from lande.fermi.likelihood.tools import force_gradient
from lande.fermi.likelihood.save import sourcedict, spectrum_to_dict, pointlike_model_to_flux

force_gradient(use_gradient=False)

parser = ArgumentParser()
parser.add_argument("i",type=int)
parser.add_argument("--type", required=True)
parser.add_argument("--index",type=float, required=True)
parser.add_argument("--min-flux",type=float, required=True)
parser.add_argument("--max-flux",type=float, required=True)
parser.add_argument("--min-extension",type=float, required=True)
parser.add_argument("--max-extension",type=float, required=True)
args=parser.parse_args()

i=args.i
min_flux_mc = args.min_flux
max_flux_mc = args.max_flux

min_extension = args.min_extension
max_extension = args.max_extension

np.random.seed(i)

extensions = np.linspace(min_extension, max_extension, 2**3+1)
np.random.shuffle(extensions)

# formula to interpolate from the flux at lowest to highest extension
flux_mc = lambda extension: np.exp(np.log(min_flux_mc) + 
                                   (np.log(max_flux_mc) - np.log(min_flux_mc))*\
                                   (extension-min(extensions))/(max(extensions)-min(extensions)))

index_mc = args.index

emin=1e2
emax=1e5
irf="P7SOURCE_V6"

skydir_mc = SkyDir()

bg = get_sreekumar()

cat = get_2fgl()
ft2 = cat['ft2']
ltcube = cat['ltcube']

results = []

for extension_mc in extensions:

    print 'Looping over extension_mc=%g' % extension_mc

    model_mc = PowerLaw(index=index_mc)
    model_mc.set_flux(flux_mc(extension_mc), emin, emax)

    r = dict(
        type = args.type,
        mc = dict(
            extension=extension_mc,
            gal=[ skydir_mc.l(), skydir_mc.b() ],
            cel=[ skydir_mc.ra(), skydir_mc.dec() ],
            model=spectrum_to_dict(model_mc),
            flux=pointlike_model_to_flux(model_mc, emin, emax),
        )
    )

    tempdir = mkdtemp()

    point = 'point'
    ps = PointSource(
        name=point,
        model=model_mc.copy(),
        skydir = skydir_mc
    )

    extended = 'extended_%f' % extension_mc
    if extension_mc > 0:
        sm = Disk(sigma=extension_mc, center=skydir_mc)
        es = ExtendedSource(
            name=extended,
            model=model_mc,
            spatial_model=sm,
        )
        sim_es = es
    else:
        # If the source has no extension,
        # simulate the source as point-like
        # but create a small extended
        # source for the later extension test
        sm = Disk(sigma=1e-10, center=skydir_mc)
        es = ExtendedSource(
            name=extended,
            model=model_mc,
            spatial_model=sm,
        )
        sim_es = ps

    ft1 = join(tempdir,'ft1.fits')
    binfile = join(tempdir, 'binned.fits')

    mc=MonteCarlo(
        sources=[bg.copy(), sim_es.copy()],
        seed=i,
        irf=irf,
        ft1=ft1,
        ft2=ft2,
        roi_dir=skydir_mc,
        maxROI=10,
        emin=emin,
        emax=emax,
        gtifile=ltcube,
        )

    mc.simulate()

    print 'Done Simulating, now fitting'


    ds=DataSpecification(
        ft1files = ft1,
        ft2files = ft2,
        ltcube   = ltcube,
        binfile  = binfile)

    sa=SpectralAnalysis(ds,
        irf         = irf,
        roi_dir     = skydir_mc,
        maxROI      = 10,
        minROI      = 10,
        event_class = 0,
    )

    roi=sa.roi(
        roi_dir=skydir_mc,
        diffuse_sources=[bg.copy()],
        fit_emin = emin,
        fit_emax = emax
    )

    roi.add_source(ps.copy())

    roi.print_summary()
    roi.fit()
    roi.print_summary()

    try:
        roi.localize(which=point, update=True)
    except Exception, ex:
        traceback.print_exc(file=sys.stdout)

    roi.fit()
    roi.print_summary()

    r['point'] = sourcedict(roi,point)

    r['extension_ul'] = roi.extension_upper_limit(which=point)

    roi.del_source(point)

    roi.add_source(es.copy())

    roi.print_summary()
    roi.fit()
    roi.print_summary()
    roi.fit_extension(which=extended)
    roi.fit()
    roi.print_summary()

    fit_sm = roi.get_source(extended)

    r['extended'] = sourcedict(roi,extended)

    r['TS_ext'] = 2*(r['extended']['logLikelihood'] - r['point']['logLikelihood'])

    # Extension upper limit

    # Then, compute TS_point & TS_ext

    results.append(r)

    rmtree(tempdir)

    # Save results to file
    savedict('results.yaml',results)

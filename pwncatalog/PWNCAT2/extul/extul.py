from os.path import join
import yaml

import numpy as np

from skymaps import SkyDir
from skymaps import IsotropicPowerLaw

from uw.like.roi_diffuse import DiffuseSource
from uw.like.roi_extended import ExtendedSource
from uw.like.Models import PowerLaw
from uw.like.SpatialModels import Disk
from uw.like.roi_monte_carlo import MonteCarlo
from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.pointspec_helpers import PointSource

from tempfile import mkdtemp
from shutil import rmtree

from lande_toobag import todict


i=0

emin=1e2
emax=10**5.5
#emax=10**3
irf="P7SOURCE_V6"

skydir_mc = SkyDir()



bg = DiffuseSource(
    IsotropicPowerLaw(1.5e-5,2.1),
    PowerLaw(p=[1,1],index_offset=1),
    'Isotropic Diffuse x1'
)

catalog_basedir = "/afs/slac/g/glast/groups/catalog/P7_V4_SOURCE/"
ft2    = join(catalog_basedir,"ft2_2years.fits")
ltcube = join(catalog_basedir,"ltcube_24m_pass7.4_source_z100_t90_cl0.fits")



results = []

extensions = np.linspace(0.1,2.0,20)

for extension in extensions[0:1]:

    tempdir = mkdtemp()

    model = PowerLaw(gamma=2)
    model.set_flux(1e-8, 1e2, 10**5.5)

    spatial_model = Disk(sigma=extension, center=skydir_mc)

    ext = ExtendedSource(
        name='extended',
        model=model,
        spatial_model=spatial_model,
    )

    ft1 = join(tempdir,'ft1.fits')
    binfile = join(tempdir, 'binned.fits')

    ft2 = join(tempdir, 'ft2.fits')
    mc=MonteCarlo(
        diffuse_sources=[bg.copy(), ext.copy()],
        seed=i,
        irf=irf,
        ft1=ft1,
        ft2=ft2,
        roi_dir=skydir_mc,
        maxROI=15,
        emin=emin,
        emax=emax,

        tstart=0,   
        tstop=604800,
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

    ps = PointSource(
        name='point',
        model=model,
        skydir = skydir_mc
    )

    # Fit point-like source

    # Extension upper limit

    # Then, compute TS_point & TS_ext


    r = dict(
        extension=extension
        gal_mc = [ skydir_mc.l(), skydir.b()]
    )

    results.append(r)

    rmtree(tempdir)

yaml.dump(open('results.yaml')).write(
    todict(results)
)

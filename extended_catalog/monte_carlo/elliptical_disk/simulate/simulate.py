from os.path import join, exists
from argparse import ArgumentParser
from tempfile import mkdtemp

from skymaps import SkyDir

from uw.like.pointspec import DataSpecification, SpectralAnalysis
from uw.like.roi_state import PointlikeState
from uw.like.roi_catalogs import Catalog2FGL
from uw.like.SpatialModels import EllipticalRing, EllipticalDisk, Disk, Gaussian
from uw.like.pointspec_helpers import get_default_diffuse
from uw.like.roi_monte_carlo import MonteCarlo

from likelihood_tools import force_gradient, sourcedict, tolist
force_gradient(use_gradient=False)

parser = ArgumentParser()
parser.add_argument("i", type=int)
args=parser.parse_args()
i=args.i
istr='%07d' % i


diffuse_sources = get_default_diffuse(diffdir='$FERMI/diffuse',
                                      gfile='ring_2year_P76_v0.fits',
                                      ifile='isotrop_2year_P76_source_v0.txt')
diffuse_sources = diffuse_sources[1:]


catalog=Catalog2FGL('$FERMI/catalogs/gll_psc_v05.fit',
                    latextdir='$FERMI/extended_archives/gll_psc_v05_templates')

name='W44'
w44_2FGL=catalog.get_source(name)

# Replace with analytic shape
skydir=SkyDir(283.98999,1.355)
major=0.3
minor=0.19
elliptical_ring = EllipticalRing(major_axis=major,
                      minor_axis=minor,
                      pos_angle=-33,
                      fraction=0.75,
                      center=skydir)

# Similarly shaped elliptical disk
elliptical_disk = EllipticalDisk(major_axis=major,
                      minor_axis=minor,
                      pos_angle=-33,
                      center=skydir)

# Simiarly shaped disk
disk = Disk(sigma=np.sqrt(major*minor), center=skydir)
gauss = Gaussian(sigma=np.sqrt(major*minor)*(Disk.x68/Gaussian.x68))

# Simulate with elliptical ring spatial model predicted by 2FGL
w44_2FGL.spatial_model = elliptical_ring

diffuse_sources.append(w44_2FGL.copy())

catalog_basedir = "/afs/slac/g/glast/groups/catalog/P7_V4_SOURCE"
ft2 = join(catalog_basedir,"ft2_2years.fits")
ltcube = join(catalog_basedir,"ltcube_24m_pass7.4_source_z100_t90_cl0.fits")


#tempdir=mkdtemp(prefix='/scratch/')
tempdir='savedir'
ft1 = join(tempdir,'ft1.fits')

emin=1e2
emax=1e5

irf='P7SOURCE_V6'
if not exists(ft1):
    mc=MonteCarlo(
        savedir=tempdir,
        sources=diffuse_sources,
        seed=i,
        irf=irf,
        ft1=ft1,
        ft2=ft2,
        roi_dir=skydir,
        maxROI=15,
        emin=emin,
        emax=emax)
    mc.simulate()


binfile = join(tempdir,'binned.fits')
ds = DataSpecification(
    ft1files = ft1,
    ft2files = ft2,
    binfile = binfile,
    ltcube = ltcube)

sa = SpectralAnalysis(ds,
                      emin=emin,
                      emax=emax,
                      binsperdec=4,
                      event_class=0,
                      roi_dir = skydir,
                      minROI=10,
                      maxROI=10,
                      irf=irf)

roi = sa.roi(
    point_sources=[],
    diffuse_sources=diffuse_sources,
)

likelihood_state = PointlikeState(roi)

results = r = dict()

results['mc'] = sourcedict(roi, name)

print roi

def fit(spatial_model):
    type=spatial_model.name
    print 'Fitting %s with %s spatial model' % (name,type)

    roi.modify(which=name, spatial_model=spatial_model)
    likelihood_state.restore(just_spectra=True)

    roi.fit()
    roi.fit_extension(which=name)
    roi.fit()
    roi.print_summary(galactic=True)
    results[type] = sourcedict(roi,name)

    open('results_%s.yaml' % istr).write(yaml.dump(tolist(results)))

fit(elliptical_ring)
fit(elliptical_disk)
fit(disk)
fit(gauss)

from os.path import join
from argparse import ArgumentParser
from tempfile import mkdtemp

from skymaps import SkyDir

from uw.like.roi_catalogs import Catalog2FGL
from uw.like.pointspec_helpers import get_default_diffuse

parser = ArgumentParser()
parser.add_argument("i",type=int)
args=parser.parse_args()
i=args.i
istr='%07d' % i


diffuse_sources = get_default_diffuse(diffdir='$FERMI/diffuse',
                                      gfile='ring_2year_P76_v0.fits',
                                      ifile='isotrop_2year_P76_source_v0.txt')


catalog=Catalog2FGL('$FERMI/catalogs/gll_psc_v05.fit',
                    latextdir='$FERMI/extended_archives/gll_psc_v05_templates')

w44=catalog.get_source('W44')

# Replace with analytic shape
skydir=SkyDir(283.98999,1.355)
w44.spatial_model = EllipticalRing(major_axis=0.30,
                          minor_axis=0.19,
                          pos_angle=-33,
                          fraction=0.75,
                          center=skydir)


print w44_ring

diffuse_sources.append(
    w44)

catalog_basedir = "/nfs/slac/g/ki/ki03/lande/fermi_data/catalog_mirror/catalog_jan_31_2011/P7_V4_SOURCE/"
ft2 =   join(catalog_basedir,"ft2_2years.fits")
ltcube   = join(catalog_basedir,"ltcube_24m_pass7.4_source_z100_t90_cl0.fits")


tempdir=mkdtemp(prefix='/scratch/')
ft1 = join(tempdir,'ft1.fits')

mc=MonteCarlo(
    diffuse_sources=diffuse_sources,
    seed=i,
    irf=irf,
    ft1=ft1,
    ft2=ft2,
    roi_dir=skydir,
    maxROI=10,
    emin=emin,
    emax=emax)
mc.simulate()


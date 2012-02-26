from os.path import join
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("i",type=int)
args=parser.parse_args()
i=args.i
istr='%07d' % i


diffuse_sources = get_default_diffuse(

catalog_basedir = "/nfs/slac/g/ki/ki03/lande/fermi_data/catalog_mirror/catalog_jan_31_2011/P7_V4_SOURCE/"
ft2 =   join(catalog_basedir,"ft2_2years.fits")
ltcube   = join(catalog_basedir,"ltcube_24m_pass7.4_source_z100_t90_cl0.fits")


tempdir=mkdtemp(prefix='/scratch/')
ft1 = join(tempdir,'ft1.fits')

skydir = SkyDir()

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


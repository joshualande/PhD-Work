from os.path import expandvars as e, join as j

import pyfits
import pylab as P
import yaml
import numpy as np

from skymaps import SkyDir

from uw.like.pointspec import DataSpecification
from uw.like.pointspec_helpers import get_default_diffuse
from uw.like.roi_catalogs import Catalog2FGL

from lande_cache import SpectralAnalysisCache
import snr_contour_loader

#name='G34.7-0.4'
name='G260.4-3.4'

l = lambda f: yaml.load(open(e(f)))

snrdata=l('$superfile/snrdata.yaml')
templates=l('$superfile/snrtemplates.yaml')

snr=snrdata[name]
skydir=SkyDir(*snr['cel'])
radius=snr['radius']

pwncat2='/nfs/slac/g/ki/ki03/lande/fermi/data/data/PWNCAT2/nov_30_2011/'
ds=DataSpecification(
    ft1files=j(pwncat2,'ft1_PWNCAT2_allsky.fits'),
    binfile=j(pwncat2,'binned_4.fits'),
    ft2files=j(pwncat2,'ft2_PWNCAT2_allsky.fits'),
    ltcube=j(pwncat2,'ltcube_PWNCAT2_allsky.fits'))

sa=SpectralAnalysisCache(ds,
                         binsperdec  = 4,
                         roi_dir     = skydir,
                         irf         = 'P7SOURCE_V6',
                         maxROI      = 10,
                         minROI      = 10,
                         event_class = 0,
                         cachedir    = 'cache')


diffuse_sources = diffuse_sources = get_default_diffuse(
    diffdir=e('$FERMI/diffuse'),
    gfile='ring_2year_P76_v0.fits',
    ifile='isotrop_2year_P76_source_v0.txt')

catalogs = Catalog2FGL('$FERMI/catalogs/gll_psc_v05.fit',
                       latextdir='$FERMI/extended_archives/gll_psc_v05_templates/')

roi = sa.roi(
    catalogs = catalogs,
    diffuse_sources = diffuse_sources,
    fit_emin = 1e3,
    fit_emax = 1e5)

print 'making plot'

plot_size = max(radius*4, 3)
smooth=roi.plot_sources(size=plot_size)

print 'overlay contours'
if templates.has_key(name):
    template = templates[name]
    if template.has_key('contours'):
        contours = template['contours']

        for contour_type, contour in contours.items():
            contour_loader = snr_contour_loader.factory(**contour)
            contour_loader.overlay(smooth.axes)

P.savefig("counts_%s.png" % name)

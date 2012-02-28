# Simple code just compares 2FGL template of W44 with my analytic shape
from os.path import expandvars
from skymaps import SkyDir, SkyImage

from uw.like.roi_catalogs import Catalog2FGL
from uw.like.SpatialModels import EllipticalRing

from shutil import copy

# First, load 2FGL w44
catalog=Catalog2FGL('$FERMI/catalogs/gll_psc_v05.fit',
                    latextdir='$FERMI/extended_archives/gll_psc_v05_templates')

w44=catalog.get_source('W44')
w44_spatial_map = w44.spatial_model
w44_file=expandvars(w44_spatial_map.file)

# Define a new analytic shape
w44_ring = EllipticalRing(major_axis=0.30,
                          minor_axis=0.19,
                          pos_angle=-33,
                          fraction=0.75,
                          center=SkyDir(283.98999,1.355))

# Create a new spatial map which is filled with new analytic shape
new_template='temp_template.fits'
copy(w44_file,new_template)
x=SkyImage(new_template)
x.fill(w44_ring.get_PySkyFunction())
x.save()

print 'original',file
print 'new',new_template

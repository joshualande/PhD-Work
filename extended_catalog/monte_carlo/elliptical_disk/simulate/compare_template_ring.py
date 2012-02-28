""" Code to compares 2FGL template of W44 with my defiend analytic shape of w44.

    Author: Joshua Lande <joshualande@gmail.com>
"""

from shutil import copy
from os.path import expandvars

from skymaps import  SkyImage

from simulate import get_catalog, get_spatial

# First, load 2FGL w44
catalog=get_catalog()


w44=catalog.get_source('W44')
w44_spatial_map = w44.spatial_model
w44_file=expandvars(w44_spatial_map.file)

# Define a new analytic shape
w44_ring = get_spatial('EllipticalRing')

# Create a new spatial map with same binning as 2FGL tempalte, but filled with new analytic shape
new_template='pointlike_ring_template.fits'
copy(w44_file,new_template)
x=SkyImage(new_template)
x.fill(w44_ring.get_PySkyFunction())
x.save()

print 'original',w44_file
print 'new',new_template

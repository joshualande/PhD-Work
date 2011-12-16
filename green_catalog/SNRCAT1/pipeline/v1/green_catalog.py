
import os
import numpy as np
import pyfits

from skymaps import SkyDir
from uw.like.Models import PowerLaw
from uw.like.pointspec_helpers import PointSource

class GreenCatalog(object):

    def __init__(self,green_catalog):

        self.green_catalog = os.path.expandvars(green_catalog)
        self.__parse_catalog_(self.green_catalog)

    def __parse_catalog_(self,green_catalog):

        table = pyfits.open(green_catalog)[1].data

        nameA = np.char.strip(table.field('nameA'))
        nameB = np.char.strip(table.field('nameB'))

        self.names = reduce(np.char.add,['G',nameA,nameB])

        self.nicknames = table.field('name')

        h = table.field('h').astype(float)
        min = table.field('min').astype(float)
        sec = table.field('sec').astype(float)

        ras = 15*(h+(min+sec/60)/60.)

        dd = table.field('dd').astype(float)
        mm = table.field('mm').astype(float)

        decs = dd - mm/60.

        self.skydirs = [SkyDir(ra,dec) for ra,dec in zip(ras,decs)]

    def get_names(self):

        return self.names.tolist()

    def get_source(self,name,model=None):

        if model is None: model=PowerLaw()

        return PointSource(name=name,model=model,skydir=self.get_skydir(name))

    def get_skydir(self,name):
        index = np.where(self.names==name)[0]
        if len(index)!=1: raise Exception("Cannot uniquely find source %s." % name)
        return self.skydirs[index]


if __name__ == '__main__':

    cat=GreenCatalog('$FERMI/catalogs/Green_cat.fits')

    for name,dir in zip(cat.names,cat.skydirs):
        print '%20s %10.1f %10.1f %10.2f %10.2f' % (name,dir.l(),dir.b(),dir.ra(),dir.dec())

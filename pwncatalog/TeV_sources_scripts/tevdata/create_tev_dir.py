import os,sys
import numpy as np
np.seterr(all='ignore')
import yaml
from skymaps import SkyDir
sources=yaml.load(open("tev_galactic_sources.yaml"))
file=open("tev_dir.yaml","w")

for name in sources.keys():
    file.write("%s:\n"%name)
    dir=sources[name]['gal']
    direct=SkyDir(dir[0],dir[1],SkyDir.GALACTIC)
    ra,dec=direct.ra(),direct.dec()
    file.write("  cel: [%f,%f]\n"%(ra,dec))
    file.write("  ft1: /afs/slac/g/glast/users/rousseau/TeV_sources/ft1s/mktime_%s.fits\n"%name)
    file.write("  ft2: /u/gl/lande/public_html/fermi/data/data/PWNCAT2/nov_30_2011/ft2_PWNCAT2_allsky.fits\n")
    file.write("  ltcube: /afs/slac/g/glast/users/rousseau/TeV_sources/ltcubes/ltcube_%s.fits\n"%name)


file.close()

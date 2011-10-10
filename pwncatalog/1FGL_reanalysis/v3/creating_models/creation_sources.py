import glob
import yaml
from creation_srcmdl import *
pwndata="/afs/slac/g/glast/users/rousseau/svn/trunk/pwncatalog/1FGL_reanalysis/v3.5/pwndata/pwndata_v1.yaml"
dir_cat="/afs/slac/g/glast/users/rousseau/catalogs/gll_psc11month_v4r4_flags_v4r4p1.fit"

pwnfile=yaml.load(open(pwndata))
for name in pwnfile.keys():
        print name
        pos=pwnfile[name]['dir']
        ra=pos[0]
        dec=pos[1]
        roi=15.0
        distmin=0.1
        outputfile="%s_model_cat.xml"%name
	creation_srcmdl(dir_cat,ra,dec,roi,distmin,name,outputfile,1.0e2,1.0e5)

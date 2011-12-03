import numpy as np

emin=1000
fit_emin=1000

index = 2
diff_factor=10


import sys
sys.path.append('/u/gl/lande/work/fermi/extended_catalog/monte_carlo/sensitivity/v13/plot')
from sensitivity import get_sensitivity

exts=np.sort(np.append(np.arange(0.1,2.1,0.1),[0.15,0.25,0.35]))
f2yrs=np.asarray([get_sensitivity(e,index,emin,fit_emin,diff_factor,'2') for e in exts])
f10yrs=np.asarray([get_sensitivity(e,index,emin,fit_emin,diff_factor,'10') for e in exts])

d=dict(exts=exts.tolist(),
       f2yrs=f2yrs.tolist(),
       f10yrs=f10yrs.tolist())

import yaml
print yaml.dump(d)

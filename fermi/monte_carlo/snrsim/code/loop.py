from os.path import join

from lande.utilities.jobtools import JobBuilder

#params=dict(source=['W44','IC443'])
#params['spectrum','normalization']=[['PowerLaw','same_prefactor'],
#                                    ['PowerLaw','same_flux'],
#                                    ['SmoothBrokenPowerLaw','standard'],
#                                   ]
#
#j = JobBuilder(savedir='$snrsim_sims/v1',
#               code='$snrsim_code/simulate.py',
#               num=5,
#               params=params)
#j.build()


#params=dict(source=['W44','IC443'])
#params['spectrum','normalization']=[['PowerLaw','same_prefactor'],
#                                    ['PowerLaw','same_flux'],
#                                    ['SmoothBrokenPowerLaw','standard'],
#                                   ]
#
#j = JobBuilder(savedir='$snrsim_sims/v2',
#               code='$snrsim_code/simulate.py',
#               num=5,
#               params=params)
#j.build()


#params=dict(source=['W44','IC443'])
#params['spectrum','normalization']=[['PowerLaw','same_prefactor'],
#                                    ['PowerLaw','same_flux'],
#                                    ['SmoothBrokenPowerLaw','standard'],
#                                   ]
#
#j = JobBuilder(savedir='$snrsim_sims/v3',
#               code='$snrsim_code/simulate.py',
#               num=5,
#               params=params)
#j.build()


params=dict(source=['W44','IC443'], 
            simdir=join("$snrsim_sims","v3"))

params['spectrum','normalization']=[['PowerLaw','same_prefactor'],
                                    ['PowerLaw','same_flux'],
                                    ['SmoothBrokenPowerLaw','standard'],
                                   ]

j = JobBuilder(savedir='$snrsim_fits/v1',
               code='$snrsim_code/fit.py',
               num=5,
               params=params)
j.build()


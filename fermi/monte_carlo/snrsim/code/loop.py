from os.path import join

from lande.utilities.jobtools import JobBuilder

#params=dict(source=['W44','IC443'])
#params['spectrum','normalization']=[['PowerLaw','same_prefactor'],
#                                    ['PowerLaw','same_flux'],
#                                    ['SmoothBrokenPowerLaw','standard'],
#                                   ]
#
#j = JobBuilder(savedir='$snr_sim_sims/v1',
#               code='$snr_sim_code/simulate.py',
#               num=5,
#               params=params)
#j.build()


#params=dict(source=['W44','IC443'])
#params['spectrum','normalization']=[['PowerLaw','same_prefactor'],
#                                    ['PowerLaw','same_flux'],
#                                    ['SmoothBrokenPowerLaw','standard'],
#                                   ]
#
#j = JobBuilder(savedir='$snr_sim_sims/v2',
#               code='$snr_sim_code/simulate.py',
#               num=5,
#               params=params)
#j.build()


#params=dict(source=['W44','IC443'])
#params['spectrum','normalization']=[['PowerLaw','same_prefactor'],
#                                    ['PowerLaw','same_flux'],
#                                    ['SmoothBrokenPowerLaw','standard'],
#                                   ]
#
#j = JobBuilder(savedir='$snr_sim_sims/v3',
#               code='$snr_sim_code/simulate.py',
#               num=5,
#               params=params)
#j.build()



#params=dict(source=['W44','IC443'], 
#            simdir=join("$snr_sim_sims","v3"))
#params['spectrum','normalization']=[['PowerLaw','same_prefactor'],
#                                    ['PowerLaw','same_flux'],
#                                    ['SmoothBrokenPowerLaw','standard'],
#                                   ]
#
#j = JobBuilder(savedir='$snr_sim_fits/v1',
#               code='$snr_sim_code/fit.py',
#               num=5,
#               params=params)
#j.build()

#params=dict(source=['W44','IC443'], 
#            simdir=join("$snr_sim_sims","v3"))
#params['spectrum','normalization']=[['PowerLaw','same_prefactor'],
#                                    ['PowerLaw','same_flux'],
#                                    ['SmoothBrokenPowerLaw','standard'],
#                                   ]
#
#j = JobBuilder(savedir='$snr_sim_fits/v2',
#               code='$snr_sim_code/fit.py',
#               num=5,
#               params=params)
#j.build()




#params=dict(source=['W44','IC443'], 
#            simdir=join("$snr_sim_sims","v3"))
#params['spectrum','normalization']=[['PowerLaw','same_prefactor'],
#                                    ['PowerLaw','same_flux'],
#                                    ['SmoothBrokenPowerLaw','standard'],
#                                   ]
#
#j = JobBuilder(savedir='$snr_sim_fits/v3',
#               code='$snr_sim_code/fit.py',
#               num=5,
#               params=params)
#j.build()

#params=dict(source=['W44','IC443'], 
#            simdir=join("$snr_sim_sims","v3"))
#params['spectrum','normalization']=[['PowerLaw','same_prefactor'],
#                                    ['PowerLaw','same_flux'],
#                                    ['SmoothBrokenPowerLaw','standard'],
#                                   ]
#
#j = JobBuilder(savedir='$snr_sim_fits/v4',
#               code='$snr_sim_code/fit.py',
#               num=5,
#               params=params)
#j.build()




"""
# June 29, 2012
params=dict()
params['mc-energy']=[True,False]
params['source','spectrum']=[['IC443','PowerLaw'],['IC443','SmoothBrokenPowerLaw'],
                             ['W44','PowerLaw'],['W44','SmoothBrokenPowerLawHard'],['W44','SmoothBrokenPowerLawSoft']
                            ]

j = JobBuilder(savedir='$snr_sim_sims/v4',
               code='$snr_sim_code/simulate.py',
               num=5,
               params=params)
j.build()
"""

"""
# August 15, 2012
params=dict()
params['mc-energy']=[True,False]
params['source','spectrum']=[['IC443','PowerLaw'],
                             ['IC443','SmoothBrokenPowerLaw'],
                             ['W44','PowerLaw'],
                             ['W44','SmoothBrokenPowerLawHard'],
                             ['W44','SmoothBrokenPowerLawSoft']
                            ]
params['diffuse'] = [ 'galactic', 'sreekumar', 'nobackground']

j = JobBuilder(savedir='$snr_sim_sims/v5',
               code='$snr_sim_code/simulate.py',
               num=1,
               params=params)
j.build()
"""





# September 7, 2012

params=dict()
params['mc-energy']=[True,False]
params['source','spectrum']=[['IC443','PowerLaw'],
                             ['IC443','SmoothBrokenPowerLaw'],
                            ]
params['diffuse'] = [ 'extrapolated']

j = JobBuilder(savedir='$snr_sim_sims/v6/full',
               code='$snr_sim_code/simulate.py',
               num=5,
               params=params)
j.build()



params=dict()
params['mc-energy']=[True,False]
params['source','spectrum']=[['IC443','PowerLaw'],
                             ['IC443','SmoothBrokenPowerLaw'],
                            ]
params['fluxfactor'] = [ 100 ]
params['diffuse'] = [ 'nobackground']
params['spatial'] = [ 'point', 'extended' ]

j = JobBuilder(savedir='$snr_sim_sims/v6/simple',
               code='$snr_sim_code/simulate.py',
               num=2,
               params=params)
j.build()

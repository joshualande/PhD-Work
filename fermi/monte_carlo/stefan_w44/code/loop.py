from lande.utilities.jobtools import JobBuilder

#params=dict(spectrum=[ 'SmoothBrokenPowerLaw', 'SmoothDoubleBrokenPowerLaw'])
#j = JobBuilder(savedir='$stefan_w44_data/v1',
#               code='$stefan_w44_code/simulate.py',
#               num=10,
#               params=params)
#j.build()



#params=dict(source=['W44','IC443'], 
#            spectrum=[ 'PowerLaw', 'SmoothBrokenPowerLaw'])
#j = JobBuilder(savedir='$stefan_w44_sims/v2',
#               code='$stefan_w44_code/simulate.py',
#               num=10,
#               params=params)
#j.build()


#params=dict(source=['W44','IC443'], 
#            spectrum=[ 'PowerLaw', 'SmoothBrokenPowerLaw'])
#j = JobBuilder(savedir='$stefan_w44_fits/v1',
#               code='$stefan_w44_code/fit.py',
#               num=10,
#               params=params)
#j.build()


# ------------------------------------------------------------------------------------------------------------------------

params=dict(source=['W44','IC443'], 
            spectrum=[ 'PowerLaw', 'SmoothBrokenPowerLaw'])
j = JobBuilder(savedir='$stefan_w44_sims/temp1',
               code='$stefan_w44_code/simulate.py',
               num=10,
               params=params)
j.build()


params=dict(source=['W44','IC443'], 
            spectrum=[ 'PowerLaw', 'SmoothBrokenPowerLaw'])
j = JobBuilder(savedir='$stefan_w44_fits/temp1',
               code='$stefan_w44_code/fit.py',
               num=10,
               params=params)
j.build()




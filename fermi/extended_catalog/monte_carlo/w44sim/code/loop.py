from lande.utilities.simtools import SimBuilder

# version 1
#num=100
#savedir = expandvars('$w44simdata/v1')

# version 2
#num=2000
#savedir = expandvars('$w44simdata/v2')

# version 3 - save r68
#num=2000
#savedir = expandvars('$w44simdata/v3')

# version 4 - better mapcube cutting
#num=100
#savedir = expandvars('$w44simdata/v4')

# version 5 - no edisp, save out r68 for MC
#num=100
#savedir = expandvars('$w44simdata/v5')

# version 6 - w/ edisp in simulation, w/ gtlike
#num=100
#savedir = expandvars('$w44simdata/v6')

# version 7 - enable energy dispersion fitting in gtlike, fix annoygin warnings
#num=1000
#savedir = expandvars('$w44simdata/v7')
#
#from os.path import join, expandvars, exists
#from os import makedirs
#for i in range(num):
#    istr='%05d' % i
#
#    jobdir = join(savedir,istr)
#    if not exists(jobdir): makedirs(jobdir)
#
#    run = join(jobdir,'run.sh')
#    open(run,'w').write("""python $w44simcode/simulate.py %g""" % i)
#
#submit_all = join(savedir,'submit_all.sh')
#open(submit_all,'w').write("submit_all */run.sh $@")




# version 8 - unbinned likelihood (at mc spatial model)
# b = SimBuilder(
#         savedir='$w44simdata/v8',
#         code='$w44simcode/simulate.py',
#         num=100,
#         )
# b.build()


# version 9 - head version of code
#b = SimBuilder(
#        savedir='$w44simdata/v9',
#        code='$w44simcode/simulate.py',
#        num=100,
#        )
#b.build()


# version 10 - better ltcube, z100 cut
#b = SimBuilder(
#        savedir='$w44simdata/v10',
#        code='$w44simcode/simulate.py',
#        num=100,
#        )
#b.build()

# version 11 - same as v10 w/ no edisp
#b = SimBuilder(
#        savedir='$w44simdata/v11',
#        code='$w44simcode/simulate.py',
#        num=100,
#        )
#b.build()


# version 12 - same as v11 w/ no diffuse sources
#b = SimBuilder(
#        savedir='$w44simdata/v12',
#        code='$w44simcode/simulate.py',
#        num=100,
#        )
#b.build()



# version 13 - no ac gut in gtlike
#b = SimBuilder(
#        savedir='$w44simdata/v13',
#        code='$w44simcode/simulate.py',
#        num=100,
#        )
#b.build()

# version 14 - resample=no, 0.1deg binning, w/ diffuse bg
#b = SimBuilder(
#        savedir='$w44simdata/v14',
#        code='$w44simcode/simulate.py',
#        num=100,
#        )
#b.build()

# version 15 - back to regular simulations w/ (resample=no, 0.1deg binning, 10 deg ROI, 9 phibins)
#b = SimBuilder(
#        savedir='$w44simdata/v15',
#        code='$w44simcode/simulate.py',
#        num=1000,
#        )
#b.build()

# version 16 - just fit w/ mc spatial but w/ (minbinsz=0.025)
#b = SimBuilder(
#        savedir='$w44simdata/v16',
#        code='$w44simcode/simulate.py',
#        num=300,
#        )
#b.build()

# version 17 - just fit w/ mc spatial but w/ (minbinsz=0.001)
#b = SimBuilder(
#        savedir='$w44simdata/v17',
#        code='$w44simcode/simulate.py',
#        num=300,
#        )
#b.build()

# version 18 - try with binsz=0.2, minbisz=0.1
#b = SimBuilder(
#        savedir='$w44simdata/v18',
#        code='$w44simcode/simulate.py',
#        num=100,
#        )
#b.build()


# version 19 - binsz=0.05, minbinsz=0.05, roi=40x40deg
#b = SimBuilder(
#        savedir='$w44simdata/v19',
#        code='$w44simcode/simulate.py',
#        num=100,
#        )
#b.build()

# version 20 - all defaults, but align_extended=True
#b = SimBuilder(
#    savedir='$w44simdata/v20',
#    code='$w44simcode/simulate.py',
#    num=50,
#    params=dict(edisp=['no','yes'], simbg=['no','yes']),
#    )
#b.build()

# version 21 - back to full analysis w/ binsz=0.05, minbinsz=0.025, align_extended=True, roi radius (pointlike) = 15*np.sqrt(2)
#b = SimBuilder(
#    savedir='$w44simdata/v21',
#    code='$w44simcode/simulate.py',
#    num=1000,
#    )
#b.build()



# version 31 
#b = SimBuilder(
#    savedir='$w44simdata/v31',
#    code='$w44simcode/simulate.py',
#    num=1000,
#    params=dict(edisp=True),
#    )
#b.build()



# version 33
b = SimBuilder(
    savedir='$w44simdata/v33',
    code='$w44simcode/simulate.py',
    num=1000,
    params=dict(edips=False),
    )
b.build()

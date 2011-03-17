from setup_pwn import setup_pwn
from uw.like.SpatialModels import Disk
from uw.like.roi_tsmap import TSCalc,TSCalcPySkyFunction
from argparse import ArgumentParser
from skymaps import SkyImage,SkyDir

parser = ArgumentParser()
parser.add_argument("-l", "--list", required=True, help="List of all yaml sources")
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
args=parser.parse_args()
  
name=args.name

roi=setup_pwn(name,args.list)

p=lambda: roi.print_summary(title='')

# First, calculate upper limit

fit=lambda: roi.fit(method='minuit')
    
fit()

p()

roi.localize(update=True)

p()

if roi.TS(which=name,quick=False) > 16:

    source = roi.get_source(which=name)
    point_position = source.skydir

    roi.modify(which=name,spatial_model=Disk())

    roi.fit_extension(which=name,use_gradient=True)

    ts_ext=roi.TS_ext(which=name,use_gradient=True)

    print 'ts_ext = ',ts_ext

    if ts_ext<16:
        roi.modify(which=name,spatial_model=point_position)

    fit()

    p()

    # get spectral values

    model = roi.get_model(which=name)

    print model.i_flux(100,100000)


    # fit in different energy ranges.


    E_range=[[100.0,1000.0],[1000.0,10000.0],[10000.0,100000.0]]

    for i in range(len(E_range)-1):
        roi.modify(fit_emin=[E_range[i][0]]*2,fit_emax=[E_range[i][2]]*2)

        fit()

        p()

        print "Energy range : emin= %.2f \t emax= %.2f"%(E_range[i][0],E_range[i][1])

        ts=roi.TS(which="",quick=False)

        model = roi.get_model(which=name)
        
        p,p_err=model.statistical(absolute=True)

        print model.i_flux(E_range[i][0],E_range[i][1])

        index,indexerr=p[1],p_err[1]
            
        print "index="+str(index)+"\t"+str(indexerr)

    # make residual TS map

    source = roi.delete(which=name)
    roi.modify(fit_emin=100,fit_emax=1000)
            
    tscalc = TSCalc(roi)
    skyfunction=TSCalcPySkyFunction(tscalc)
    
    
    namTS="output_residual_TSMap_%s.fits"%(name)
    outputFile=namTS
    pixelsize=0.2
    fov=10
    ptype='ZEA'
    galactic=False
    earth=False
    
    skyimage = SkyImage(center, outputFile, pixelsize, fov, 1, ptype, galactic, earth)
    skyimage.fill(skyfunction.get_pyskyfun())
    del(skyimage)
    
                                                        

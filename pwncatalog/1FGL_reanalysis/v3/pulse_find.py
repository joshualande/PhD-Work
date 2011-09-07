import matplotlib as mpl
mpl.rcParams['backend'] = 'Agg'
mpl.use("Agg")
from setup_pwn import setup_pwn
from argparse import ArgumentParser
import yaml
import numpy as np
from scipy.optimize import leastsq
import pylab as P

#parser = ArgumentParser()
#parser.add_argument("--pwndata", required=True)
#parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
#parser.add_argument("--phcent", type=float, required=True)
#args=parser.parse_args()
#
#name=args.name
#phi_center=args.phcent
#pwndata=args.pwndata

pwndata='pwndata_v1.yaml'

""" This min and max do not correspond to
the off pulse phase min and max, but
to the phase interval over which to
search for the off pulse phase min and max.
They correspond to the peak in the phaseogram
of the two pulsar peaks inside of which
we look for the off pulse emission. """

#name='PSRJ0534+2200'
#phase_max=1
#phase_min=0.3

name='PSRJ0007+7303'
phase_min=0.45-0.35
phase_max=0.45+0.25

dphimax=(phase_max-phase_min) % 1
phi_center=(phase_min + dphimax/2) % 1
#npts=100
npts=30
def phasebinanalysis(phi_center_f):
    #npts=100
    #npts=10
    
    TS=np.zeros(npts)
    phimin=np.zeros(npts)
    phimax=np.zeros(npts)
    
    # don't go all the way to 0 = no photons!
    dphi = np.linspace(dphimax/10,dphimax,npts)
    phimin = (phi_center_f - dphi/2) % 1
    phimax = (phi_center_f + dphi/2) % 1

    for i,phase in enumerate(zip(phimin,phimax)):
        print 'phase min=%.2f, max=%.2f (%d/%d)' % (phase[0],phase[1],i+1,npts)
        
        roi=setup_pwn(name,pwndata,phase, quiet=True)
        print 'bin edges:',roi.bin_edges
        roi.fit(use_gradient=True)
        TS[i]=roi.TS(which=name, quick=False)

    middle_index=int(len(dphi)/2.0)
    dphi_break_0=dphi[middle_index]
    pwn_0=TS[middle_index]/dphi_break_0
    psr_0=(TS[-1]-TS[middle_index])/(dphi[-1]-dphi[middle_index])
    p0=np.asarray([pwn_0,psr_0,dphi_break_0])

    # this function returns TS as a function of dphi
    def model_ts(p,dphi):
        # pwn = slope of pwn
        # psr = slope of psr
        # dphi_break is break between pwn and pulsar
        pwn,psr,dphi_break=p
        return np.where(dphi<dphi_break,
                        pwn*dphi,
                        psr*(dphi-dphi_break) + pwn*dphi_break)
    def model_ts_pl(p,dphi):
        # pwn = slope of pwn
        pwn=p
        return pwn*dphi
    errfunc = lambda p, dphi: TS-model_ts(p,dphi)
    p1, success = leastsq(errfunc,p0,args=(dphi,))

    pwn_1,psr_1,dphi_break_1= p1
    phimin_1 = (phi_center_f - dphi_break_1/2) % 1
    phimax_1 = (phi_center_f + dphi_break_1/2) % 1
    print 'The best dphi is = %.2f. Range = [%.2f, %.2f]' % (dphi_break_1,phimin_1,phimax_1)
                    


    
    p2=pwn_0

    TS2=[]
    TS2.append(TS[0])
    dphi2=[]
    dphi2.append(dphi[0])
    for i in range(len(TS)-2):
        TS2.append(TS[i+1])
        dphi2.append(dphi[i+1])
        errfunc2= lambda p2, dphi:TS2-model_ts_pl(p2,dphi2)
        p3, success = leastsq(errfunc2,p2,args=(dphi2,))
        error=TS[i+2]-model_ts_pl(p3,dphi[i+2])
        if error > 4:
            dphi_break_1=dphi[i+1]
            phimin_1=(phi_center_f -dphi_break_1/2) % 1
            phimax_1 = (phi_center_f + dphi_break_1/2) % 1
            print 'The best dphi is = %.2f. Range = [%.2f, %.2f]' % (dphi_break_1,phimin_1,phimax_1)

    # plot the results

    f=open("phase_analysis_%s.yaml" % name,"w")
    yaml.dump(dict(TS=TS.tolist(), dphi=dphi.tolist(),
                   phimin=phimin.tolist(), phimax=phimax.tolist(),
                   p0=p0.tolist(),p1=p1.tolist()),f) # todo, add phimin, phimax to file
    f.close()
    
    #plotting code
    P.figure(1,figsize=(6,6));P.clf()
    
    P.ylabel(r'TS')
    P.xlabel(r'$\Delta\phi$')
    P.title("TS $(\Delta\phi)$")
    P.grid(True)

    dphi_model=np.linspace(0,dphi[-1],100)
    P.plot(dphi_model,model_ts(p1,dphi=dphi_model),label='model')
    P.plot(dphi,TS, 'o', label='data')

    P.savefig("TS_dphi_%s_%s.png"%(name,phi_center_f))

    return dphi_break_1,phimin_1,phimax_1


#Loop on the center position the idea is the following : look to 1 bin in each side of the center. redefine the center as the position fo which the interval is the largest then iterate in the same sens.
dphicent,phimincent,phimaxcent=phasebinanalysis(phi_center)
dphilow,phiminlow,phimaxlow=phasebinanalysis(phi_center-dphimax/npts)
dphihigh,phiminhigh,phimaxhigh=phasebinanalysis(phi_center+dphimax/npts)

f2=open("control.txt","w")

f2.write("dphicent,phimincent,phimaxcent=%.2f\t%.2f\t%.2f\n"%(dphicent,phimincent,phimaxcent))
f2.write("dphilow,phiminlow,phimaxlow=%.2f\t%.2f\t%.2f\n"%(dphilow,phiminlow,phimaxlow))
f2.write("dphihigh,phiminhigh,phimaxhigh=%.2f\t%.2f\t%.2f\n"%(dphihigh,phiminhigh,phimaxhigh))
delta=0
dphiloop=0
if dphilow>=dphicent :
    delta=-dphimax/npts
    dphiloop=dphilow
elif dphihigh>=dphicent :
    delta=+dphimax/npts
    dphiloop=dphihigh
else :
    delta=0.0

f2.write("delta=%.2f\n"%(delta))

if delta !=0.0:
    i=0
    while dphiloop<dphicent and i<10:
        dphiloop=dphicent
        phi_center+=delta
        dphicent,phimincent,phimaxcent=phasebinanalysis(phi_center)
        i+=1
        f2.write("dphicent,phimincent,phimaxcent=%.2f\t%.2f\t%.2f\n"%(dphicent,phimincent,phimaxcent))

print "Best fit position :\n\tcenter=%.2f\n\twidth=%.2f\n\tmin=%.2f\n\tmax=%.2f\n"%(dphicent,phimaxcent-phimincent,phimincent,phimaxcent)
f2.write("Best fit position :\n\tcenter=%.2f\n\twidth=%.2f\n\tmin=%.2f\n\tmax=%.2f\n"%(dphicent,phimaxcent-phimincent,phimincent,phimaxcent))        

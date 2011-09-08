import matplotlib as mpl
mpl.rcParams['backend'] = 'Agg'
mpl.use("Agg")
from setup_pwn import setup_pwn
from argparse import ArgumentParser
import yaml
import numpy as np
from scipy.optimize import leastsq
import pylab as P


def compute_curve(name,pwndata,phi_center,npts):
    """Function to compute the points TS vs dphi"""
    #npts=50


    # don't go all the way to 0 = no photons!
    dphi = np.linspace(0,1,npts)[1:]
    phimin = (phi_center - dphi/2) % 1
    phimax = (phi_center + dphi/2) % 1

    TS=np.empty_like(dphi)

    for i,phase in enumerate(zip(phimin,phimax)):
        print 'phase min=%.2f, max=%.2f (%d/%d)' % (phase[0],phase[1],i+1,npts)
        if phase[0]>phase[1]:
            phase2=[[phase[0],1.0],[0.0,phase[1]]]
        else :
            phase2=phase

        roi=setup_pwn(name,pwndata,phase2, quiet=True)
        print 'bin edges:',roi.bin_edges
        roi.fit(method="minuit",use_gradient=True, estimate_errors=False)
        TS[i]=roi.TS(which=name, quick=False)
    

        f=open("results_%s_%.2f.yaml" %(name,phi_center)"w")
        yaml.dump(dict(TS=TS.tolist(), 
                       dphi=dphi.tolist(),
                       phi_center=phi_center,
                       phimin=phimin.tolist(), 
                       phimax=phimax.tolist()),
                  f) # todo, add phimin, phimax to file
        f.close()

        return TS,dphi,phimin,phimax

def model_ts_line(pwn,dphi):
    """Model of a line"""
    # pwn = slope of pwn
    return pwn*dphi

def find_deviation(TS,dphi):
    """ Find the point at which TS diverges from the best
        fit line by >=9."""
    error=np.zeros_like(TS)
    for i in range(2,len(TS)):
        errfunc= lambda p2, dphi:TS2[0:i-1]-model_ts_pl(p2,dphi[0:i-1])
        p3, success = leastsq(errfunc,p2,args=(dphi[0:i-1],))
        error[i]=TS[i]-model_ts_line(p3,dphi[i]))

    first_greater = np.argwhere(error > 9)[0]
    error_less = error[ 0:first_greater-1 ]

    last_greater = np.argwhere(less > 4)[-1]

    best_dphi=dphi[last_less-1],
    best_TS=TS[last_less-1],
    bset_error=error[last_less-1]

    print 'The best dphi is = %.2f. TS=%.2f, error=%.2f' % (best_dphi,best_TS,best_error)
    return last_greater_4

def find_center(center,npts,**kwargs):
   """Loop on the center position the idea is the following : look to 1 bin in each side of the center. redefine the center as the position fo which the interval is the largest then iterate in the same sens."""
   TS1,dphi1,phimin1,phimax1=compute_curve(center,**kwargs)
   index1=find_deviation(TS1,dphi1)
   #center-1.0/npts
   TS2,dphi2,phimin2,phimax2=compute_curve(center-1.0/npts,**kwargs)
   index2=find_deviation(TS2,dphi2)
   #center+1.0/npts
   TS3,dphi3,phimin3,phimax3=compute_curve(center+1.0/npts,**kwargs)
   index3=find_deviation(TS3,dphi)

   f2=open("control.txt","w")

   f2.write("dphicent,phimincent,phimaxcent=%.2f\t%.2f\t%.2f\n"%(dphi1[index1],phimin1[index1],phimax[index1]))
   f2.write("dphilow,phiminlow,phimaxlow=%.2f\t%.2f\t%.2f\n"%(dphi2[index2],phimin2[index2],phimax2[index2]))
   f2.write("dphihigh,phiminhigh,phimaxhigh=%.2f\t%.2f\t%.2f\n"%(dphi3[index3],phimin3[index3],phimax3[index3]))

   """
   delta=0
   dphiloop=0
   if dphilow>=dphicent :
       delta=-1.0/npts
       dphiloop=dphilow
       dphicent=dphiloop+1
   elif dphihigh>=dphicent :
       delta=+1.0/npts
       dphiloop=dphihigh
       dphicent=dphiloop+1
   else :
       delta=0.0

   f2.write("delta=%.2f\n"%(delta))
       
   if delta !=0.0:
       i=0
       while dphiloop<dphicent and i<10:
           dphiloop=dphicent
           center+=delta
           TS4,dphi4=compute_curve(center,npts=50)
           dphicent,phimincent,phimaxcent,errorcent=find_deviation(TS4,dphi4)
           i+=1
           f2.write("dphicent,phimincent,phimaxcent,dphiloop=%.2f\t%.2f\t%.2f\t%.2f\n"%(dphicent,phimincent,phimaxcent,dphiloop))
           
       print "Best fit position :\n\tcenter=%.2f\n\twidth=%.2f\n\tmin=%.2f\n\tmax=%.2f\n"%((phimincent+dphicent/2.0)%1,dphicent,phimincent,phimaxcent)
       f2.write("Best fit position :\n\tcenter=%.2f\n\twidth=%.2f\n\tmin=%.2f\n\tmax=%.2f\n"%((phimincent+dphicent/2.0)%1,dphicent,phimincent,phimaxcent))

   f2.close()

   return (phimincent+dphicent/2.0)%1,dphicent,phimincent,phimaxcent
   """


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--pwndata", required=True)
    parser.add_argument("-p", "--pwnphase", required=True)
    parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
    parser.add_argument("--localize", help="Localize phi center")
    parser.add_argument("--npts", default=50)
    args=parser.parse_args()

    phase=yaml.load(open(args.pwnphase))[args.name]['phase']
    # guess at center of off pulse region
    phi_center=(phase[0] + ((phase[1]-phase[0]) % 1)/2.0) % 1

    if args.localize:
        cent,dphi,phimin,phimax=find_center(name=args.name, pwndata=args.pwndata, 
                                            phi_center=phi_center, npts=args.npts)
    else:
        compute_curve(args.name,args.pwndata,phi_center,args.npts)

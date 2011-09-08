import matplotlib as mpl
mpl.rcParams['backend'] = 'Agg'
mpl.use("Agg")
from setup_pwn import setup_pwn
from argparse import ArgumentParser
import yaml
import numpy as np
from scipy.optimize import leastsq
import pylab as P

parser = ArgumentParser()
parser.add_argument("--pwndata", required=True)
parser.add_argument("-p", "--pwnphase", required=True)
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
args=parser.parse_args()

#name=args.name
name="PSRJ0007+7303"


phase=yaml.load(open(args.pwnphase))[name]['phase']
# guess at center of off pulse region
phi_center=(phase[0] + ((phase[1]-phase[0]) % 1)/2.0) % 1

def compute_curve(phi_center,npts=50):
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

        roi=setup_pwn(name,args.pwndata,phase2, quiet=True)
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

        return TS,dphi

def model_ts_line(p,dphi):
    """Model of a line"""
    # pwn = slope of pwn
    pwn=p
    return pwn*dphi

def find_dec(TS,dphi):
    """function to find the best phase interval"""
    p2=pwn_0
    TS2=[]
    TS2.append(TS[0])
    dphi2=[]
    error=[]
    dphi2.append(dphi[0])
    i=0
    error[0]=0
    error2=0
    ind=0
    while i<(len(TS)-2) and error2<9:
        TS2.append(TS[i+1])
        dphi2.append(dphi[i+1])
        errfunc2= lambda p2, dphi:TS2-model_ts_pl(p2,dphi)
        p3, success = leastsq(errfunc2,p2,args=(dphi2,))
        error2=TS[i+2]-model_ts_line(p3,dphi[i+2])
        error.append(error2)
        print 'error=%.2f'%error2
        if error2 > 9:
            dphi_break_1=dphi[i+1]
            phimin_1=(phi_center_f -dphi_break_1/2) % 1
            phimax_1 = (phi_center_f + dphi_break_1/2) % 1
            #print 'The best dphi is = %.2f. Range = [%.2f, %.2f]\t error=%.2f' % (dphi_break_1,phimin_1,phimax_1,error2)
            ind=i
        i+=1
    
    while i<range(len(dphi2)) and error[i]>4:
        i-=1
        ind-=1

    dphi_break_1=dphi[ind]
    phimin_1=(phi_center_f -dphi_break_1/2) % 1
    phimax_1 = (phi_center_f + dphi_break_1/2) % 1
    print 'The best dphi is = %.2f. Range = [%.2f, %.2f]\t error=%.2f' % (dphi_break_1,phimin_1,phimax_1,error[ind])
    
    return dphi_break_1,phimin_1,phimax_1,error


def find_center(center,npts):
   """Loop on the center position the idea is the following : look to 1 bin in each side of the center. redefine the center as the position fo which the interval is the largest then iterate in the same sens."""
   TS1,dphi1=compute_curve(center,npts=50)
   dphicent,phimincent,phimaxcent,errorcent=find_dec(TS1,dphi1)
   #center-1.0/npts
   TS2,dphi2=compute_curve(center-1.0/npts,npts=50)
   dphilow,phiminlow,phimaxlow,errorlow=find_dec(TS2,dphi2)
   #center+1.0/npts
   TS3,dphi3=compute_curve(center+1.0/npts,npts=50)
   dphihigh,phiminhigh,phimaxhigh,errorhigh=find_dec(TS3,dphi)

   f2=open("control.txt","w")

   f2.write("dphicent,phimincent,phimaxcent=%.2f\t%.2f\t%.2f\n"%(dphicent,phimincent,phimaxcent))
   f2.write("dphilow,phiminlow,phimaxlow=%.2f\t%.2f\t%.2f\n"%(dphilow,phiminlow,phimaxlow))
   f2.write("dphihigh,phiminhigh,phimaxhigh=%.2f\t%.2f\t%.2f\n"%(dphihigh,phiminhigh,phimaxhigh))
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
           dphicent,phimincent,phimaxcent,errorcent=find_dec(TS4,dphi4)
           i+=1
           f2.write("dphicent,phimincent,phimaxcent,dphiloop=%.2f\t%.2f\t%.2f\t%.2f\n"%(dphicent,phimincent,phimaxcent,dphiloop))
           
       print "Best fit position :\n\tcenter=%.2f\n\twidth=%.2f\n\tmin=%.2f\n\tmax=%.2f\n"%((phimincent+dphicent/2.0)%1,dphicent,phimincent,phimaxcent)
       f2.write("Best fit position :\n\tcenter=%.2f\n\twidth=%.2f\n\tmin=%.2f\n\tmax=%.2f\n"%((phimincent+dphicent/2.0)%1,dphicent,phimincent,phimaxcent))

   f2.close()

   return (phimincent+dphicent/2.0)%1,dphicent,phimincent,phimaxcent


npts=50
cent,dphi,phimin,phimax=find_center(phi_center,npts)

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
phase_min=0.45-0.25
phase_max=0.45+0.25

dphimax=(phase_max-phase_min) % 1
phi_center=(phase_min + dphimax/2) % 1

#npts=100
npts=10

TS=np.zeros(npts)
phimin=np.zeros(npts)
phimax=np.zeros(npts)

# don't go all the way to 0 = no photons!
dphi = np.linspace(dphimax/10,dphimax,npts)
phimin = (phi_center - dphi/2) % 1
phimax = (phi_center + dphi/2) % 1

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

errfunc = lambda p, dphi: TS-model_ts(p,dphi)
p1, success = leastsq(errfunc,p0,args=(dphi,))


pwn_1,psr_1,dphi_break_1= p1
phimin_1 = (phi_center - dphi_break_1/2) % 1
phimax_1 = (phi_center + dphi_break_1/2) % 1
print 'The best dphi is = %.2f. Range = [%.2f, %.2f]' % (dphi_break_1,phimin_1,phimax_1)

# plot the results

f=open("phase_analysis_%s.yaml" % name,"w")
yaml.dump(dict(TS=TS.tolist(), dphi=dphi.tolist(),
                 phimin=phimin.tolist(), phimax=phimax.tolist(),
                 p0=p0.tolist(),p1=p1.tolist()),f) # todo, add phimin, phimax to file
f.close()

#plotting code
P.figure(1,figsize=(6,6))

P.ylabel(r'TS')
P.xlabel(r'$\Delta\phi$')
P.title("TS $(\Delta\phi)$")
P.grid(True)

dphi_model=np.linspace(0,dphi[-1],100)
P.plot(dphi_model,model_ts(p1,dphi=dphi_model),label='model')
P.plot(dphi,TS, 'o', label='data')

P.savefig("TS_dphi_%s.png"%name)

import matplotlib as mpl
mpl.rcParams['backend'] = 'Agg'
mpl.use("Agg")
from setup_pwn import setup_pwn
from uw.like.SpatialModels import Disk
from uw.like.roi_tsmap import TSCalc,TSCalcPySkyFunction
from argparse import ArgumentParser
from skymaps import SkyImage,SkyDir
import yaml
from array import *
from scipy.optimize import leastsq
from uw.like.sed_plotter import plot_sed
import pylab as P



parser = ArgumentParser()
parser.add_argument("-l", "--list", required=True, help="List of all yaml sources")
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
args=parser.parse_args()

name=args.name

phase_center=args.phcent

f=open("%s_phase_analysis.out"%name,"w")

f.write("#0:TS\t,1:width of the phase interval(Delta phi)\t,2:minimum of the phase interval\t,3:maximum of the phase interval")

Tstat=array('f',100*[0])
dphi=array('f',100*[0])
phimin=array('f',100*[0])
phimax=array('f',100*[0])

for i in range(100):
    phimin[i]=phcent-float(i+1)/200.0
    phimax[i]=phcent+float(i+1)/200.0
    dphi[i]=float(i+1)/200.0

    phase= [phimin[i],phimax[i]]
    roi=setup_pwn(name,args.list,phase)
    roi.fit(method="minuit",use_gradient=True)
    Tstat[i]=roi.TS(which=name)
    
    f.write("%g\t%g\t%g\t%g"%(Tstat,dph[i],phimin[i],phimax[i]))
    if i<99:
        f.write("\n")


results=r={}

source=roi.get_source(which=name)
pulsar_position=source.skydir

TS_less_25=[]
dphi_less_25=[]
TS_high_25=[]
dphi_high_25=[]

for i in range(len(Tstat)):
    if Tsat[i]<25:
        TS_less_25.append(Tstat[i])
        dphi_less_25.append(dphi[i])
    else :
        TS_high_25.append(Tstat[i])
        dphi_high_25.append(dphi[i])


p0=[10,0.5]
def linear_func(p):
    y=p[0]*x+p[1]
    return y

courbe1=leastsq(linear_func,p0,)



#plotting code
P.figure(1,figsize=(2.5*num_cols,2*num_rows));P.clf()
oldlw = P.rcParams['axes.linewidth']
P.rcParams['axes.linewidth'] = 2
axes = P.gca()

P.ylabel(r'TS',fontsize=42)
P.xlabel(r'dphi',fontsize=42)
P.title('TS(dphi)',fontsize='small')

P.title("TS(dphi)",fontsize='small')
P.grid(True)



P.savefig("TS_dphi_%s.png"%name)

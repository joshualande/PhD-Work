import matplotlib as mpl
mpl.rcParams['backend'] = 'Agg'
mpl.use("Agg")
from setup_pwn import setup_pwn
from argparse import ArgumentParser
import yaml
import numpy as np
from scipy.optimize import leastsq
import pylab as P
from uw.pulsar import lc_plotting_func

def plot_lc(ft1,name,rad,phase):
    """plot light curve using pointlike script in whixh is added a line to plot the edges of the offpulse region
    phase = [a,b]
    a=minimum of the edge
    b=maximum of the edge"""
    
    global psrlc
    psrlc = lc_plotting_func.PulsarLightCurve( ft1, psrname=name, radius=rad)
    psrlc.fill_phaseogram()
    #psrlc.plot_lightcurve(nbands=4)

    P.axvline(phase[0], color='r')
    P.axvline(phase[1], color='r')

    phase,counts=psrlc.get_phaseogram(emin=1e2,emax=1e5)
    print zip(phase,counts)
    P.errorbar(phase,counts, 
               yerr=np.sqrt(counts), 
               marker='o',color='k', markersize=5,
               drawstyle='steps-mid', capsize=0)
    P.xlim(0,2)
    P.savefig('phaseogram_%s.pdf' % name)

    f=open('results_phaseogram_%s.yaml' % name)
    yaml.dump(
        dict(
            phase=phase,
            counts=counts),
        f)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--pwndata", required=True)
    parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
    parser.add_argument("-p", "--pwnphase", required=True)
    parser.add_argument("--npts", default=100)
    parser.add_argument("--emin", default=100, type=float)
    args=parser.parse_args()

    ft1=yaml.load(open(args.pwndata))[args.pwn]['ft1']
    phase=yaml.load(open(args.pwnphase))[args.pwn]['phase']

    plot_lc(ft1,name,rad=4,phase=phase)

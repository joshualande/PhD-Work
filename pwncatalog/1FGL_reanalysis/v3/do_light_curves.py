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

def plot_lc(ft1,name,rad,off_peak):
    """plot light curve using pointlike script in whixh is added a line to plot the edges of the offpulse region
    off_peak= [a,b]
    a=minimum of the edge
    b=maximum of the edge"""
    
    global psrlc
    psrlc = lc_plotting_func.PulsarLightCurve( ft1, psrname=name, radius=rad)
    psrlc.fill_phaseogram()
    #psrlc.plot_lightcurve(nbands=4)

    P.axvline(off_peak[0], color='r')
    P.axvline(off_peak[1], color='r')

    phase,counts=psrlc.get_phaseogram(emin=1e2,emax=1e5)
    P.errorbar(phase,counts, 
               yerr=np.sqrt(counts), 
               marker='o',color='k', markersize=5,
               drawstyle='steps-mid', capsize=0)
    P.xlim(0,2)
    P.savefig('phaseogram_%s.pdf' % name)

    f=open('results_phaseogram_%s.yaml' % name,'w')
    yaml.dump(
        dict(
            phase=phase.tolist(),
            counts=counts.tolist(),
            off_peak=off_peak,
            ),
        f)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--pwndata", required=True)
    parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
    parser.add_argument("-p", "--pwnphase", required=True)
    parser.add_argument("--test", default=False, action='store_true')
    parser.add_argument("--rad", default=4)
    args=parser.parse_args()

    if args.test:
        ft1="/nfs/slac/g/ki/ki03/lande/fermi_data/CTA1/pwncatalog_v1/ft1_CTA1.fits"
        name="PSRJ0007+7303"
        plot_lc(ft1,name,rad=args.rad,off_peak=[0.5,0.75])
    else:

        name=args.name

        ft1=yaml.load(open(args.pwndata))[name]['ft1']
        phase=yaml.load(open(args.pwnphase))[name]['phase']

        plot_lc(ft1,name,rad=args.rad,off_peak=phase)

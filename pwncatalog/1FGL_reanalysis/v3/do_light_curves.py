import matplotlib as mpl
mpl.rcParams['backend'] = 'Agg'
mpl.use("Agg")
from setup_pwn import setup_pwn
from argparse import ArgumentParser
import yaml
import numpy as np
from scipy.optimize import leastsq
import pylab as P
import lc_plotting_romain as plot

def plot_lc(ft1,name,rad,itv):
    """plot light curve using pointlike script in whixh is added a line to plot the edges of the offpulse region
    itv = [a,b]
    a=minimum of the edge
    b=maximum of the edge"""
    
    psrlc = plot.PulsarLightCurve( ft1, psrname=name, radius=rad)
    psrlc.fill_phaseogram()
    psrlc.plot_lightcurve(nbands=4,Romain=True,itv=itv)
    
if __name__ == '__main__':


    ft1="/nfs/slac/g/ki/ki03/lande/fermi_data/CTA1/pwncatalog_v1/ft1_CTA1.fits"
    name="PSRJ0007+7303"
    
    plot_lc(ft1,name,4,itv=[0.5,0.75])


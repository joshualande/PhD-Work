from argparse import ArgumentParser
import copy
import numbers
import pickle
import yaml
import numpy as np
import pylab as P
from uw.pulsar import lc_plotting_func
from uw.pulsar import lcprimitives as lp
from uw.pulsar.lcprimitives import * # for the eval
from uw.pulsar.lc_off_peak import OffPeak
from uw.pulsar import lcfitters as lf
from toolbag import tolist


def find_offpeak(ft1,name,rad,peaks,off_peak):
    """plot light curve using pointlike script in whixh is added a line to plot the edges of the offpulse region
    off_peak= [a,b]
    a=minimum of the edge
    b=maximum of the edge"""
    
    plc = lc_plotting_func.PulsarLightCurve(ft1, 
                                           psrname=name, radius=rad,
                                           emin=50, emax=300000)
    plc.fill_phaseogram()

    phases = plc.get_phases()
    primitives = []
    for peak in peaks:
        if isinstance(peak,numbers.Real):
            primitives.append(lp.LCLorentzian2(p=[0.4,0.05,0.05,peak]))
        else:
            primitives.append(eval(peak))
    #primitives = [lp.LCGaussian2(p=[0.05,0.05,0.05,peak]) for peak in peaks]
    #primitives = [lp.LCGaussian(p=[0.05,0.05,peak]) for peak in peaks]
    #primitives = [lp.LCGaussian(p=[0.05,0.05,peak]) for peak in peaks]
    lct = lf.LCTemplate(primitives=primitives)

    init_template = copy.deepcopy(lct)

    lcf = lf.LCFitter(lct,phases)
    print lcf
    lcf.fit(quick_fit_first=True)
    print lcf
    lcf.plot()

    dom = np.linspace(0,1,200)
    P.plot(dom,init_template(dom),color='green',lw=1)


    op = OffPeak(lcf)

    def wrap_axvspan(min,max,**kwargs):
        if isinstance(min,list) and isinstance(max,list):
            wrap_axvspan(min[0],min[1],**kwargs)
            wrap_axvspan(max[0],max[1],**kwargs)
        else:
            if min > max:
                P.axvspan(min,1,**kwargs)
                P.axvspan(0,max,**kwargs)
            else:
                P.axvspan(min,max,**kwargs)

    for a,b in op.off_peak.tolist(dense=False):
        P.axvspan(a, b, label='lande', alpha=0.25, color='green')

    wrap_axvspan(off_peak[0], off_peak[1], label='pwncat1', alpha=0.25, color='blue')

    P.legend()

    P.title(name)

    P.savefig('results_%s.pdf' % name)
    #P.savefig('phaseogram_%s.pdf' % name)

    global results
    results=tolist(
            dict(
                lande_phase = op.off_peak.tolist(),
                pwncat1phase = off_peak,
                )
            )

    yaml.dump(results,
              open('results_%s.yaml' % name,'w')
             )

    results['lcf'] = lcf
    results['init_template'] = init_template
    results['final_template'] = lct

    pickle.dump(
        results,
        open('results_%s.pickle' % name,'w')
        )



if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--pwndata", required=True)
    parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
    parser.add_argument("--pwnphase", required=True)
    parser.add_argument("--pwnpeaks", required=True)
    parser.add_argument("--rad", default=1)
    args=parser.parse_args()

    name=args.name
    ft1=yaml.load(open(args.pwndata))[name]['ft1']
    phase=yaml.load(open(args.pwnphase))[name]['phase']
    peaks=yaml.load(open(args.pwnpeaks))[name]['peaks']

    print peaks
    if peaks is None: parser.exit('no peaks')

    find_offpeak(ft1,name,rad=args.rad,peaks=peaks,off_peak=phase)

from argparse import ArgumentParser
import copy
import numbers
import pickle
import yaml
import numpy as np
import pylab as P

from setup_pwn import setup_pwn

from uw.pulsar import lc_plotting_func
from uw.pulsar import lcprimitives as lp
from uw.pulsar.lcprimitives import * # for the eval
from uw.pulsar.lc_off_peak import OffPeak
from uw.pulsar.phase_range import PhaseRange
from uw.pulsar import lcfitters as lf
from uw.like.Models import ExpCutoff
from toolbag import tolist


def find_TSdc(name,pwndata):
    print 'Calculating TSdc'
    roi=setup_pwn(name,pwndata,phase=PhaseRange(0,1))

    # start with a grid search, for convergence help
    f=roi.get_model(name).i_flux(1e2,1e5)

    best_ts = -np.inf
    for index in [.01, .5, 1,1.5,2]:
        for cutoff in [ 3e2, 1e3, 3e3, 1e4, 3e4]:
            m=ExpCutoff(index=index,cutoff=cutoff)
            m.set_flux(f,1e2,1e5)
            roi.modify(which=name, model=m, keep_old_flux=False)
            roi.fit(estimate_errors=False)
            ts=roi.TS(which=name)
            print cutoff,index,ts
            if  ts > best_ts:
                best_ts, best_index, best_cutoff = ts, index, cutoff

    roi.print_summary()

    TSdc = best_ts

    roi.plot_sed(which=name, filename='sed_%s.pdf' % name)
    roi.print_summary()


    print 'TSdc=%.1f' % TSdc

    return TSdc


def find_offpeak(ft1,name,rad,peaks,pwncat1phase, TSdc):
    """plot light curve using pointlike script in whixh is added a line to plot the edges of the offpulse region
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
    lct = lf.LCTemplate(primitives=primitives)

    init_template = copy.deepcopy(lct)

    print 'WARNING: HERE I SHOULD BE USING A WEIGHTED LIGHT CURVE'

    lcf = lf.LCFitter(lct,phases)
    print lcf
    lcf.fit(quick_fit_first=True)
    print lcf
    lcf.plot()

    dom = np.linspace(0,1,200)
    P.plot(dom,init_template(dom),color='green',lw=1)

    #if np.any([isinstance(p, LCLorentzian) or isinstance(p, LCLorentzian2) for p in primitives]):
    #    TScontamination = 0.1
    #else:
    #    TScontamination = 1
    #contamination = 1/(np.sqrt(TSdc)*10)
    #contamination = .01*(100/TSdc)**(1./2)
    #contamination = .01*(100/TSdc)**(1./3)
    #contamination = .01*(100/TSdc)**(1./4)
    contamination = .01

    op = OffPeak(lcf, contamination = contamination) 

    op.off_peak.axvspan(label='lande', alpha=0.25, color='green')

    pwncat1phase.axvspan(label='pwncat1', alpha=0.25, color='blue')

    P.legend()

    P.title(name)

    P.savefig('results_%s.pdf' % name)
    #P.savefig('phaseogram_%s.pdf' % name)

    global results
    results=tolist(
            dict(
                lande_phase = op.off_peak.tolist(),
                pwncat1phase = pwncat1phase.tolist(),
                TSdc = TSdc,
                contamitation = contamination,
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
    pwndata=args.pwndata

    ft1=yaml.load(open(pwndata))[name]['ft1']

    pwncat1phase=PhaseRange(*yaml.load(open(args.pwnphase))[name]['phase'])

    peaks=yaml.load(open(args.pwnpeaks))[name]['peaks']

    print peaks
    if peaks is None: parser.exit('no peaks')

    TSdc = find_TSdc(name,pwndata)

    peaks=yaml.load(open(args.pwnpeaks))[name]['peaks']

    find_offpeak(ft1,name,rad=args.rad,peaks=peaks,pwncat1phase=pwncat1phase, TSdc=TSdc)

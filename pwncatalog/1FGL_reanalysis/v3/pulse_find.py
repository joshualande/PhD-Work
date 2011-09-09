from setup_pwn import setup_pwn

from argparse import ArgumentParser
import yaml
import numpy as np

import roi_gtlike
from LikelihoodState import LikelihoodState

from lande_roi import mixed_linear

def compute_curve(name,pwndata,phimin, phimax, fit_emin):
    """Function to compute the points TS vs (phi range)"""

    TS=np.empty_like(phimin)


    print 'First, analyzing unphased data'
    roi=setup_pwn(name,pwndata,phase=[0,1], quiet=True, fit_emin=fit_emin)
    print 'bin edges:',roi.bin_edges

    gtlike = roi_gtlike.Gtlike(roi)
    like=gtlike.like
    like.fit()

    # freeze index of PWN
    index=like[like.par_index(name, 'Index')]
    index.setTrueValue(-2)
    index.setFree(0)

    # fix everything in the ROI except prefactor
    for i in range(len(like.model.params)):
        like.freeze(i)
    like[like.par_index(name, 'Prefactor')].setFree(1)

    # now, freeze everything else in the ROI:
    saved_state = LikelihoodState(gtlike.like)

    for i,phase in enumerate(zip(phimin,phimax)):
        print 'Loop %4d/%4d: phase min=%.2f, max=%.2f' % (i+1,len(phimin),phase[0],phase[1])

        roi=setup_pwn(name,pwndata,phase, quiet=True, fit_emin=fit_emin)
        gtlike = roi_gtlike.Gtlike(roi)

        # give model the same parameters as global fit.
        saved_state.like = gtlike.like
        saved_state.restore()

        gtlike.like.fit()
        # n.b. no need to reoptimize since only one parameter
        # is fit.
        TS[i] = gtlike.like.Ts(name,reoptimize=False)

        print 'phase=%s, TS=%s' % (phase,TS[i])

        f=open("results_%s.yaml" % name,"w")
        yaml.dump(dict(TS=TS.tolist(), 
                       phimin=phimin.tolist(), 
                       phimax=phimax.tolist()),
                  f)
        f.close()

    return TS,phimin,phimax



if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--pwndata", required=True)
    parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
    parser.add_argument("-p", "--pwnphase", required=True)
    parser.add_argument("--npts", default=100)
    parser.add_argument("--emin", default=100, type=float)
    args=parser.parse_args()

    phimax = mixed_linear(1./args.npts,1,args.npts)
    phimin = np.zeros_like(phimax)

    compute_curve(args.name,args.pwndata,phimin,phimax,fit_emin=args.emin)

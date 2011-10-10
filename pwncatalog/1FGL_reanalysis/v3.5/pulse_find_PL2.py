from setup_pwn_gal_fixe import setup_pwn

from argparse import ArgumentParser
import yaml
import numpy as np

import roi_gtlike
from LikelihoodState import LikelihoodState

from lande_roi import mixed_linear

def compute_curve(name,pwndata,phimin, phimax, fit_emin):
    """Function to compute the points TS vs (phi range)"""

    TS=np.zeros_like(phimin)
    flux=np.zeros_like(phimin)
    Npred=np.zeros_like(phimin)
    print 'First, analyzing unphased data'
    roi=setup_pwn(name,pwndata,phase=[0,1], quiet=True, fit_emin=fit_emin)
    print 'bin edges:',roi.bin_edges

    print roi

    gtlike = roi_gtlike.Gtlike(roi)
    like=gtlike.like

    for i in range(len(like.model.params)):
        like.freeze(i)
    like[like.par_index(name, 'Prefactor')].setFree(1)
    like[like.par_index(name, 'Prefactor')].setBounds(0.0,1.0e5)
#    like.fit()

    print like.model

    # freeze index of PWN
    index=like[like.par_index(name, 'Index')]
    index.setTrueValue(-2)
    index.setFree(0)

    print like.model

    # now, freeze everything else in the ROI:
    saved_state = LikelihoodState(gtlike.like)

    print "----------------------------------Begin Loop---------------------------------------"

    for i,phase in enumerate(zip(phimin,phimax)):
        print 'Loop %4d/%4d: phase min=%.2f, max=%.2f' % (i+1,len(phimin),phase[0],phase[1])

        roi=setup_pwn(name,pwndata,phase, quiet=True, fit_emin=fit_emin)
        gtlike = roi_gtlike.Gtlike(roi)
        gtlike.like[gtlike.like.par_index(name, 'Prefactor')].setBounds(0.0,1.0e5)
        # put the value of flux of the whole phase scaled by the phase_factor.
        print roi.phase_factor
        print "Model avant modif"
        print gtlike.like.model
        

        # give model the same parameters as global fit.
        #saved_state.like = gtlike.like
        #saved_state.restore()
        
        for j in range(len(gtlike.like.model.params)):
            gtlike.like.freeze(j)
        gtlike.like[gtlike.like.par_index(name, 'Prefactor')].setFree(1)
        gtlike.like[gtlike.like.par_index(name, 'Prefactor')].setBounds(0.0,1.0e5)
        gtlike.like[gtlike.like.par_index("Galactic Diffuse (gll_iem_v02.fit)", 'Prefactor')].setBounds(0.0,1.0e5)
        gtlike.like["Galactic Diffuse (gll_iem_v02.fit)"].funcs['Spectrum'].getParam('Prefactor').setValue(1.0*roi.phase_factor)
        gtlike.like[gtlike.like.par_index("Isotropic Diffuse (isotropic_iem_v02.txt)", 'Normalization')].setBounds(0.0,1.0e5)
        gtlike.like["Isotropic Diffuse (isotropic_iem_v02.txt)"].funcs['Spectrum'].getParam('Normalization').setValue(1.0*roi.phase_factor)
        print "Model apres modif"
        print gtlike.like.model
        gtlike.like.fit()
        outputModel = "output_model_%s_%s_%s.xml" %(name,phase[0], phase[1])

        print "Model apres fit"
        print gtlike.like.model
        # n.b. no need to reoptimize since only one parameter
        # is fit.
        print i
        print len(TS)
        TS[i] = gtlike.like.Ts(name,reoptimize=True)

        flux[i]=gtlike.like.flux(name,1.0e2,1.0e5)
        Npred[i]=gtlike.like.logLike.NpredValue(name)
        print 'phase=%s, TS=%s' % (phase,TS[i])

        f=open("results_%s.yaml" % name,"w")
        yaml.dump(dict(TS=TS[0:i+1].tolist(), 
                       phimin=phimin[0:i+1].tolist(), 
                       phimax=phimax[0:i+1].tolist(),
                       flux=flux[0:i+1].tolist(),
                       Npred=Npred[0:i+1].tolist()),
                  f)
        f.close()

    return TS,phimin,phimax



if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("--pwndata", required=True)
    parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
    parser.add_argument("-p", "--pwnphase", required=True)
    parser.add_argument("--npts", default=50)
    parser.add_argument("-emin", "--emin",  default=1.0e2, type=float)
    parser.add_argument("-emax", "--emax",  default=1.0e5, type=float)

    args=parser.parse_args()

    phimax = mixed_linear(1./args.npts,1,args.npts)
    phimin = np.zeros_like(phimax)

    compute_curve(args.name,args.pwndata,phimin,phimax,fit_emin=args.emin)

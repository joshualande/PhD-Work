import yaml
import numpy as np

# This import has to come first
from analyze_helper import save_results

from setup_pwn import setup_pwn,get_source
from argparse import ArgumentParser

from uw.pulsar.phase_range import PhaseRange
from uw.like.roi_state import PointlikeState
from roi_gtlike import Gtlike
from LikelihoodState import LikelihoodState
from likelihood_tools import paranoid_gtlike_fit


def thierry_profile(name, func, phases):
    """ func is a function which returns a pyLikelihood object 
        when phased in a phase. """

    like = func(PhaseRange(0,1))

    # freeze index of PWN
    index=like[like.par_index(name, 'Index')]
    index.setTrueValue(-2)
    index.setFree(0)

    def fix_prefactor(like):
        prefactor=like[like.par_index(name, 'Prefactor')]
        prefactor.setFree(1)
        prefactor.setBounds(1e-10,1e10) 
        # now, save current ROI
        like.syncSrcParams()

    fix_prefactor(like)
    
    paranoid_gtlike_fit(like, covar=False)

    # freeze everything but prefactor of PWN

    for i in range(len(like.model.params)):
        like.freeze(i)

    # set prefactor free
    fix_prefactor(like)

    like.syncSrcParams()

    saved_state = LikelihoodState(like)
    TS = np.empty_like(phases)

    for i,phase in enumerate(phases):

        like = func(phase)
        fix_prefactor(like) # kind of lame, but I think this is needed

        # give model the same parameters as global fit.
        saved_state.like = like
        saved_state.restore()

        paranoid_gtlike_fit(like, covar=False)

        # n.b. no need to reoptimize since only one fit parameter!
        TS[i] = like.Ts(name,reoptimize=False)

        print 'Loop %4d/%4d: phase=%s, TS=%.1f' % (i+1,len(phases),str(phase),TS[i])

    return TS


results=dict()

parser = ArgumentParser()
parser.add_argument("--pwndata", required=True)
parser.add_argument("-p", "--pwnphase", required=True)
parser.add_argument("-n", "--name", required=True, help="Name of the pulsar")
parser.add_argument("--emin", default=1e2, type=float)
parser.add_argument("--emax", default=10**5.5, type=float)
args=parser.parse_args()

name=args.name
good_phase=PhaseRange(yaml.load(open(args.pwnphase))[name]['phase'])

phase_center = good_phase.phase_center
good_dphi = good_phase.phase_fraction
npts = 10
dphis = np.linspace(0,good_dphi+0.2, npts+1)[1:]
phases = [PhaseRange(phase_center-dphi/2, phase_center+dphi/2) for dphi in dphis]


def func(phase):
    roi=setup_pwn(phase=phase, 
                  name=name, pwndata=args.pwndata,
                  free_radius=5, max_free=10, 
                  fit_emin=args.emin, fit_emax=args.emax,
                  skip_setup=True)
    # make sure gtlike object exists so that it's destructor
    # is not called
    global gtlike 
    gtlike = Gtlike(roi, optimizer='NEWMINUIT')
    return gtlike.like

print 'good_phase = %s, %s +/- %s' % (good_phase, phase_center, good_dphi/2)

results['dphis'] = dphis
results['phases'] = phases
results['TS'] = thierry_profile(name, func, phases)

save_results(results,name)

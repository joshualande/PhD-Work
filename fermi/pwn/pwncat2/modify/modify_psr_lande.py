import os,sys
from os.path import expandvars
folder = os.path.dirname(__file__)
sys.path.append(folder)
import modify_psr_base

import numpy as np

from skymaps import SkyDir
from uw.like.pointspec_helpers import PointSource
from uw.like.Models import PowerLaw, SmoothBrokenPowerLaw, SumModel, FileFunction, LogParabola, PLSuperExpCutoff
from uw.like.SpatialModels import Disk
from uw.like.roi_extended import ExtendedSource

from lande.utilities.math import overlaps
from lande.fermi.pipeline.pwncat2.analysis.setup import PWNRegion

def modify_roi(name,roi):
    modify_psr_base.modify_roi(name,roi)

    e0=np.sqrt(1e2*10**5.5)

    def fix_gamma_cygni_region(roi):
        # delete source associated with Gamma Cygni SNR
        roi.del_source(which='2FGL J2019.1+4040')

        # Free the pulsar component
        roi.modify(which='2FGL J2021.5+4026', free=True)

        # Add in Gamma Cygni SNR using best fit parmaeters
        # From extended source search paper
        model = PowerLaw(index=2.42)
        model.set_flux(2e-9,emin=1e4,emax=1e5)
        model.set_default_limits(oomp_limits=True)
        es=ExtendedSource(name='Gamma Cygni',
                          model=model,
                          spatial_model=Disk(l=78.24,b=2.20,sigma=0.63))
        roi.add_source(es)


    if name == 'PSRJ0007+7303':
        print 'fixing starting value of %s' % name
        # In previous analysis, I found trouble converging for some hypothesis,
        # so start out with best spectral parameters

        # best fit parmaters taken from:
        # $pwndata/spectral/v8/analysis_no_plots/PSRJ0007+7303/results_PSRJ0007+7303.yaml
        modify_psr_base.set_flux_index(roi,name,5.637887384602554e-08,2.869750880323576)

    if name == 'PSRJ0023+0923':
        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0023+0923/v1/iteration_v1/run.py
        roi.modify(which="2FGL J0030.4+0450", free=True)

    if name == 'PSRJ0034-0534':
        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0034-0534/v1/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(110.964540896,-64.5075870689,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=8.26279236249e-15, index=2.58385504461, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ0102+4839':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0102+4839/v1/iteration_v1/run.py
        model=PowerLaw(norm=4.77276e-13, index=2.01965, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(127.789190256,-10.6871258101,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0102+4839/v1/iteration_v2/run.py
        model=PowerLaw(norm=2.6108e-13, index=1.77088, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(124.936171519,-17.8324907932,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0106+4855':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0106+4855/v1/iteration_v1/run.py
        model=PowerLaw(norm=3.2257e-13, index=1.79886, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(124.902581145,-17.8410812906,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0218+4232':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0218+4232/v1/iteration_v1/run.py
        model=PowerLaw(norm=7.41413e-13, index=2.16066, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(141.890006495,-20.0283413292,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0205+6449':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0205+6449/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(132.964587372,-0.940630424813,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.32743634755e-14, index=2.20294569667, e0=5623.4132519, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ0248+6021':

        # Values taken from $pwnpersonal/individual_sources/PSRJ0248+6021/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.89676e-12, index=2.54806, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(136.651028662,1.91638928353,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0248+6021/v2/iteration_v1/run.py
        model=PowerLaw(norm=1.39429e-12, index=2.39466, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(139.079106372,3.96339422846,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0248+6021/v2/iteration_v2/run.py
        roi.modify(which="2FGL J0218.7+6208c", free=True)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0248+6021/v2/iteration_v2/run.py
        roi.modify(which="2FGL J0218.7+6208c", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0248+6021/v2/iteration_v3/run.py
        model=PowerLaw(norm=7.99365289489e-14, index=2.56703331102, e0=np.sqrt(1e2*1e5))
        model.set_e0(e0)
        PWNRegion.limit_powerlaw(model)
        roi.modify(which='PSRJ0248+6021', model=model, keep_old_flux=False)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0248+6021/v3/iteration_v1/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(133.736134754,2.14221240226,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.49074649752e-14, index=2.20958899123, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0248+6021/v3/iteration_v2/run.py
        ps=PointSource(name='seed4', 
                       skydir=SkyDir(133.10343155,0.552774015125,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.96535891768e-14, index=2.35951487861, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0248+6021/v3/iteration_v3/run.py
        ps=PointSource(name='seed5', 
                       skydir=SkyDir(136.81779912,-3.17459488184,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.75401557545e-14, index=2.35400774839, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

                        

    if name == 'PSRJ0357+3205':
        # Values taken from $pwnpersonal/individual_sources/PSRJ0357+3205/v1/iteration_v1/run.py

        model=PowerLaw(norm=1.50764e-12, index=2.36031, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(160.336172309,-17.3616171342,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0357+3205/v2/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(159.702267353,-19.8307979676,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.45817462191e-14, index=2.1079192233, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ0534+2200':
        # (a) fix spectrum of crab

        # Parameters taken from arXiv:1112.1979v2
        # and $pwnpersonal/individual_sources/PSRJ0534+2200/v2/iteration_v1/run.py

        sync = PowerLaw(index=3.59)
        sync.set_flux(6.1e-7, emin=100, emax=np.inf) 
        ic = SmoothBrokenPowerLaw(index_1=1.48, index_2=2.19, e_break=13.9e3, beta=0.2)
        ic.set_flux(1.1e-7, emin=100, emax=np.inf)

        sum_model = SumModel(sync, ic)

        filename=expandvars('$PWD/crab_spectrum.txt')
        sum_model.save_profile(filename, emin=10, emax=1e6)

        model = FileFunction(file=filename)
        roi.modify(which='PSRJ0534+2200', model=model)

        # (b) add nearby source

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0534+2200/v2/iteration_v2/run.py
        model=PowerLaw(norm=2.06176e-12, index=2.56593, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(183.728621429,-4.08423898725,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0610-2100':
        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0610-2100/v1/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(225.694339988,-21.549265187,SkyDir.GALACTIC),
                       model=PowerLaw(norm=2.37549296687e-14, index=1.86277032208, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ0613-0200':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0613-0200/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.21954e-12, index=2.26465, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(213.710766254,-11.4496875154,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0613-0200/v2/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(214.346071714,-12.5653145742,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.24542973495e-14, index=1.89620011191, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ0631+1036':

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0631+1036/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.36144e-12, index=2.24104, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(201.96840164,2.63238059482,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0631+1036/v2/iteration_v2/run.py
        roi.modify(which="2FGL J0633.9+1746", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0631+1036/v2/iteration_v3/run.py
        roi.modify(which="2FGL J0633.7+0633", free=True)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0631+1036/v2/iteration_v4/run.py
        roi.modify(which="2FGL J0633.9+1746", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0631+1036/v2/iteration_v5/run.py
        model=PowerLaw(norm=9.55962564961e-14, index=2.333032306, e0=np.sqrt(10*1e5))
        model.set_e0(e0)
        PWNRegion.limit_powerlaw(model)
        roi.modify(which='PSRJ0631+1036', model=model, keep_old_flux=False)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0631+1036/v2/iteration_v6/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(205.749565711,-2.73839381012,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.84059647317e-12, index=2.17956292598, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0631+1036/v2/iteration_v8/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(206.202996049,1.38579439903,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.38824869801e-14, index=2.56059537015, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ0633+0632':

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0633+0632/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.87896e-12, index=2.52495, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(206.228771742,1.5374031115,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0633+0632/v1/iteration_v2/run.py
        model=PowerLaw(norm=1.48345e-12, index=2.20523, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(205.763876721,-2.72839852568,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0633+0632/v1/iteration_v3/run.py
        model=PowerLaw(norm=1.20463e-12, index=1.9803, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(207.059007704,-1.90816325068,SkyDir.GALACTIC)
        ps=PointSource(name="seed3", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0633+0632/v2/iteration_v1/run.py
        roi.modify(which="2FGL J0631.5+1035", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0633+0632/v3/iteration_v1/run.py
        ps=PointSource(name='seed4', 
                       skydir=SkyDir(202.040565397,2.68882299212,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.16073773691e-14, index=2.20995284143, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ0659+1414':
        roi.modify(which="2FGL J0633.9+1746", free=True)


    if name == 'PSRJ0729-1448':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0729-1448/v1/iteration_v1/run.py
        model=PowerLaw(norm=2.11637e-12, index=2.33741, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(233.900470646,-0.220997218399,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0729-1448/v2/iteration_v1/run.py
        ps=PointSource(name='seed2',
                       skydir=SkyDir(225.816371551,-0.138344375555,SkyDir.GALACTIC),
                       model=PowerLaw(norm=2.65594443751e-14, index=2.14551904557, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ0734-1559':

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0734-1559/v1/iteration_v1/run.py
        model=PowerLaw(norm=2.39292e-12, index=2.36721, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(233.928276957,-0.176812544449,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0734-1559/v1/iteration_v2/run.py
        model=PowerLaw(norm=1.02789e-12, index=2.06358, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(231.291186104,-0.0769198428432,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0742-2822':
        # Parameters came from $pwnpersonal/individual_sources/PSRJ0742-2822/v1/iteration_v1/run.py
        model=PowerLaw(norm=3.53607e-13, index=1.80772, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(244.483009084,-4.72149826403,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0742-2822/v2/iteration_v1/run.py
        model=PowerLaw(norm=1.18032e-12, index=2.32253, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(239.823388505,0.825787353838,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0742-2822/v2/iteration_v2/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(243.455924363,0.337746130836,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.27745360307e-12, index=2.36442816303, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ0751+1807':

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0751+1807/v1/iteration_v1/run.py
        model = PowerLaw(norm=4.48e-13, index=2.28, e0=1e3)
        PWNRegion.limit_powerlaw(model)
        roi.modify(which='PSRJ0751+1807',
                   model=model,
                   keep_old_flux=True)

    if name == 'PSRJ0835-4510':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ0835-4510/v1/iteration_v1/run.py
        model=PowerLaw(norm=3.38097e-12, index=2.41688, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(262.832249309,0.643797379224,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Modify Vela X spectrum to be same as published results from 
        #  -> "THE VELA-X PULSAR WIND NEBULA REVISITED WITH 4 YEARS OF FERMI LARGE AREA TELESCOPE OBSERVATIONS" - Grondin et al 2013
        model = SmoothBrokenPowerLaw(index_1=1.83, index_2=2.87, e_break=2.1e3, beta=0.2)
        model.set_flux(1.83e-7, emin=200, emax=np.inf)

        filename=expandvars('$PWD/vela_x_spectrum.txt')
        model.save_profile(filename, emin=10, emax=1e6)

        model = FileFunction(file=filename)
        roi.modify(which='PSRJ0835-4510', model=model)

    if name == 'PSRJ0908-4913':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0908-4913/v1/iteration_v1/run.py
        roi.modify(which="2FGL J0835.3-4510", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0908-4913/v1/iteration_v2/run.py
        model=PowerLaw(norm=1.61329e-12, index=2.21098, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(271.258995834,0.149243337966,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0908-4913/v1/iteration_v4/run.py
        model=PowerLaw(norm=8.78234e-13, index=1.77965, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(266.592361248,-1.93883515163,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0908-4913/v1/iteration_v5/run.py
        model=PowerLaw(norm=9.08555e-13, index=1.81663, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(267.884950765,-0.934447309326,SkyDir.GALACTIC)
        ps=PointSource(name="seed3", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0908-4913/v2/iteration_v1/run.py
        roi.modify(which="2FGL J0848.5-4535", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0908-4913/v2/iteration_v2/run.py
        model=PowerLaw(norm=7.10292e-13, index=1.71194, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(265.681421785,-1.59476651574,SkyDir.GALACTIC)
        ps=PointSource(name="seed4", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0908-4913/v3/iteration_v1/run.py
        ps=PointSource(name='seed5', 
                       skydir=SkyDir(269.143816897,-0.361496692877,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.7076131973e-14, index=2.26686119207, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0908-4913/v3/iteration_v2/run.py
        ps=PointSource(name='seed6', 
                       skydir=SkyDir(270.080486048,1.38972959516,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.98849388238e-14, index=2.25850466269, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0908-4913/v3/iteration_v3/run.py
        roi.modify(which="2FGL J0848.5-4535", free=True)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0908-4913/v4/iteration_v1/run.py
        ps=PointSource(name='seed7', 
                       skydir=SkyDir(265.345555019,-1.09781037034,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=4.47740909044e-14, index=1.81480284629, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0908-4913/v4/iteration_v2/run.py
        roi.modify(which="2FGL J0835.3-4510", free=True)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ0908-4913/v4/iteration_v3/run.py
        ps=PointSource(name='seed8', 
                       skydir=SkyDir(264.246967292,1.70997109274,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.79814535525e-14, index=2.23003856044, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1023-5746':

        # In previous analysis v9:
        # $pwndata/spectral/v9/analysis_no_plots/PSRJ1023-5746/results_PSRJ1023-5746.yaml
        # I found that this source had large residual surrounding it. So always fit it
        roi.modify(which='2FGL J1044.5-5737', free=True)

        # v9: Add new source 'seed1' that represents residual found in the TSmap at the top left
        # (in galactic coordinates) at (l,b)=(286.252,0.522)
        # The best fit parameters of this new source are taken from
        # $pwnpersonal/individual_sources/PSRJ1023-5746/v1/iteration_v1/run.py
        ps1 = PointSource(name='seed1',
                         skydir=SkyDir(286.2517892658979,0.5217112872908655,SkyDir.GALACTIC),
                         model=PowerLaw(norm=3.8835219935993907e-12,index=2.2310422346640504, set_default_oomp_limits=True))
        roi.add_source(ps1)

        # v10: Add new source 'seed2' that represents additional residual found from
        # $pwnpersonal/individual_sources/PSRJ1023-5746/v2/iteration_v1/run.py
        ps2 = PointSource(name='seed2',
                         skydir=SkyDir(284.5071255898265,0.9734675040757886,SkyDir.GALACTIC),
                         model=PowerLaw(norm=2.787037074673656e-12,index=2.2750149645582809, set_default_oomp_limits=True))
        roi.add_source(ps2)

        # Parameters came from $pwnpersonal/individual_sources/PSRJ1023-5746/v3/v1/iteration_v1/run.py
        model=PowerLaw(norm=9.81327e-13, index=1.64754, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(285.184506369,-0.0773421350636,SkyDir.GALACTIC)
        ps=PointSource(name="seed3", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1023-5746/v4/iteration_v1/run.py
        roi.modify(which="2FGL J1048.2-5831", free=True)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1023-5746/v5/iteration_v1/run.py
        ps=PointSource(name='seed4', 
                       skydir=SkyDir(283.606607326,4.61782779689,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.94465169935e-14, index=2.29954918403, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1023-5746/v5/iteration_v3/run.py
        roi.modify(which="2FGL J1057.9-5226", free=True)



    if name == 'PSRJ1016-5857':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1016-5857/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1028.5-5819", free=True)
        roi.modify(which="2FGL J1036.4-5828c", free=True)
        roi.modify(which="2FGL J1048.2-5831", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1016-5857/v1/iteration_v2/run.py
        roi.modify(which="2FGL J1045.0-5941", free=True)
        roi.modify(which="2FGL J1044.5-5737", free=True)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1016-5857/v1/iteration_v3/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(286.97826923,-0.591156387185,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.14924296445e-12, index=2.00185132576, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1016-5857/v1/iteration_v4/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(285.25434511,0.533887711276,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.55632957386e-12, index=2.19992738577, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1016-5857/v2/iteration_v1/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(287.257551757,-2.19684021719,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.65241642288e-14, index=2.11920692485, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)



    if name == 'PSRJ1019-5749':
        
        # Analysis came from $pwnpersonal/individual_sources/PSRJ1019-5749/v1/iteration_v2/run.py
        roi.modify(which='2FGL J1028.5-5819', free=True)
        roi.modify(which='2FGL J1036.4-5828c', free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1019-5749/v1/iteration_v2/run.py
        model=PowerLaw(norm=3.71803e-12, index=2.51986, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(285.580986429,0.56400926783,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1019-5749/v1/iteration_v3/run.py
        roi.modify(which="2FGL J1048.2-5831", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1019-5749/v1/iteration_v4/run.py
        model=PowerLaw(norm=2.83122e-12, index=2.29234, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(284.482071165,0.671568823511,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1019-5749/v2/iteration_v1/run.py
        model=PowerLaw(norm=2.31069e-12, index=2.37913, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(287.860104893,-1.3756364096,SkyDir.GALACTIC)
        ps=PointSource(name="seed3", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1019-5749/v3/iteration_v1/run.py
        roi.modify(which="2FGL J1044.5-5737", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1019-5749/v3/iteration_v2/run.py
        ps=PointSource(name='seed4', 
                       skydir=SkyDir(286.575380561,-0.948190723903,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.76182795299e-14, index=1.89696134898, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1019-5749/v3/iteration_v4/run.py
        roi.modify(which="2FGL J1057.9-5226", free=True)



    if name == 'PSRJ1028-5819':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ1028-5819/v1/iteration_v1/run.py
        roi.modify(which='2FGL J1044.5-5737', free=True)
        roi.modify(which='2FGL J1048.2-5831', free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1028-5819/v1/iteration_v2/run.py
        model=PowerLaw(norm=3.23885e-12, index=2.14376, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(285.511479051,0.742991500068,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1028-5819/v2/iteration_v1/run.py
        model=PowerLaw(norm=3.35481e-12, index=2.11961, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(283.805447725,-0.715796302543,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1028-5819/v2/iteration_v2/run.py
        model=PowerLaw(norm=1.81777e-12, index=1.95643, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(287.091319865,-0.93052274267,SkyDir.GALACTIC)
        ps=PointSource(name="seed3", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1028-5819/v3/iteration_v2/run.py
        roi.modify(which="2FGL J1057.9-5226", free=True)
        roi.modify(which="2FGL J1118.8-6128", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1028-5819/v3/iteration_v3/run.py
        ps=PointSource(name='seed4', 
                       skydir=SkyDir(290.440317179,-3.96639941416,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.87891183147e-14, index=2.57266986846, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1028-5819/v4/iteration_v1/run.py
        ps=PointSource(name='seed5', 
                       skydir=SkyDir(290.01352881,-0.84539074006,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.65345019653e-14, index=2.25877019009, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1044-5737':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ1044-5737/v1/iteration_v1/run.py
        roi.modify(which='2FGL J1023.5-5749c', free=True)
        roi.modify(which='2FGL J1022.7-5741', free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1044-5737/v1/iteration_v2/run.py
        roi.modify(which="2FGL J1028.5-5819", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1044-5737/v1/iteration_v3/run.py
        model=PowerLaw(norm=1.45355e-12, index=1.81839, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(285.230741326,0.0446637805384,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1044-5737/v3/iteration_v2/run.py
        roi.modify(which="2FGL J1057.9-5226", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1044-5737/v3/iteration_v3/run.py
        roi.modify(which="2FGL J1118.8-6128", free=True)
        roi.modify(which="2FGL J1112.5-6105", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1044-5737/v3/iteration_v4/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(290.698555174,-4.11634105539,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.14890436526e-14, index=2.69098137906, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1044-5737/v3/iteration_v5/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(289.943343411,-0.887164456861,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.58987965645e-14, index=2.37854404779, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1044-5737/v3/iteration_v6/run.py
        ps=PointSource(name='seed4', 
                       skydir=SkyDir(287.798317109,-1.37048513642,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=4.9647349951e-14, index=1.91563329088, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1044-5737/v3/iteration_v7/run.py
        ps=PointSource(name='seed5', 
                       skydir=SkyDir(286.625921611,-1.00877418344,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.28674022223e-14, index=2.19111237861, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1044-5737/v3/iteration_v8/run.py
        ps=PointSource(name='seed6',
                       skydir=SkyDir(283.869459928,-0.687935488709,SkyDir.GALACTIC),
                       model=PowerLaw(norm=8.30720630373e-14, index=2.27835472383, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1044-5737/v4/iteration_v1/run.py
        ps=PointSource(name='seed7',
                       skydir=SkyDir(284.353940021,0.7478882094,SkyDir.GALACTIC),
                       model=PowerLaw(norm=4.93545496966e-14, index=2.12308006562, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1044-5737/v4/iteration_v3/run.py
        ps=PointSource(name='seed8',
                       skydir=SkyDir(291.58193627,-0.997368829599,SkyDir.GALACTIC),
                       model=PowerLaw(norm=5.61618504835e-14, index=2.47430711974, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1044-5737/v4/iteration_v4/run.py
        ps=PointSource(name='seed9',
                       skydir=SkyDir(283.369341709,4.8188847473,SkyDir.GALACTIC),
                       model=PowerLaw(norm=1.85759342156e-14, index=1.80350193598, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)



    if name == 'PSRJ1048-5832':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1048-5832/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1028.5-5819", free=True)


        # Analysis came from $pwnpersonal/individual_sources/PSRJ1048-5832/v1/iteration_v2/run.py
        model=PowerLaw(norm=2.62919e-12, index=2.3449, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(289.735306739,-1.00596563899,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1048-5832/v2/iteration_v1/run.py
        roi.modify(which="2FGL J1023.5-5749c", free=True)
        roi.modify(which="2FGL J1022.7-5741", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1048-5832/v2/iteration_v2/run.py
        roi.modify(which="2FGL J1118.8-6128", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1048-5832/v2/iteration_v3/run.py
        roi.modify(which="2FGL J1057.9-5226", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1048-5832/v2/iteration_v4/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(290.526243375,-4.03942714917,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.13167674464e-12, index=2.58383864576, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1048-5832/v3/iteration_v1/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(291.492702478,-0.997532362926,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=6.1328576585e-14, index=2.2837287097, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1048-5832/v3/iteration_v2/run.py
        roi.modify(which="2FGL J1016.5-5858", free=True)

    if name == 'PSRJ1057-5226':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1057-5226/v1/iteration_v2/run.py
        roi.modify(which="2FGL J1044.5-5737", free=True)
        roi.modify(which="2FGL J1048.2-5831", free=True)
        roi.modify(which="2FGL J1023.5-5749c", free=True)
        roi.modify(which="2FGL J1022.7-5741", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1057-5226/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(288.883595605,9.12046975096,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.73070629043e-14, index=2.18474280097, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ1105-6107':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ1105-6107/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1044.5-5737", free=True)
        roi.modify(which="2FGL J1048.2-5831", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1105-6107/v1/iteration_v2/run.py
        model=PowerLaw(norm=4.53159e-12, index=2.44334, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(285.793515139,0.325479474916,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1105-6107/v1/iteration_v3/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(289.948506928,-0.830471890337,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.8320279121e-12, index=2.36395151488, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1105-6107/v2/iteration_v1/run.py
        ps=PointSource(name='seed3',
                       skydir=SkyDir(291.551458554,-0.942285626869,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.77023949242e-14, index=2.27423787191, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1105-6107/v3/iteration_v2/run.py
        roi.modify(which="2FGL J1028.5-5819", free=True)
        roi.modify(which="2FGL J1027.4-5730c", free=True)
        roi.modify(which="2FGL J1023.5-5749c", free=True)
        roi.modify(which="2FGL J1022.7-5741", free=True)

    if name == 'PSRJ1112-6103':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1112-6103/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1048.2-5831", free=True)
        roi.modify(which="2FGL J1044.5-5737", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1112-6103/v1/iteration_v3/run.py
        roi.modify(which="2FGL J1057.9-5226", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1112-6103/v1/iteration_v4/run.py
        roi.modify(which="2FGL J1023.5-5749c", free=True)
        roi.modify(which="2FGL J1022.7-5741", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1112-6103/v1/iteration_v5/run.py
        roi.modify(which="2FGL J1028.5-5819", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1112-6103/v1/iteration_v7/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(285.225337117,0.514641784821,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.32679272159e-14, index=2.12539171017, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1112-6103/v2/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(286.331559215,0.436359341364,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.13524192428e-14, index=2.23376160876, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1112-6103/v2/iteration_v3/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(290.807794747,-5.2224967519,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.52234878325e-14, index=2.43747335211, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ1119-6127':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1119-6127/v3/iteration_v1/run.py
        roi.modify(which="2FGL J1048.2-5831", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1119-6127/v3/iteration_v2/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(290.819839798,-5.17106330164,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.16391102291e-12, index=2.29201502328, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1119-6127/v3/iteration_v3/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(291.699208089,-0.593683071023,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.55707444394e-12, index=2.24782583172, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1124-5916':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1124-5916/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1048.2-5831", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1124-5916/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1048.2-5831", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1124-5916/v1/iteration_v2/run.py
        roi.modify(which="2FGL J1118.8-6128", free=True)
        roi.modify(which="2FGL J1112.5-6105", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1124-5916/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(291.410969636,-1.06695058463,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=6.14897035106e-14, index=2.2847948902, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1125-5825':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1125-5825/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1048.2-5831", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1125-5825/v1/iteration_v2/run.py
        roi.modify(which="2FGL J1118.8-6128", free=True)
        roi.modify(which="2FGL J1112.5-6105", free=True)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1125-5825/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(290.923761196,-1.43349694811,SkyDir.GALACTIC),
                       model=PowerLaw(norm=3.65697804225e-14, index=2.22989651495, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1125-5825/v2/iteration_v3/run.py
        roi.modify(which="2FGL J1044.5-5737", free=True)
        roi.modify(which="2FGL J1057.9-5226", free=True)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1125-5825/v2/iteration_v4/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(291.59743439,-0.718322470073,SkyDir.GALACTIC),
                       model=PowerLaw(norm=6.05036445019e-14, index=2.30946919684, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1125-5825/v2/iteration_v5/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(289.902647311,-0.829581974359,SkyDir.GALACTIC),
                       model=PowerLaw(norm=4.32579535457e-14, index=2.12698223643, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)




    if name == 'PSRJ1357-6429':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ1357-6429/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1418.7-6058", free=True)
        roi.modify(which="2FGL J1420.1-6047", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1357-6429/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(311.04136852,-5.02714294892,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.04615127537e-14, index=2.04884500014, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1357-6429/v2/iteration_v2/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(306.00940961,-1.47217408331,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=4.08909893471e-14, index=2.31824295231, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1357-6429/v2/iteration_v3/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(312.442405622,0.352694217469,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=7.00851281392e-14, index=1.64320243565, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1410-6132':
        
        # Avoid convergence failures. 
        # Parameters from $pwnpersonal/individual_sources/PSRJ1410-6132/v1/iteration_v1/ run.py
        model=PowerLaw(norm=4.98e-12, index=2.08, e0=1000)
        model.set_e0(e0)
        PWNRegion.limit_powerlaw(model)
        roi.modify(which='PSRJ1410-6132',
                   model=model,
                   keep_old_flux=False)

        roi.modify(which='2FGL J1405.5-6121',
                   model=LogParabola(norm=6.25e-12, index=2.15, beta=0.21, e_break=1.5e+03, set_default_oomp_limits=True),
                   keep_old_flux=False)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1410-6132/v2/iteration_v1/run.py
        roi.modify(which="2FGL J1356.0-6436", free=True)

    if name == 'PSRJ1413-6205':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1413-6205/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1420.1-6047", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1413-6205/v1/iteration_v2/run.py
        roi.modify(which="2FGL J1356.0-6436", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1413-6205/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(312.362809818,3.99583070479,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.2103886838e-14, index=1.66163594909, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ1418-6058':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1418-6058/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1413.4-6204", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1418-6058/v2/iteration_v1/run.py
        roi.modify(which="2FGL J1459.4-6054", free=True)

    if name == 'PSRJ1420-6048':
        print 'fixing starting value of %s' % name
        # In previous analysis, I found trouble converging for some hypothesis,
        # so start out with best spectral parameters

        # best fit parmaters taken from:
        # $pwndata/spectral/v8/analysis_no_plots/PSRJ1420-6048/results_PSRJ1420-6048.yaml
        modify_psr_base.set_flux_index(roi,name,1.4239401328058901e-08,1.8751316333602417)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1420-6048/v1/iteration_v1/run.py    
        roi.modify(which="2FGL J1413.4-6204", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1420-6048/v2/iteration_v1/run.py
        roi.modify(which="2FGL J1459.4-6054", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1420-6048/v3/iteration_v1/run.py
        roi.modify(which="2FGL J1356.0-6436", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1420-6048/v3/iteration_v2/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(312.408117799,4.00675148596,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.78103968833e-14, index=1.9303682476, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1420-6048/v3/iteration_v3/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(312.256044999,2.82079439362,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.04313642181e-14, index=1.6579090066, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ1429-5911':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1429-5911/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1509.6-5850", free=True)
        roi.modify(which="2FGL J1459.4-6054", free=True)
        roi.modify(which="2FGL J1413.4-6204", free=True)

    if name == 'PSRJ1446-4701':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1446-4701/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.0112e-12, index=2.33614, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(320.908389496,14.741711492,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1446-4701/v2/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(317.759695414,13.6270498797,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=9.06513561447e-15, index=2.64423254638, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1459-6053':
        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1459-6053/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1420.1-6047", free=True)
        roi.modify(which="2FGL J1418.7-6058", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1459-6053/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(315.815555128,-5.48719056996,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.20422925696e-14, index=2.39327282263, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1509-5850':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1509-5850/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1459.4-6054", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1509-5850/v3/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(317.400527018,-5.08655662094,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.3726717868e-14, index=2.1205308173, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ1513-5908':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ1513-5908/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1459.4-6054", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1513-5908/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(316.720976626,-5.3160438512,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.85739913047e-14, index=2.28455581008, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1531-5610':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1531-5610/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1509.6-5850", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1531-5610/v2/iteration_v1/run.py
        ps=PointSource(name='seed1',
                       skydir=SkyDir(326.358582371,2.81019207584,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.52269259203e-14, index=1.68424234239, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1600-3053':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1600-3053/v2/iteration_v1/run.py
        ps=PointSource(name='seed1',
                       skydir=SkyDir(345.953356271,14.6873812264,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.04297662956e-14, index=2.06408110925, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1614-2230':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1614-2230/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1625.7-2526", free=True)

    if name == 'PSRJ1620-4927':
        print 'fixing starting value of %s' % name
        # In previous analysis, I found trouble converging for some hypothesis,
        # so start out with best spectral parameters

        # best fit parmaters taken from:
        # $pwndata/spectral/v8/analysis_no_plots/PSRJ1620-4927/results_PSRJ1620-4927.yaml
        modify_psr_base.set_flux_index(roi,name,4.605558542777753e-08,2.0941239204631703)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1620-4927/v2/iteration_v1/run.py
        model=PowerLaw(norm=4.67995e-12, index=2.11003, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(333.008696871,0.0306605245011,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1620-4927/v3/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(338.478730801,-2.20318338762,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.65544415397e-12, index=2.33480583109, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ1648-4611':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1648-4611/v1/iteration_v2/run.py
        roi.modify(which="2FGL J1709.7-4429", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1648-4611/v1/iteration_v3/run.py
        model=PowerLaw(norm=1.98727e-12, index=2.44488, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(339.187684989,-4.31868997792,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1648-4611/v2/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(338.39806147,-2.18088902122,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.39900594325e-14, index=2.11105486918, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1648-4611/v2/iteration_v2/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(339.163009228,3.07721990434,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=4.1024867815e-14, index=1.86249007958, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1658-5324':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ1658-5324/v1/iteration_v1/run.py
        model=PowerLaw(norm=7.25394e-13, index=1.9179, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(333.799799064,-8.62492903066,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1658-5324/v1/iteration_v2/run.py
        model=PowerLaw(norm=1.43796e-12, index=2.38295, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(336.992952017,-5.44100960768,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1658-5324/v2/iteration_v1/run.py
        model=PowerLaw(norm=6.25471e-12, index=2.25546, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(339.305979877,-1.30488371278,SkyDir.GALACTIC)
        ps=PointSource(name="seed3", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1658-5324/v2/iteration_v2/run.py
        ps=PointSource(name='seed4', 
                       skydir=SkyDir(338.296907879,-2.04576357985,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.27541586467e-12, index=2.40057243748, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ1702-4128':
        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1702-4128/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1718.3-3827", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1702-4128/v1/iteration_v2/run.py
        roi.modify(which="2FGL J1714.5-3829", free=True)
        roi.modify(which="2FGL J1712.4-3941", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1702-4128/v2/iteration_v1/run.py
        roi.modify(which="2FGL J1714.5-3829", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1702-4128/v2/iteration_v2/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(347.597126309,-0.687316152386,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.18277842221e-14, index=1.4463378764, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1702-4128/v2/iteration_v3/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(344.381917096,-3.58283214283,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.63923540414e-14, index=2.34459579322, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1702-4128/v3/iteration_v1/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(348.300702378,-0.102780146588,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.17225189366e-13, index=2.11438552533, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)



    if name == 'PSRJ1709-4429':

        # Not sure, but this nearby source was fitting to a very unphysical
        # log-parabola bump in the v9 analysis of PSR J1709
        # $pwndata/spectral/v9/analysis_no_plots/PSRJ1709-4429/results_PSRJ1709-4429.yaml
        # so turn it into a more well behaved PowerLaw
        roi.modify(which='2FGL J1704.9-4618',
                   keep_old_flux=False,
                   model=PowerLaw(
                       norm=2.6400767608080404e-12,
                       index=2.6814468574367032,
                       e0=1000.0, set_default_oomp_limits=True))

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1709-4429/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(344.46706654,-3.5796427066,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=4.32852254873e-14, index=2.36455250515, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1709-4429/v2/iteration_v2/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(347.508851863,-0.703633261486,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.23731553365e-14, index=1.55724241688, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1709-4429/v2/iteration_v3/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(339.143335139,-4.2457206972,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.6239366048e-14, index=2.38679064814, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1709-4429/v2/iteration_v4/run.py
        ps=PointSource(name='seed4', 
                       skydir=SkyDir(338.380792845,-2.09588898957,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.77450257251e-14, index=2.17762318631, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)



    if name == 'PSRJ1718-3825':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1718-3825/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.06204e-12, index=1.56099, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(347.584694432,-0.681857494514,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1718-3825/v2/iteration_v2/run.py
        roi.modify(which="2FGL J1709.7-4429", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1718-3825/v2/iteration_v3/run.py
        roi.modify(which="2FGL J1732.5-3131", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1718-3825/v3/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(353.535765613,-5.07442572886,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.57463439345e-14, index=2.26689639259, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)



    if name == 'PSRJ1730-3350':

        roi.modify(which='2FGL J1737.2-3213',           
                   model=LogParabola(norm=1.17e-12, index=2.99, beta=0.571, e_break=2.16e+03, set_default_oomp_limits=True),
                   keep_old_flux=False)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1730-3350/v2/iteration_v1/run.py
        roi.modify(which="2FGL J1747.1-3000", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1730-3350/v3/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(358.746259714,-3.85892797658,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.24541432392e-14, index=2.20499173648, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1730-3350/v3/iteration_v2/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(357.812401855,3.60239368251,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.21402572576e-14, index=2.11673746506, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1730-3350/v4/iteration_v2/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(353.66122418,-4.97741091514,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.74612884963e-14, index=2.19630876064, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1730-3350/v4/iteration_v3/run.py
        roi.modify(which="2FGL J1718.3-3827", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1730-3350/v4/iteration_v4/run.py
        ps=PointSource(name='seed4', 
                       skydir=SkyDir(357.585875955,0.993249318189,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=6.45739424905e-14, index=2.05619573423, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1730-3350/v5/iteration_v1/run.py
        ps=PointSource(name='seed5',
                       skydir=SkyDir(356.945095127,-0.191215515818,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=7.65122300897e-14, index=2.01888080597, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)



    if name == 'PSRJ1732-3131':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1732-3131/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1747.1-3000", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1732-3131/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(359.896499565,0.67432692491,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.13790137991e-13, index=2.01834916389, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1732-3131/v2/iteration_v2/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(358.380896917,1.4706570954,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=7.0411134277e-14, index=1.843382924, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1732-3131/v3/iteration_v1/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(0.934053712025,1.49263160479,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=6.04948228472e-14, index=1.81567949427, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)



    if name == 'PSRJ1741-2054':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1741-2054/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1758.8-2402c", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1741-2054/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(6.0178920382,0.344470312517,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=8.23927076985e-14, index=2.0172897423, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1741-2054/v3/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(2.52843592933,3.68214891909,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.89984677103e-14, index=2.26787357201, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1744-1134':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1744-1134/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.72388137017e-13, index=2.27483263865, e0=np.sqrt(1e2*1e5))
        model.set_e0(e0)
        PWNRegion.limit_powerlaw(model)
        roi.modify(which='PSRJ1744-1134', 
                   model=model,
                   keep_old_flux=False)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1744-1134/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(13.8858245783,11.2382822948,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.32589811308e-14, index=1.86077083293, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1744-1134/v2/iteration_v2/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(17.4344461597,13.3869883672,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.56240866791e-14, index=2.19083839165, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1746-3239':

        # In previous analysis 
        # $pwndata/spectral/v9/analysis_no_plots/PSRJ1746-3239/results_PSRJ1746-3239.yaml
        # I found that this source was badly misfit, so set free
        roi.modify(which='2FGL J1747.1-3000', free=True)

        # In previous analysis 
        # $pwnpersonal/individual_sources/PSRJ1746-3239/v1/iteration_v1/run.py
        # I found the need for a new source
        ps = PointSource(name='seed1',
                         skydir=SkyDir(357.2349498889614,-1.0448205537267325,SkyDir.GALACTIC),
                         model=PowerLaw(norm=3.2270327105385296e-12,
                                        index=2.1855137088271537, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1746-3239/v2/iteration_v1/run.py
        roi.modify(which="2FGL J1732.5-3131", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1746-3239/v2/iteration_v2/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(359.680776399,1.22464915128,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.51982240786e-12, index=2.00499887044, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1746-3239/v3/iteration_v1/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(358.354717748,-2.63792512008,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=4.15747134896e-14, index=2.22310569138, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1746-3239/v3/iteration_v2/run.py
        ps=PointSource(name='seed4', 
                       skydir=SkyDir(1.28785401869,1.97903454631,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=4.84289509895e-14, index=1.94338964805, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)



    if name == 'PSRJ1747-2958':

        # In previous analysis 
        # $pwndata/spectral/v9/analysis_no_plots/PSRJ1747-2958/results_PSRJ1747-2958.yaml
        # I found that these sources were badly misfit

        # See $pwnpersonal/individual_sources/PSRJ1747-2958/v1/iteration_v1/run.py
        # for special analysis of region
        roi.modify(which='2FGL J1746.6-2851c', free=True)
        roi.modify(which='2FGL J1747.3-2825c', free=True)

        # This further away source is also not fit well. See
        # $pwndata/spectral/v10/analysis_plots/PSRJ1747-2958/plots/source_0.1_extended_PSRJ1747-2958.png
        roi.modify(which='2FGL J1732.5-3131', free=True)

        # After freeing those sources, I found a residual emission, which
        # I will model as a new source w/ arameters taken from
        # See $pwnpersonal/individual_sources/PSRJ1747-2958/v1/iteration_v1/run.py
        ps = PointSource(name='seed1',
                         skydir=SkyDir(265.609,-28.654),
                         model=PowerLaw(norm=4.54e-12,
                                        index=2.20, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1747-2958/v3/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(3.78813638492,3.02376982301,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.89755082789e-14, index=2.65471474759, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1747-4036':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1747-4036/v1/iteration_v1/run.py
        model=PowerLaw(norm=5.31456e-13, index=1.8748, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(350.765455165,-8.48679435559,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1747-4036/v2/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(353.585217898,-5.13100433808,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.67915426712e-14, index=2.28139568381, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1747-4036/v2/iteration_v3/run.py
        roi.modify(which="2FGL J1709.7-4429", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1747-4036/v2/iteration_v4/run.py
        roi.modify(which="2FGL J1718.3-3827", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1747-4036/v3/iteration_v2/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(354.634819301,-1.50991888727,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=4.0839312275e-14, index=2.4699979286, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1801-2451':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1801-2451/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1809.8-2332", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1801-2451/v2/iteration_v2/run.py
        roi.modify(which="2FGL J1741.9-2054", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1801-2451/v2/iteration_v3/run.py
        roi.modify(which="2FGL J1747.1-3000", free=True)
        roi.modify(which="2FGL J1833.6-2104", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1801-2451/v2/iteration_v4/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(359.850400942,0.799901961948,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=8.37060551567e-14, index=1.99876650994, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1801-2451/v3/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(0.447406681723,2.89592340459,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.73437154305e-14, index=1.9527142892, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1801-2451/v4/iteration_v1/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(2.4748057343,3.58322435928,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.32828348763e-14, index=2.28861657031, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ1803-2149':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1803-2149/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1809.8-2332", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1803-2149/v2/iteration_v1/run.py
        roi.modify(which="2FGL J1741.9-2054", free=True)

    if name == 'PSRJ1809-2332':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1809-2332/v2/iteration_v1/run.py
        roi.modify(which="2FGL J1833.6-2104", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1809-2332/v2/iteration_v2/run.py
        model=PowerLaw(norm=2.40015523271e-13, index=2.51029888415, e0=np.sqrt(1e2*1e5))
        model.set_e0(e0)
        PWNRegion.limit_powerlaw(model)
        roi.modify(which='PSRJ1809-2332', 
                   model=model,
                   keep_old_flux=False)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1809-2332/v3/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(5.8879124236,0.288477499519,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=9.98029549858e-14, index=1.91465083972, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1810+1744':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1810+1744/v1/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(41.1412374152,13.1430254992,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.74396681577e-14, index=2.26238985693, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ1813-1246':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1813-1246/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1826.1-1256", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1813-1246/v1/iteration_v2/run.py
        roi.modify(which="2FGL J1833.6-1032", free=True)

    if name == 'PSRJ1823-3021A':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1823-3021A/v2/iteration_v2/run.py
        ps=PointSource(name='seed1',
                       skydir=SkyDir(6.05832844512,-3.72446949444,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.44678749683e-14, index=2.90225670983, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1823-3021A/v3/iteration_v1/run.py
        ps=PointSource(name='seed2',
                       skydir=SkyDir(2.05187379899,-6.76880908783,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.99460008569e-14, index=1.87219474918, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1826-1256':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1826-1256/v1/iteration_v3/run.py
        roi.modify(which="2FGL J1833.6-1032", free=True)
        roi.modify(which="2FGL J1813.4-1246", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1826-1256/v2/iteration_v1/run.py
        ps=PointSource(name='seed1',
                       skydir=SkyDir(20.6028370894,-4.22690808715,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=4.2159239189e-14, index=2.09900040555, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /afs/slac.stanford.edu/u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1826-1256/v3/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(17.1016392913,1.14480915359,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=8.02506198541e-14, index=2.22959323884, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1833-1034':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1833-1034/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1826.1-1256", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1833-1034/v1/iteration_v2/run.py
        roi.modify(which="2FGL J1813.4-1246", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1833-1034/v1/iteration_v3/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(18.7653292747,1.93018606947,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=6.33563253524e-14, index=1.90201589085, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1833-1034/v1/iteration_v4/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(18.8686531205,-1.02998056239,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=9.56493141083e-14, index=2.18407833596, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1833-1034/v1/iteration_v5/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(16.6985942654,0.102578758263,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=8.10025554682e-14, index=2.42976385092, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1835-1106':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1835-1106/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1813.4-1246", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1835-1106/v1/iteration_v2/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(21.7696608987,-6.05486195427,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.81795866627e-12, index=2.33701941988, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1835-1106/v2/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(17.5067871309,-2.10727986139,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.75855512547e-14, index=2.76743387939, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1835-1106/v2/iteration_v2/run.py
        roi.modify(which="2FGL J1837.3-0700c", free=True)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1835-1106/v2/iteration_v3/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(24.8159929656,-0.312339927726,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.28025066491e-13, index=1.9692153112, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1835-1106/v2/iteration_v4/run.py
        ps=PointSource(name='seed4', 
                       skydir=SkyDir(23.3224479892,-5.4671437957,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.03308486715e-14, index=2.51890044978, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1835-1106/v3/iteration_v1/run.py
        ps=PointSource(name='seed5', 
                       skydir=SkyDir(18.1974606968,0.506769151315,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=6.3706044662e-14, index=2.39308798367, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

    
    if name == 'PSRJ1838-0537':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1838-0537/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(25.1194896744,-0.118379731723,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=6.27534658701e-14, index=1.17492138767, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1838-0537/v2/iteration_v2/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(22.8116723172,-6.30791251945,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.75180658992e-14, index=2.67079648501, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1838-0537/v2/iteration_v3/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(31.1240732344,-5.37187572496,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.66430957658e-14, index=2.27046887729, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1838-0537/v2/iteration_v4/run.py
        roi.modify(which="2FGL J1833.6-1032", free=True)
        roi.modify(which="2FGL J1826.1-1256", free=True)



    if name == 'PSRJ1846+0919':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1846+0919/v1/iteration_v1/run.py
        model=PowerLaw(norm=4.81421e-12, index=2.27118, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(40.3531284371,0.68666217185,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1846+0919/v1/iteration_v3/run.py
        model=PowerLaw(norm=1.13635564381e-13, index=2.3528111204, e0=np.sqrt(1e2*1e5))
        model.set_e0(e0)
        model.set_default_limits(oomp_limits=True)
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(36.1037064322,0.122504899788,SkyDir.GALACTIC), 
                       model=model)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1846+0919/v2/iteration_v1/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(38.9783116077,1.19200846879,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=6.1493696327e-14, index=2.14461517853, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)





    if name == 'PSRJ1907+0602':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1907+0602/v1/iteration_v1/run.py
        model=PowerLaw(norm=2.94694e-12, index=2.23247, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(39.6911920096,1.37022766688,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1907+0602/v2/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(35.9855282617,0.289102268794,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.58261057897e-12, index=2.23253027573, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ1939+2134':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1939+2134/v1/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(61.1069794973,-0.020626624811,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.84339719761e-14, index=1.7707891594, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1939+2134/v1/iteration_v2/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(53.7047801952,2.54533707571,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.84142283976e-14, index=2.36294672893, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /afs/slac.stanford.edu/u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1939+2134/v2/iteration_v1/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(53.5284152227,-2.42803296756,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.13429147262e-14, index=2.36125432255, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)



    if name == 'PSRJ1952+3252':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1952+3252/v1/iteration_v1/run.py
        model=PowerLaw(norm=3.64908e-12, index=2.64963, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(74.0483151389,0.998233204602,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ1954+2836':

        # Analysis came from /afs/slac.stanford.edu/u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1954+2836/v1/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(61.0525240819,-0.0194155455509,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.40316698306e-14, index=1.88273395784, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ1959+2048':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1959+2048/v1/iteration_v1/run.py
        model=PowerLaw(norm=2.67284e-12, index=1.97096, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(61.3699136334,0.0363110623687,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ1959+2048/v1/iteration_v2/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(55.6789349846,-0.0259897845325,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.42676588842e-12, index=1.87448790915, e0=1000.0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ2017+0603':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2017+0603/v1/iteration_v1/run.py
        model=PowerLaw(norm=5.97897e-13, index=1.97357, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(44.2595421276,-12.7241517879,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ2021+3651':

        fix_gamma_cygni_region(roi)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2021+3651/v2/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(76.8827176381,4.49775554963,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.29108562331e-14, index=2.15844565249, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)



    if name == 'PSRJ2021+4026':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ2021+4026/v1/iteration_v1/run.py
        roi.modify(which="2FGL J2021.0+3651", free=True)

        # Note, this source is the (pulsar assocaited with the) Gamma-Cygni SNR, so no need
        # to correctly model the region by adding Gamma-Cygni as an extended SNR.

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2021+4026/v2/iteration_v1/run.py
        roi.modify(which="2FGL J2030.0+3640", free=True)


    if name == 'PSRJ2028+3332':

        fix_gamma_cygni_region(roi)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2030+3641/v1/iteration_v2/run.py
        roi.modify(which='2FGL J2032.2+4126', free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2028+3332/v1/iteration_v3/run.py
        roi.modify(which="2FGL J1953.0+3253", free=True)
        roi.modify(which="2FGL J1958.6+2845", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2028+3332/v1/iteration_v4/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(74.6338977671,-7.55426554766,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.01380042617e-14, index=2.34411651063, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2028+3332/v2/iteration_v1/run.py
        roi.modify(which="2FGL J2021.0+3651", free=True)



    if name == 'PSRJ2030+4415':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ2030+4415/v1/iteration_v1/run.py
        model=PowerLaw(norm=4.0005e-12, index=2.48727, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(80.7308713518,1.54773623442,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir) 
        roi.add_source(ps)

        # Analysis from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2030+4415/v2/iteration_v1/run.py
        fix_gamma_cygni_region(roi)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2030+3641/v1/iteration_v2/run.py
        roi.modify(which='2FGL J2032.2+4126', free=True)


    if name == 'PSRJ2032+4127':

        fix_gamma_cygni_region(roi)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2032+4127/v2/iteration_v1/run.py
        roi.modify(which="2FGL J2021.0+3651", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2032+4127/v2/iteration_v2/run.py
        roi.modify(which="2FGL J2030.0+3640", free=True)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2032+4127/v2/iteration_v3/run.py
        model=PowerLaw(norm=2.31436226763e-13, index=2.34156498732, e0=np.sqrt(1e2*1e5))
        model.set_e0(e0)
        PWNRegion.limit_powerlaw(model)
        roi.modify(which='PSRJ2032+4127', 
                   model=model,
                   keep_old_flux=False)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2032+4127/v3/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(76.2874030943,4.5808459079,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.41212028323e-14, index=2.23815362813, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ2030+3641':
        fix_gamma_cygni_region(roi)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2030+3641/v1/iteration_v2/run.py
        roi.modify(which="2FGL J2032.2+4126", free=True)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2030+3641/v2/iteration_v2/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(78.6887246488,3.21325198432,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.28859248803e-14, index=2.14552826137, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


        # Analysis came from /afs/slac.stanford.edu/u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2030+3641/v3/iteration_v2/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(71.2196186766,1.46626229414,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=4.25506524865e-14, index=2.13003898524, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ2043+2740':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2043+2740/v1/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(73.2360285753,-7.76412215207,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.79509818749e-14, index=1.77812764818, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2043+2740/v1/iteration_v2/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(75.0313377746,-7.59146248173,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.48611304736e-14, index=2.31665074171, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)



    if name == 'PSRJ2055+2539':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ2055+2539/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.47473e-12, index=2.28808, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(74.6188639662,-7.67739530141,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2055+2539/v2/iteration_v1/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(75.5236881054,-8.5837381889,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.20072761889e-14, index=2.42619077228, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    if name == 'PSRJ2111+4606':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ2111+4606/v1/iteration_v1/run.py
        model=PowerLaw(norm=7.72022e-13, index=1.82989, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(85.935283806,1.39345978435,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ2124-3358':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ2124-3358/v1/iteration_v1/run.py
        model=PowerLaw(norm=8.87418e-13, index=2.13046, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(7.80736074681,-41.4131256955,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)


    if name == 'PSRJ2229+6114':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2229+6114/v1/iteration_v1/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(105.636365811,2.96446003064,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.85239756878e-14, index=2.43288401889, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2229+6114/v1/iteration_v2/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(107.900135179,7.45675163517,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=2.04179263063e-14, index=2.34891447256, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

    if name == 'PSRJ2238+5903':
        

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2238+5903/v1/iteration_v2/run.py
        ps=PointSource(name='seed1', 
                       skydir=SkyDir(105.198974577,3.6272748858,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=4.06542997682e-14, index=2.39895770087, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2238+5903/v1/iteration_v3/run.py
        ps=PointSource(name='seed2', 
                       skydir=SkyDir(110.523146572,3.55971003637,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.23249581438e-14, index=1.99253978427, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2238+5903/v1/iteration_v4/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(109.206878285,-1.08948455424,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=3.92884766064e-14, index=1.58638784179, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)



    if name == 'PSRJ2240+5832':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ2240+5832/v1/iteration_v2/run.py
        model=PowerLaw(norm=2.91961e-13, index=1.41685, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(109.146031617,-1.05920960182,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ2240+5832/v1/iteration_v3/run.py
        model=PowerLaw(norm=1.82781e-12, index=2.48384, e0=1000, set_default_oomp_limits=True)
        skydir=SkyDir(105.605336985,2.8411205157,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2240+5832/v2/iteration_v1/run.py
        ps=PointSource(name='seed3', 
                       skydir=SkyDir(106.625787103,2.77669886738,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=5.1058917963e-14, index=1.86803437427, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2240+5832/v2/iteration_v2/run.py
        ps=PointSource(name='seed4', 
                       skydir=SkyDir(105.242233988,3.83994919054,SkyDir.GALACTIC), 
                       model=PowerLaw(norm=1.98311268884e-14, index=2.49685926985, e0=e0, set_default_oomp_limits=True))
        roi.add_source(ps)


    catalog = PWNRegion.get_catalog()
    names = catalog.get_names()    
    new_sources = [source for source in roi.get_sources() if source.name not in names and 'PSR' not in source.name]
    print 'new_sources = ',[i.name for i in new_sources]
    return new_sources


def get_cutoff_model(name):
    ec=None

    if name == 'PSRJ1112-6103':
        # parameters taken from 
        # $pwndata/spectral/v18/analysis_no_plots/PSRJ1112-6103/results_PSRJ1112-6103.yaml
        ec=PLSuperExpCutoff.from_gtlike(
            Cutoff=55005.75302330966, 
            Index1=-2.1146914874544533,
            Index2=1.0, 
            Prefactor=5.63695160040493e-13,
            Scale=3162.2776601683795,
            set_default_oomp_limits=True)

    elif name == 'PSRJ1119-6127':
        # Parameters from ???
        ec=PLSuperExpCutoff.from_gtlike(
            Cutoff= 999.999080269481, 
            Index1= -1.1150590055120246,
            Index2= 1.0, 
            Prefactor= 2.390605996204141e-11,
            Scale= 1000.0, 
            set_default_oomp_limits=True)
        ec.set_free('b',False)

    elif name == 'PSRJ1410-6132':
        # Parameters from $pwndata/spectral/v22/analysis/PSRJ1410-6132/results_PSRJ1410-6132_gtlike_point.yaml
        ec=PLSuperExpCutoff.from_gtlike(
            Cutoff=1000.0020944387121,
            Index1=-0.39389466758817093,
            Index2=1.0,
            Prefactor=2.3394118851977505e-11,
            Scale=1000.0,
            set_default_oomp_limits=True)
        ec.set_free('b',False)

    return ec

def get_gtlike_cutoff_model(name):
    ec = None
    if name == 'PSRJ0908-4913':
        # from $pwnpipeline/v34/analysis/PSRJ0908-4913/results_PSRJ0908-4913_gtlike_at_pulsar.yaml
        ec=PLSuperExpCutoff.from_gtlike(
                Cutoff= 272.8455226212762,
                Index1= -0.0019587564421516546,
                Index2= 1.0,
                Prefactor= 1.9920568832440028e-10,
                Scale= 1000.0,
                set_default_oomp_limits=True)
        ec.set_free('b',False)
    return ec



def get_override_localization(name):

    if name == 'PSRJ1648-4611':
        return dict(
            init_position=SkyDir(339.37417265790333, -1.2120735396287685,SkyDir.GALACTIC),
            method='MinuitLocalizer',
        )

    return None


def get_variability_time_cuts(name):
    """ Some pulsars have bad time intervals. Here, we cut out
        time ranges around the bad intervals. """

    if name == 'PSRJ0205+6449':

        def good_interval(tmin, tmax):
            # from $kerr_2pc_data/v1/J0205+6449/do_gtmktime.py

            if overlaps(tmin, tmax, 256179803, 260474522) or \
               overlaps(tmin, tmax, 328134373, 330369633):
                return False
            return True
        return good_interval

    if name == 'PSRJ1838-0537':
        def good_interval(tmin, tmax):
            # from $kerr_2pc_data/v1/J1838-0537/do_gtmktime.py
            if overlaps(tmin, tmax, 273456002, 297216002):
                return False
            return True
        return good_interval

    return None        

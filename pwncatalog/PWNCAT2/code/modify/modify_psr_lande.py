import os,sys
from os.path import expandvars
folder = os.path.dirname(__file__)
sys.path.append(folder)
import modify_psr_base

import numpy as np

from skymaps import SkyDir
from uw.like.pointspec_helpers import PointSource
from uw.like.Models import PowerLaw, SmoothBrokenPowerLaw, SumModel, FileFunction, LogParabola
from uw.like.SpatialModels import Disk
from uw.like.roi_extended import ExtendedSource

def modify_roi(name,roi):
    modify_psr_base.modify_roi(name,roi)


    if name == 'PSRJ0007+7303':
        print 'fixing starting value of %s' % name
        # In previous analysis, I found trouble converging for some hypothesis,
        # so start out with best spectral parameters

        # best fit parmaters taken from:
        # $pwndata/spectral/v8/analysis_no_plots/PSRJ0007+7303/results_PSRJ0007+7303.yaml
        modify_psr_base.set_flux_index(roi,name,5.637887384602554e-08,2.869750880323576)

    if name == 'PSRJ0102+4839

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0102+4839/v1/iteration_v1/run.py
        model=PowerLaw(norm=4.77276e-13, index=2.01965, e0=1000)
        skydir=SkyDir(127.789190256,-10.6871258101,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0102+4839/v1/iteration_v2/run.py
        model=PowerLaw(norm=2.6108e-13, index=1.77088, e0=1000)
        skydir=SkyDir(124.936171519,-17.8324907932,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0106+4855':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0106+4855/v1/iteration_v1/run.py
        model=PowerLaw(norm=3.2257e-13, index=1.79886, e0=1000)
        skydir=SkyDir(124.902581145,-17.8410812906,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0218+4232':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0218+4232/v1/iteration_v1/run.py
        model=PowerLaw(norm=7.41413e-13, index=2.16066, e0=1000)
        skydir=SkyDir(141.890006495,-20.0283413292,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0248+6021':

        # Values taken from $pwnpersonal/individual_sources/PSRJ0248+6021/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.89676e-12, index=2.54806, e0=1000)
        skydir=SkyDir(136.651028662,1.91638928353,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0248+6021/v2/iteration_v1/run.py
        model=PowerLaw(norm=1.39429e-12, index=2.39466, e0=1000)
        skydir=SkyDir(139.079106372,3.96339422846,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0248+6021/v2/iteration_v2/run.py
        roi.modify(which="2FGL J0218.7+6208c", free=True)


    if name == 'PSRJ0357+3205':
        # Values taken from $pwnpersonal/individual_sources/PSRJ0357+3205/v1/iteration_v1/run.py

        model=PowerLaw(norm=1.50764e-12, index=2.36031, e0=1000)
        skydir=SkyDir(160.336172309,-17.3616171342,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0534+2200':
        # (a) fix spectrum of crab

        # Parameters taken from arXiv:1112.1979v2
        # and $pwnpersonal/individual_sources/PSRJ0534+2200/v2/iteration_v1/run.py

        sync = PowerLaw(index=3.59)
        sync.set_flux(6.1e-7, emin=100, emax=np.inf) 
        ic = SmoothBrokenPowerLaw(index_1=1.48, index_2=2.19, e_break=13.9e3)
        ic.set_flux(1.1e-7, emin=100, emax=np.inf)

        sum_model = SumModel(sync, ic)

        filename=expandvars('$PWD/crab_spectrum.txt')
        sum_model.save_profile(filename, emin=10, emax=1e6)

        model = FileFunction(file=filename)
        roi.modify(which='PSRJ0534+2200', model=model)

        # (b) add nearby source

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0534+2200/v2/iteration_v2/run.py
        model=PowerLaw(norm=2.06176e-12, index=2.56593, e0=1000)
        skydir=SkyDir(183.728621429,-4.08423898725,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0631+1036':

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0631+1036/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.36144e-12, index=2.24104, e0=1000)
        skydir=SkyDir(201.96840164,2.63238059482,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0633+0632':

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0633+0632/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.87896e-12, index=2.52495, e0=1000)
        skydir=SkyDir(206.228771742,1.5374031115,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0633+0632/v1/iteration_v2/run.py
        model=PowerLaw(norm=1.48345e-12, index=2.20523, e0=1000)
        skydir=SkyDir(205.763876721,-2.72839852568,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0633+0632/v1/iteration_v3/run.py
        model=PowerLaw(norm=1.20463e-12, index=1.9803, e0=1000)
        skydir=SkyDir(207.059007704,-1.90816325068,SkyDir.GALACTIC)
        ps=PointSource(name="seed3", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0633+0632/v2/iteration_v1/run.py
        roi.modify(which="2FGL J0631.5+1035", free=True)

    if name == 'PSRJ0729-1448':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0729-1448/v1/iteration_v1/run.py
        model=PowerLaw(norm=2.11637e-12, index=2.33741, e0=1000)
        skydir=SkyDir(233.900470646,-0.220997218399,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)


    if name == 'PSRJ0734-1559':

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0734-1559/v1/iteration_v1/run.py
        model=PowerLaw(norm=2.39292e-12, index=2.36721, e0=1000)
        skydir=SkyDir(233.928276957,-0.176812544449,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0734-1559/v1/iteration_v2/run.py
        model=PowerLaw(norm=1.02789e-12, index=2.06358, e0=1000)
        skydir=SkyDir(231.291186104,-0.0769198428432,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0742-2822':
        # Parameters came from $pwnpersonal/individual_sources/PSRJ0742-2822/v1/iteration_v1/run.py
        model=PowerLaw(norm=3.53607e-13, index=1.80772, e0=1000)
        skydir=SkyDir(244.483009084,-4.72149826403,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0751+1807':

        # Parameters came from $pwnpersonal/individual_sources/PSRJ0751+1807/v1/iteration_v1/run.py
        roi.modify(which='PSRJ0751+1807',
                   model=PowerLaw(norm=4.48e-13, index=2.28, e0=1e3),
                   keep_old_flux=True)

    if name == 'PSRJ0835-4510':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ0835-4510/v1/iteration_v1/run.py
        model=PowerLaw(norm=3.38097e-12, index=2.41688, e0=1000)
        skydir=SkyDir(262.832249309,0.643797379224,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ0908-4913':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0908-4913/v1/iteration_v1/run.py
        roi.modify(which="2FGL J0835.3-4510", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0908-4913/v1/iteration_v2/run.py
        model=PowerLaw(norm=1.61329e-12, index=2.21098, e0=1000)
        skydir=SkyDir(271.258995834,0.149243337966,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0908-4913/v1/iteration_v4/run.py
        model=PowerLaw(norm=8.78234e-13, index=1.77965, e0=1000)
        skydir=SkyDir(266.592361248,-1.93883515163,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ0908-4913/v1/iteration_v5/run.py
        model=PowerLaw(norm=9.08555e-13, index=1.81663, e0=1000)
        skydir=SkyDir(267.884950765,-0.934447309326,SkyDir.GALACTIC)
        ps=PointSource(name="seed3", model=model, skydir=skydir)
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
                         model=PowerLaw(norm=3.8835219935993907e-12,index=2.2310422346640504))
        roi.add_source(ps1)

        # v10: Add new source 'seed2' that represents additional residual found from
        # $pwnpersonal/individual_sources/PSRJ1023-5746/v2/iteration_v1/run.py
        ps2 = PointSource(name='seed2',
                         skydir=SkyDir(284.5071255898265,0.9734675040757886,SkyDir.GALACTIC),
                         model=PowerLaw(norm=2.787037074673656e-12,index=2.2750149645582809))
        roi.add_source(ps2)

        # Parameters came from $pwnpersonal/individual_sources/PSRJ1023-5746/v3/v1/iteration_v1/run.py
        model=PowerLaw(norm=9.81327e-13, index=1.64754, e0=1000)
        skydir=SkyDir(285.184506369,-0.0773421350636,SkyDir.GALACTIC)
        ps=PointSource(name="seed3", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1023-5746/v4/iteration_v1/run.py
        roi.modify(which="2FGL J1048.2-5831", free=True)

    if name == 'PSRJ1016-5857':
        raise Exception("...")

    if name == 'PSRJ1019-5749':
        
        # Analysis came from $pwnpersonal/individual_sources/PSRJ1019-5749/v1/iteration_v2/run.py
        roi.modify(which='2FGL J1028.5-5819', free=True)
        roi.modify(which='2FGL J1036.4-5828c', free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1019-5749/v1/iteration_v2/run.py
        model=PowerLaw(norm=3.71803e-12, index=2.51986, e0=1000)
        skydir=SkyDir(285.580986429,0.56400926783,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1019-5749/v1/iteration_v3/run.py
        roi.modify(which="2FGL J1048.2-5831", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1019-5749/v1/iteration_v4/run.py
        model=PowerLaw(norm=2.83122e-12, index=2.29234, e0=1000)
        skydir=SkyDir(284.482071165,0.671568823511,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)



    if name == 'PSRJ1028-5819':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ1028-5819/v1/iteration_v1/run.py
        roi.modify(which='2FGL J1044.5-5737', free=True)
        roi.modify(which='2FGL J1048.2-5831', free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1028-5819/v1/iteration_v2/run.py
        model=PowerLaw(norm=3.23885e-12, index=2.14376, e0=1000)
        skydir=SkyDir(285.511479051,0.742991500068,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1028-5819/v2/iteration_v1/run.py
        model=PowerLaw(norm=3.35481e-12, index=2.11961, e0=1000)
        skydir=SkyDir(283.805447725,-0.715796302543,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1028-5819/v2/iteration_v2/run.py
        model=PowerLaw(norm=1.81777e-12, index=1.95643, e0=1000)
        skydir=SkyDir(287.091319865,-0.93052274267,SkyDir.GALACTIC)
        ps=PointSource(name="seed3", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ1044-5737':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ1044-5737/v1/iteration_v1/run.py
        roi.modify(which='2FGL J1023.5-5749c', free=True)
        roi.modify(which='2FGL J1022.7-5741', free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1044-5737/v1/iteration_v2/run.py
        roi.modify(which="2FGL J1028.5-5819", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1044-5737/v1/iteration_v3/run.py
        model=PowerLaw(norm=1.45355e-12, index=1.81839, e0=1000)
        skydir=SkyDir(285.230741326,0.0446637805384,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)




    if name == 'PSRJ1048-5832':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1048-5832/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1028.5-5819", free=True)


        # Analysis came from $pwnpersonal/individual_sources/PSRJ1048-5832/v1/iteration_v2/run.py
        model=PowerLaw(norm=2.62919e-12, index=2.3449, e0=1000)
        skydir=SkyDir(289.735306739,-1.00596563899,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ1357-6429'
        # Analysis came from $pwnpersonal/individual_sources/PSRJ1357-6429/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1418.7-6058", free=True)
        roi.modify(which="2FGL J1420.1-6047", free=True)

    if name == 'PSRJ1410-6132':
        
        # Avoid convergence failures. 
        # Parameters from $pwnpersonal/individual_sources/PSRJ1410-6132/v1/iteration_v1/ run.py
        roi.modify(which='PSRJ1410-6132',
                   model=PowerLaw(norm=4.98e-12, index=2.08, e0=1000),
                   keep_old_flux=False)

        roi.modify(which='2FGL J1405.5-6121',
                   model=LogParabola(norm=6.25e-12, index=2.15, beta=0.21, e_break=1.5e+03),
                   keep_old_flux=False)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1410-6132/v2/iteration_v1/run.py
        roi.modify(which="2FGL J1356.0-6436", free=True)

    if name == 'PSRJ1413-6205':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1413-6205/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1420.1-6047", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1413-6205/v1/iteration_v2/run.py
        roi.modify(which="2FGL J1356.0-6436", free=True)


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

    if name == 'PSRJ1429-5911':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1429-5911/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1509.6-5850", free=True)
        roi.modify(which="2FGL J1459.4-6054", free=True)
        roi.modify(which="2FGL J1413.4-6204", free=True)

    if name == 'PSRJ1446-4701':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1446-4701/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.0112e-12, index=2.33614, e0=1000)
        skydir=SkyDir(320.908389496,14.741711492,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ1509-5850':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1509-5850/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1459.4-6054", free=True)

    if name == 'PSRJ1513-5908':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ1513-5908/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1459.4-6054", free=True)

    if name == 'PSRJ1531-5610':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1531-5610/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1509.6-5850", free=True)

    if name == 'PSRJ1600-3053':
        # Don't keep seed from analysis $pwnpersonal/individual_sources/PSRJ1600-3053/v1/iteration_v1/run.py
        # because it is not significant enough
        pass

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
        model=PowerLaw(norm=4.67995e-12, index=2.11003, e0=1000)
        skydir=SkyDir(333.008696871,0.0306605245011,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ1648-4611':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1648-4611/v1/iteration_v2/run.py
        roi.modify(which="2FGL J1709.7-4429", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1648-4611/v1/iteration_v3/run.py
        model=PowerLaw(norm=1.98727e-12, index=2.44488, e0=1000)
        skydir=SkyDir(339.187684989,-4.31868997792,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ1658-5324':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ1658-5324/v1/iteration_v1/run.py
        model=PowerLaw(norm=7.25394e-13, index=1.9179, e0=1000)
        skydir=SkyDir(333.799799064,-8.62492903066,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1658-5324/v1/iteration_v2/run.py
        model=PowerLaw(norm=1.43796e-12, index=2.38295, e0=1000)
        skydir=SkyDir(336.992952017,-5.44100960768,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
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
                       e0=1000.0))

    if name == 'PSRJ1718-3825':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1718-3825/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.06204e-12, index=1.56099, e0=1000)
        skydir=SkyDir(347.584694432,-0.681857494514,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)


    if name == 'PSRJ1730-3350':

        roi.modify(which='2FGL J1737.2-3213',           
                   model=LogParabola(norm=1.17e-12, index=2.99, beta=0.571, e_break=2.16e+03),
                   keep_old_flux=False)

    if name == 'PSRJ1741-2054':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1741-2054/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1758.8-2402c", free=True)

    if name == 'PSRJ1744-1134':

        # Parameters taken from gtlike at_pulsar analysis in
        # $pwndata/spectral/v9/analysis_no_plots/PSRJ1744-1134/results_PSRJ1744-1134.yaml
        modify_psr_base.set_flux_index(roi,name,4.7112402016117437e-08,2.3441611339006334)

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
                                        index=2.1855137088271537))
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
                                        index=2.20))
        roi.add_source(ps)

    if name == 'PSRJ1747-4036':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1747-4036/v1/iteration_v1/run.py
        model=PowerLaw(norm=5.31456e-13, index=1.8748, e0=1000)
        skydir=SkyDir(350.765455165,-8.48679435559,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ1801-2451':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1801-2451/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1809.8-2332", free=True)

    if name == 'PSRJ1803-2149':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1803-2149/v1/iteration_v1/run.py
        roi.modify(which="2FGL J1809.8-2332", free=True)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1803-2149/v2/iteration_v1/run.py
        roi.modify(which="2FGL J1741.9-2054", free=True)

    if name == 'PSRJ1826-1256':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1826-1256/v1/iteration_v3/run.py
        roi.modify(which="2FGL J1833.6-1032", free=True)
        roi.modify(which="2FGL J1813.4-1246", free=True)

    if name == 'PSRJ1907+0602':

        # Analysis came from $pwnpersonal/individual_sources/PSRJ1907+0602/v1/iteration_v1/run.py
        model=PowerLaw(norm=2.94694e-12, index=2.23247, e0=1000)
        skydir=SkyDir(39.6911920096,1.37022766688,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ2021+4026':
        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2021+4026/v1/iteration_v1/run.py
        roi.modify(which="2FGL J2021.0+3651", free=True)

    if name == 'PSRJ2030+4415':

        # Analysis came from /u/gl/lande/work/fermi/pwncatalog/PWNCAT2/individual_sources/PSRJ2030+4415/v1/iteration_v1/run.py
        model=PowerLaw(norm=4.0005e-12, index=2.48727, e0=1000)
        skydir=SkyDir(80.7308713518,1.54773623442,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ2032+4127':

        """
        # In previous analysis 
        # $pwndata/spectral/v9/analysis_no_plots/PSRJ2032+4127/results_PSRJ2032+4127.yaml
        # I foudn that these 2 nearby sources (correlated with the Gamma Cygni SNR + Pulsar)
        # had very large residual when they were not expeiclty fit.
        # So here, always fit the spectra

        roi.modify(which='2FGL J2019.1+4040', free=True)
        roi.modify(which='2FGL J2021.5+4026', free=True)
        """

        # In previous analysis 
        # $pwndata/spectral/v10/analysis_no_plots/PSRJ2032+4127/results_PSRJ2032+4127.yaml
        # I found that just freeing the two sources near gamma 
        # cygni was not sufficient. A better solution
        # is to explicitly add in Gamma Cygni as an SNR


        # delete source associated with Gamma Cygni SNR
        roi.del_source(which='2FGL J2019.1+4040')

        # Free the pulsar component
        roi.modify(which='2FGL J2021.5+4026', free=True)

        # Add in Gamma Cygni SNR using best fit parmaeters
        # From extended soruce search paper
        model = PowerLaw(index=2.42)
        model.set_flux(2e-9,1e4,1e5)
        es=ExtendedSource(name='Gamma Cygni',
                          model=model,
                          spatial_model=Disk(l=78.24,b=2.20,sigma=0.63))
        roi.add_source(es)

    if name == 'PSRJ2021+4026':
        # Remove this nearby source which is associated with the
        # Gamma-Cygni SNR
        roi.del_source(which='2FGL J2019.1+4040')

    if name == 'PSRJ2055+2539':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ2055+2539/v1/iteration_v1/run.py
        model=PowerLaw(norm=1.47473e-12, index=2.28808, e0=1000)
        skydir=SkyDir(74.6188639662,-7.67739530141,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)


    if name == 'PSRJ2111+4606':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ2111+4606/v1/iteration_v1/run.py
        model=PowerLaw(norm=7.72022e-13, index=1.82989, e0=1000)
        skydir=SkyDir(85.935283806,1.39345978435,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ2124-3358':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ2124-3358/v1/iteration_v1/run.py
        model=PowerLaw(norm=8.87418e-13, index=2.13046, e0=1000)
        skydir=SkyDir(7.80736074681,-41.4131256955,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

    if name == 'PSRJ2240+5832':
        # Analysis came from $pwnpersonal/individual_sources/PSRJ2240+5832/v1/iteration_v2/run.py
        model=PowerLaw(norm=2.91961e-13, index=1.41685, e0=1000)
        skydir=SkyDir(109.146031617,-1.05920960182,SkyDir.GALACTIC)
        ps=PointSource(name="seed1", model=model, skydir=skydir)
        roi.add_source(ps)

        # Analysis came from $pwnpersonal/individual_sources/PSRJ2240+5832/v1/iteration_v3/run.py
        model=PowerLaw(norm=1.82781e-12, index=2.48384, e0=1000)
        skydir=SkyDir(105.605336985,2.8411205157,SkyDir.GALACTIC)
        ps=PointSource(name="seed2", model=model, skydir=skydir)
        roi.add_source(ps)


    
    new_sources = [source for source in roi.get_sources() if
                   '2FGL' not in source.name and 'PSRJ' not in source.name]
    return new_sources


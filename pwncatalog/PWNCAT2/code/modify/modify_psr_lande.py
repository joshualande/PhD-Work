import os,sys
folder = os.path.dirname(__file__)
sys.path.append(folder)
import modify_psr_base

from skymaps import SkyDir
from uw.like.pointspec_helpers import PointSource
from uw.like.Models import PowerLaw
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


    if name == 'PSRJ1023-5746':

        # In previous analysis 
        # $pwndata/spectral/v9/analysis_no_plots/PSRJ1023-5746/results_PSRJ1023-5746.yaml
        # I foudn that this source had large residual surrounding it. So always fit it
        roi.modify(which='2FGL J1044.5-5737', free=True)

        # Add new source 'seed1' that represents residual found in the TSmap at the top left
        # (in galactic coordinates) at (l,b)=(286.252,0.522)
        # The best fit parameters of this new source are taken from
        # $pwnpersonal/individual_sources/PSRJ1023-5746/v1/iteration_v1/run.py
        ps1 = PointSource(name='seed1',
                         skydir=SkyDir(286.2517892658979,0.5217112872908655,SkyDir.GALACTIC),
                         model=PowerLaw(norm=3.8835219935993907e-12,index=2.2310422346640504))
        roi.add_source(ps1)

        # Add new source 'seed2' that represents additional residual found from
        # $pwnpersonal/individual_sources/PSRJ1023-5746/v2/iteration_v1/run.py
        ps2 = PointSource(name='seed2',
                         skydir=SkyDir(284.5071255898265,0.9734675040757886,SkyDir.GALACTIC),
                         model=PowerLaw(norm=2.787037074673656e-12,index=2.2750149645582809))
        roi.add_source(ps2)
        

    if name == 'PSRJ1420-6048':
        print 'fixing starting value of %s' % name
        # In previous analysis, I found trouble converging for some hypothesis,
        # so start out with best spectral parameters

        # best fit parmaters taken from:
        # $pwndata/spectral/v8/analysis_no_plots/PSRJ1420-6048/results_PSRJ1420-6048.yaml
        modify_psr_base.set_flux_index(roi,name,1.4239401328058901e-08,1.8751316333602417)

    if name == 'PSRJ1620-4927':
        print 'fixing starting value of %s' % name
        # In previous analysis, I found trouble converging for some hypothesis,
        # so start out with best spectral parameters

        # best fit parmaters taken from:
        # $pwndata/spectral/v8/analysis_no_plots/PSRJ1620-4927/results_PSRJ1620-4927.yaml
        modify_psr_base.set_flux_index(roi,name,4.605558542777753e-08,2.0941239204631703)

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



import os,sys
folder = os.path.dirname(__file__)
sys.path.append(folder)
import modify_psr_base

def modify_roi(name,roi):
    modify_psr_base.modify_roi(name,roi)

    if name == 'PSRJ0007+7303':
        print 'fixing starting value of %s' % name
        # In previous analysis, I found trouble converging for some hypothesis,
        # so start out with best spectral parameters

        # best fit parmaters taken from:
        # $pwndata/spectral/v8/analysis_no_plots/PSRJ0007+7303/results_PSRJ0007+7303.yaml
        modify_psr_base.set_flux_index(roi,name,5.637887384602554e-08,2.869750880323576)


    if name == 'PSRJ1023-5746'

        # In previous analysis 
        # $pwndata/spectral/v9/analysis_no_plots/PSRJ1023-5746/log_PSRJ1023-5746.txt
        # I foudn that this source had large residual surrounding it. So always fit it
        roi.modify(which='2FGL J1044.5-5737', free=True)

        # Add new source 'seed' that represents residual found in the TSmap at the top left
        # (in galactic coordinates) at (l,b)=(286.252,0.522)
        # The best fit parameters of this new source are taken from
        # $pwnpersonal/individual_sources/PSRJ1023-5746/v1/iteration_v1/run.py
        ps = PointSource(name='seed',
                         skydir=SkyDir(286.2517892658979,0.5217112872908655,SkyDir.GALACTIC),
                         model=PowerLaw(norm=3.8835219935993907e-12,index=2.2310422346640504))
        roi.add_source(ps)
        

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

    if name == 'PSRJ2032+4127':

        # In prvious analysis 
        # $pwndata/spectral/v9/analysis_no_plots/PSRJ2032+4127/log_PSRJ2032+4127.txt
        # I foudn that these 2 nearby sources (correlated with the Gamma Cygni SNR + Pulsar)
        # had very large residual when they were not expeiclty fit.
        # So here, always fit the spectra

        roi.modify(which='2FGL J2019.1+4040', free=True)
        roi.modify(which='2FGL J2021.5+4026', free=True)



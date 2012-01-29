import os,sys
folder = os.path.dirname(__file__)
sys.path.append(folder)
import modify_psr_base

def modify_roi(name,roi):
    modify_psr_base.modify_roi(name,roi)

    if name == 'PSRJ0007+7303':
        print 'fixing starting value of %s' % name
        # best fit parmaters taken from:
        # $pwndata/spectral/v8/analysis_no_plots/PSRJ0007+7303/results_PSRJ0007+7303.yaml
        modify_psr_base.set_flux_index(roi,name,5.637887384602554e-08,2.869750880323576)

    if name == 'PSRJ1420-6048':
        print 'fixing starting value of %s' % name
        # best fit parmaters taken from:
        # $pwndata/spectral/v8/analysis_no_plots/PSRJ1420-6048/results_PSRJ1420-6048.yaml
        modify_psr_base.set_flux_index(roi,name,1.4239401328058901e-08,1.8751316333602417)

    if name == 'PSRJ1620-4927':
        print 'fixing starting value of %s' % name
        # best fit parmaters taken from:
        # $pwndata/spectral/v8/analysis_no_plots/PSRJ1620-4927/results_PSRJ1620-4927.yaml
        modify_psr_base.set_flux_index(roi,name,4.605558542777753e-08,2.0941239204631703)

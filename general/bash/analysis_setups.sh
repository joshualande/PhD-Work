

function setup_extended_catalog {
    export PATH=~/svn/lande/trunk/extended_catalog/code/:~/svn/lande/trunk/pointlike/:$PATH
    export PYTHONPATH=~/svn/lande/trunk/extended_catalog/code/:$PYTHONPATH

    export w44simdata=$nfs/extended_catalog/monte_carlo/w44simdata
    export w44simcode=/u/gl/lande/svn/lande/trunk/extended_catalog/monte_carlo/w44sim/code
    export w44simplots=/u/gl/lande/svn/lande/trunk/extended_catalog/monte_carlo/w44sim/plots

    export tsext_plane_data=$nfs/extended_catalog/monte_carlo/tsext/plane
    export tsext_plane_code=/u/gl/lande/svn/lande/trunk/extended_catalog/monte_carlo/tsext/plane/code
    export tsext_plane_plots=/u/gl/lande/svn/lande/trunk/extended_catalog/monte_carlo/tsext/plane/plots

}

function setup_snr_low_energy {
    export snr_low_energy_code=/u/gl/lande/svn/lande/trunk/fermi/monte_carlo/snr_low_energy/code
    export snr_low_energy_plots=/u/gl/lande/svn/lande/trunk/fermi/monte_carlo/snr_low_energy/plots
    export snr_low_energy_data=$nfs/fermi/snr_low_energy
}

function setup_mc_testing {
    export fitdiffdata=$FERMI/monte_carlo/test_mapcube_cutting/fitdiff
    export fitdiffcode=/u/gl/lande/svn/lande/trunk/fermi/monte_carlo/test_mapcube_cutting/fitdiff/code
    export fitdiffplots=/u/gl/lande/svn/lande/trunk/fermi/monte_carlo/test_mapcube_cutting/fitdiff/plots

    export simsrccode=$svn/fermi/monte_carlo/simsrc/code
    export simsrcplots=$svn/fermi/monte_carlo/simsrc/plots
    export simsrcdata=$FERMI/monte_carlo/simsrc
}


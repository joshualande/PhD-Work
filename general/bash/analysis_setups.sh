

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

function setup_snrlim {
    export snrlimcode=$svn/fermi/snrlim/code
    export snrlimfits=$fermi/snrlim/fits
    export snrlimdata=$fermi/snrlim/data/aug_13_2012

    export superfile=$HOME/svn/snrcat1/superfile/
}

function setup_radiopsrs {
    export radiopsrsfits=$fermi/radiopsrs/fits
    export radiopsrsdata=$fermi/radiopsrs/data
}

function setup_multiwavelength {
    export multiwavelength=$svn/fermi/multiwavelength/
}

function setup_pysed {
    export PYTHONPATH=~/svn/lande/trunk/:$PYTHONPATH
    export sed=~/svn/lande/trunk/pysed
}

function setup_snrsim {
    export snr_sim_code=$svn/fermi/monte_carlo/snrsim/code
    export snr_sim_sims=$FERMI/monte_carlo/snrsim/sims
    export snr_sim_fits=$FERMI/monte_carlo/snrsim/fits
}


function dm_satellite_setup {
    export SHERIDAN=~szalewsk
}


function setup_tevcat {
    export tevcat_paper=$svn/fermi/tevcat/paper
}



function setup_pwncat {
    export help_others=$HOME/work/fermi/help_others
    export alice=~allafort/ki05/pwncatalog
    export marianne=/nfs/farm/g/glast/u54/lemoine/PWNCat

    export pwncode=$svn/fermi/pwn/pwncat2/pipeline
    export pwnclassify=$svn/fermi/pwn/pwncat2/classify

    export pwndata=$svn/fermi/pwn/pwncat2/data
    export pwnmodify=$svn/fermi/pwn/pwncat2/modify
    export pwnpipeline=$nfs/fermi/pwn/pwncat2/pipeline

    export pwncat2_off_peak_results=$nfs/fermi/pwn/pwncat2/off_peak/off_peak_bb/pwncat2
    export pwncat2_off_peak_code=$svn/fermi/pwn/pwncat2/off_peak/code
    export pwncat2_off_peak_plots=$svn/fermi/pwn/pwncat2/off_peak/plots

    export pwncat2_spectral_plots=$svn/fermi/pwn/pwncat2/plots
    export pwncat2_spectral_website=$svn/fermi/pwn/pwncat2/website
    export pwncat2_spectral_tables=$svn/fermi/pwn/pwncat2/tables

    export pwnpaper=~/svn/lande/trunk/pwncatalog/PWNCAT2/paper
    export pwnpersonal=/u/gl/lande/work/fermi/pwncatalog/PWNCAT2
    export pwnmc=~/svn/lande/trunk/pwncatalog/PWNCAT2/mc

    export tevdata=$nfs/pwncatalog/PWNCAT2/analyze_tev

    export ozlem_2pc_data=/nfs/farm/g/glast/u55/pulsar/2ndPulsarcatalog/dataset/SpectAn
    export kerr_2pc_data=$ki03/fermi/2pc/data/
    export pulsar_group=/afs/slac/g/glast/groups/pulsar

    # These are depricated.
    export KERRPSR=$nfs/pulsar
    export OZLEMPSR=$ozlem_2pc_data 

    export PYTHONPATH=$pwncode/lande/publication_plots/plot_helper:$PYTHONPATH
    export PYTHONPATH=$pwncode/lande/tables:$PYTHONPATH
    export PYTHONPATH=$pwncode/lande/off_peak:$PYTHONPATH

    export extuldata=$pwndata/monte_carlo/extul
    export extulcode=$pwnmc/extul
    export extulplots=$pwnplots/extul

    export PYTHONPATH=$PYTHONPATH:$HOME/svn/lande/trunk/pwncatalog/PWNCAT2/code

    export lat2pc=/u/gl/lande/svn/lat2pc/trunk

}

function CandA_paper_draft {
    # Eric told me to add this to modify the C&A paper paper
    export CVSROOT=/nfs/slac/g/glast/ground/paper_drafts
    #cvs co ScienceGroups/CandA/Pass7Validation

    #The paper is in this folder: /u/gl/lande/cvs/ScienceGroups/CandA/Pass7Validation

    # Add text here on bad psf vs high level science
    # /u/gl/lande/cvs/ScienceGroups/CandA/Pass7Validation/pointSpreadFunction/psfHighLevel.tex

    # Add text here on
    # 10 year vs 2 year sensitivity: to ~/cvs/ScienceGroups/CandA/Pass7Validation/sciencePerformance/perf_spatialExtent.tex

}

function snrcat1setup {
    GREENCAT=$nfs/green_catalog/v1
    PYTHONPATH=/u/gl/lande/svn/lande/trunk/green_catalog/v1:$PYTHONPATH

    # collect here things specific to green catalog analysis
    export SNRTEMPLATES=/afs/slac/g/glast/users/jhewitt/snrcat1_fits

    export fits=/afs/slac/g/glast/groups/pulsar/snrcat1/fits
    export superfile=~/svn/snrcat1/superfile
    export PYTHONPATH=~/svn/snrcat1/code:$PYTHONPATH
}


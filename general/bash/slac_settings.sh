

function fixscreen {
    # sometimes my AFS tolken expires.
    # something, something. I don't really understand,
    # but running these commands fixes it.
    kinit
    /usr/bin/aklog
}


function _kipac_base {
    export KIPACSOFT=/afs/slac/g/ki/software
}

function pythonkipac {
    _kipac_base 
    #export PATH=$KIPACSOFT/python/2.6.2/amd64_linux26/bin:$PATH
    export PATH=/afs/slac/g/ki/software/python/2.5.5/amd64_rhel50/bin/:$PATH
    export PYTHONPATH=/afs/slac/g/ki/software/python/2.5.5/amd64_rhel50/lib/python2.5/:$PYTHONPATH
}

function ds9kipac {
    _kipac_base

    export PATH=$KIPACSOFT/ds9/6.1/amd64_linux26:$PATH

    export setup="${setup} ds9"
}

function fvkipac {
    _kipac_base

    export HEADAS=`echo $KIPACSOFT/heasoft/6.9/$(sys)/heasoft/*-linux-gnu-libc2.3.4`
    source $HEADAS/headas-init.sh
    export PATH=$HEADAS/bin/:$PATH
    export setup="${setup} fv"
}

function texlivekipac {
    _kipac_base

    # setup local tex build
    #export PATH=/u/gl/lande/texlive/2010/bin/x86_64-linux:$PATH
    export PATH=$KIPACSOFT/texlive/amd64_rhel60/amd64_rhel60/bin/x86_64-linux/:$PATH
    export KIPACSOFT=/afs/slac/g/ki/software
    export setup="${setup} texlive"
}

function kipacsetup {
    # setup all the kipac software
    fvkipac
    ds9kipac
    texlivekipac

    export setup="${setup} kipac"
}


function fix_matplotlib {
    # This says to use file .matplotlib/matplotlibrc for my configuration
    export MATPLOTLIBRC=~/.matplotlib
    # whereas this says to use as a temp folder random scratch space.
    export MPLCONFIGDIR=/scratch
}


# get functions for science tools
SOURCE="${BASH_SOURCE[0]}"
BASH_DIR="$( dirname "$SOURCE" )"
source $BASH_DIR/science_tools.sh


function stockscons {
#    _stockscons 09-27-01 Optimized
#    _stockscons HEAD-1-972 Debug
#    _stockscons 09-28-00 Optimized
#    _stockscons HEAD-1-981 Debug

    # This version has my variability bug fixed in skymaps
    #_stockscons HEAD-1-985 Debug
    #_stockscons HEAD-1-980 Debug
    
    #_stockscons 09-29-00 Optimized
    _stockscons 09-30-01 Optimized


    # Get custom irfs
    #export CUSTOM_IRF_DIR=$FERMI/irfs
    #export CUSTOM_IRF_NAMES=P7SOURCE_V4PSF,P7SOURCE_V4


    # get my version of ipython        
    #export PATH=~/bin:$PATH
}

function testsconcs {
    # for testing stuff
    _stockscons 09-27-01 Optimized
}

function tempscons {
    _stockscons 09-28-00 Optimized
    export head=/u/gl/lande/head
    export PYTHONPATH=$head:$PYTHONPATH
    export PYTHONPATH=/u/gl/lande/lib/python2.7/site-packages:$PYTHONPATH
    export setup=`echo $setup | sed 's/stockscons/tempscons/g'`
}

function headscons {
    # stock version of science tools with head version of pointlike on top of it.
    stockscons 

    export head=/u/gl/lande/head
    # point at the most up to teh cvs version of all the pointlike code

    # To get the code:
    #   cvs co -d uw ScienceTools-scons/pointlike/python/uw
    export PYTHONPATH=$head:$PYTHONPATH

    # I got pyLikelihood with the command:
    #   cvs co -d pyLikelihood ScienceTools-scons/pyLikelihood/python
    export PYTHONPATH=/u/gl/lande/head/pyLikelihood/:$PYTHONPATH
    #_stockscons HEAD-1-1003 Debug

    export PYTHONPATH=/u/gl/lande/lib/python2.7/site-packages:$PYTHONPATH

    export python=$head/uw/like

    export setup=`echo $setup | sed 's/stockscons/headscons/g'`
}


function tempscons {
    stockscons 
    export temp=/u/gl/lande/temp
    export PYTHONPATH=$temp:$PYTHONPATH
    export PYTHONPATH=/u/gl/lande/lib/python2.7/site-packages:$PYTHONPATH
    export python=$temp/uw/like
    export setup=`echo $setup | sed 's/stockscons/tempscons/g'`
}


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



function setup_svn {
    export svn=/u/gl/lande/svn/lande/trunk
}

function setup_mc_testing {
    export fitdiffdata=$FERMI/monte_carlo/test_mapcube_cutting/fitdiff
    export fitdiffcode=/u/gl/lande/svn/lande/trunk/fermi/monte_carlo/test_mapcube_cutting/fitdiff/code
    export fitdiffplots=/u/gl/lande/svn/lande/trunk/fermi/monte_carlo/test_mapcube_cutting/fitdiff/plots

    export simsrccode=$svn/fermi/monte_carlo/simsrc/code
    export simsrcplots=$svn/fermi/monte_carlo/simsrc/plots
    export simsrcdata=$FERMI/monte_carlo/simsrc
}


function setup_personal_code {
    export PYTHONPATH=~/svn/lande/trunk/code/:$PYTHONPATH
}

function devscons {
    # path of scons code
    set_bldtype
    export PATH=$PATH:/afs/slac/g/glast/applications/SCons/1.3.0/bin

    export GLAST_EXT=/afs/slac/g/glast/ground/GLAST_EXT/${BLDTYPE}

    export INST_DIR=/u/gl/lande/dev/ScienceTools-scons
    source ${INST_DIR}/bin/${BLDTYPE}-Optimized/_setup.sh

    # point at the most up to the cvs version of all the pointlike code
    export PYTHONPATH=/u/gl/lande/dev/ScienceTools-scons/pointlike/python:$PYTHONPATH

    export python=$INST_DIR/pointlike/python/uw/like

    export CALDB=${INST_DIR}/irfs/caldb/CALDB

    export PYTHONPATH=/u/gl/lande/lib/python2.7/site-packages:$PYTHONPATH
    export setup="${setup} sconsdev"
}


function build {
    scons --with-GLAST-EXT=${GLAST_EXT} --compile-opt $@
}

function buildpointlike {
    build pointlike 
    build skymaps 
    build setup
}
function buildgtlike {
    build Likelihood
    build pyLikelihood

    # This is necessary for the facilities code to pass the irfs to gtlike
    build caldb

    # To get GtApp
    build sane facilities

    # evtbin=gtbin dataSubselector=gtbin
    build evtbin dataSubselector

    build setup
}

function setup_fermi_code {
    export FERMI=$nfs/fermi
    export fermi=$FERMI
    export FERMILANDE=$FERMI # in case I have to share with others
    export diffuse=$fermi/diffuse
    export catalogs=$fermi/catalogs
    export extended_archives=$fermi/extended_archives
    export globalcat=/afs/slac/g/glast/groups/catalog
}


function setup_general_slac_alias {

    # places at SLAC
    export u31="/nfs/farm/g/glast/u31/lande" # Josh's u31 home
    export afs=/afs/slac/g/glast/users/lande
    export markus=/u/gl/markusa/disk/glast_data/gammas
    export sass="/afs/slac/www/slac/sass"

    export nfs="/nfs/slac/g/ki/ki03/lande"
    export ki03=$nfs

    export yajie=~yuanyj

    alias f2f=fixed2fixed

    function vimdump {
        if [[ ! $string =~ kipac ]]; 
        then
            kipacsetup 
        fi
        fdump $1 STDOUT - - page=no pagewidth=256 | vim -
    }
}

export PYTHONPATH=$HOME/bin:$HOME/python:$PYTHONPATH

function mathematica_setup {
    PATH=$PATH:/afs/slac.stanford.edu/g/ki/software/Wolfram/Mathematica/8.0/Executables
}

export PATH=~/bin:~/svn/lande/trunk/general/bin/:$PATH

# local stuff
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/lib


function setup_lsf {
    # For the program lsf program.
    export PATH="$PATH:/usr/local/bin" 
    export PATH="$PATH:/usr/afsws/bin"

    function bj { 
        run=`bjobs -r $@ 2> /dev/null | awk '$1!="JOBID"{print $0}' | wc -l`
        jobs=`bjobs $@ 2> /dev/null | awk '$1!="JOBID"{print $0}' | wc -l`
        echo $run/$jobs
    }

    # Nice function submit jobs to xxl queue
    for queue in long xlong xxl kipac-ibq; do
        eval "function $queue { bsub -q $queue -oo log.txt python \$PWD/\$1; }"
    done
    
    #function xxl { bsub -q xxl -oo log.txt python $PWD/$1 }

    # Alias to show just the queues I like
    alias bq="bqueues short medium long xlong xxl kipac-ibq express"

}


function setup_science_tools_dev {
    export CVSROOT=/nfs/slac/g/glast/ground/cvs

    # Get the program STAG
    export PATH="/afs/slac.stanford.edu/g/glast/applications/stag/i386_rhel40/:$PATH"
}

function tagCollector {
    # Tag the science tools
    echo python tagCollector.py ScienceTools --new=HEAD -r True
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


function temposetup {
    # Taken from Romain, who got it from Marie-Helene.
    # For some reason, tempo2 can only be run in
    # the cshell on rhel5-32 machines.
    export TEMPO2=/afs/slac/g/glast/users/guillemot/tempo2/tempo2-1.11/T2runtime
    export PATH=/afs/slac/g/glast/users/guillemot/tempo2/tempo2-1.11:${PATH}
    export ephem='/afs/slac/g/glast/groups/pulsar/ephemeris'

    # exmaple usage: 
    #   http://fermi.gsfc.nasa.gov/ssc/data/analysis/user/Fermi_plug_doc.pdf
    #   tempo2 -gr fermi -ft1 FT1.fits -ft2 FT2.fits -f pulsar.par -grdev toto.ps/cps -phase -col PULSE_PHASE

    export setup="${setup} tempo2"
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



function setup_pysed {
    export PYTHONPATH=~/svn/lande/trunk/:$PYTHONPATH
    export sed=~/svn/lande/trunk/pysed
}

function setup_snrsim {
    export snr_sim_code=$svn/fermi/monte_carlo/snrsim/code
    export snr_sim_sims=$FERMI/monte_carlo/snrsim/sims
    export snr_sim_fits=$FERMI/monte_carlo/snrsim/fits
}
function epd_setup {
    export PATH=/u/gl/lande/software/epd/bin:$PATH
    export setup="${setup} epd"
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


function setup_defaults_slac {
    setup_general_slac_alias
    setup_fermi_code
    setup_svn
    setup_mc_testing
    setup_personal_code
    setup_lsf
    fix_matplotlib
    setup_extended_catalog
    setup_pwncat
    setup_tevcat
    setup_pysed
    setup_snrsim
    setup_science_tools_dev 
    setup_snr_low_energy
    setup_snrlim
    setup_radiopsrs
    setup_multiwavelength
}
setup_defaults_slac

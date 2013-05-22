function source_common_setups {
    # Source common default programs.
    SOURCE="${BASH_SOURCE[0]}"
    BASH_DIR="$( dirname "$SOURCE" )"
    source $BASH_DIR/science_tools.sh
    source $BASH_DIR/kipac_setup.sh
    source $BASH_DIR/analysis_setups.sh
}
source_common_setups


function fixscreen {
    # sometimes my AFS tolken expires.
    # something, something. I don't really understand,
    # but running these commands fixes it.
    kinit
    /usr/bin/aklog
}

function fix_matplotlib {
    # This says to use file .matplotlib/matplotlibrc for my configuration
    export MATPLOTLIBRC=~/.matplotlib
    # whereas this says to use as a temp folder random scratch space.
    export MPLCONFIGDIR=/scratch
}



function tempsetup1 {
    _stockscons 09-31-01 Optimized
    export PYTHONPATH=/u/gl/lande/lib/python2.7/site-packages:$PYTHONPATH
    export PATH=~/bin:$PATH
    export setup=`echo $setup | sed 's/stockscons/tempsetup1/g'`
}

function tempsetup2 {
    _stockscons 09-30-00 Optimized
    export PYTHONPATH=/u/gl/lande/lib/python2.7/site-packages:$PYTHONPATH
    export PATH=~/bin:$PATH
    export setup=`echo $setup | sed 's/stockscons/tempsetup2/g'`
}

function tempsetup3 {
    _stockscons 09-30-01 Optimized
    export PYTHONPATH=/u/gl/lande/lib/python2.7/site-packages:$PYTHONPATH
    export PATH=~/bin:$PATH
    export setup=`echo $setup | sed 's/stockscons/tempsetup3/g'`
}

function tempsetup4 {
    _stockscons 09-31-00 Optimized
    export PYTHONPATH=/u/gl/lande/lib/python2.7/site-packages:$PYTHONPATH
    export PATH=~/bin:$PATH
    export setup=`echo $setup | sed 's/stockscons/tempsetup4/g'`
}

function stockscons {
    #_stockscons 09-30-01 Optimized
    _stockscons 09-31-01 Optimized
    export PATH=~/bin:$PATH
}

function testsconcs {
    # for testing stuff
    _stockscons 09-27-01 Optimized
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

function pythonkipac {
    #_pythonkipac 2.5.5
    _pythonkipac 2.7.3 # Note, Checking for Chris - JL Dec 6, 2012
}

function devscons {
    # path of scons code
    set_bldtype
    #export PATH=$PATH:/afs/slac/g/glast/applications/SCons/1.3.0/bin
    export PATH=$PATH:/afs/slac/g/glast/applications/SCons/2.1.0/bin

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



function setup_svn {
    export svn=/u/gl/lande/svn/lande/trunk
}


function setup_personal_code {
    export PYTHONPATH=~/svn/lande/trunk/code/:$PYTHONPATH
}



function build {
    scons --with-GLAST-EXT=${GLAST_EXT} --compile-opt $@
}

function buildskymaps {
    build astro
    build skymaps 
    build setup
}

function buildpointlike {
    # for some reason, building pointlike will not build
    # the skymaps swig interface so you have to explicitly build it first.
    
    # For some reason, I get an error building skymaps first, so
    # first I have to build astro.
    build astro 
    build skymaps 
    build pointlike 
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


function setup_general_slac_alias {

    # places at SLAC
    export u31="/nfs/farm/g/glast/u31/lande" # Josh's u31 home
    export afs=/afs/slac/g/glast/users/lande
    export markus=/u/gl/markusa/disk/glast_data/gammas
    export sass="/afs/slac/www/slac/sass"

    export nfs="/nfs/slac/g/ki/ki03/lande"
    export ki03=$nfs

    export yajie=~yuanyj

    export FERMI=$nfs/fermi
    export fermi=$FERMI
    export FERMILANDE=$FERMI # in case I have to share with others
    export diffuse=$fermi/diffuse
    export catalogs=$fermi/catalogs
    export extended_archives=$fermi/extended_archives
    export globalcat=/afs/slac/g/glast/groups/catalog

    export ipython=$svn/ipython
}



export MY_BIN=$HOME/bin

export PYTHONPATH=$MY_BIN:$HOME/python:$PYTHONPATH


export PATH=$MY_BIN:~/svn/lande/trunk/general/bin/:$PATH

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


function setup_science_tools_development {
    export CVSROOT=/nfs/slac/g/glast/ground/cvs

    # Get the program STAG
    export PATH="/afs/slac.stanford.edu/g/glast/applications/stag/i386_rhel40/:$PATH"
}

function tagCollector {
    # Tag the science tools
    echo python tagCollector.py ScienceTools --new=HEAD -r True
}

function epd_setup {
    export PATH=/u/gl/lande/epd/bin:$PATH

    setup_personal_code

    export setup="${setup} epd_setup"
}

function __launch_ipython_notebook {

    ip=`echo $SSH_CONNECTION | awk '{print $3}'`
    port=$(( $RANDOM%1000+9000 ))
    echo "https://$ip:$port"
    ipython notebook --profile=nbserver --port=$port --ip=$ip
}

function _launch_ipython_notebook {
    cd $ipython
    __launch_ipython_notebook
}

function launch_ipython_notebook {
    epd_setup
    _launch_ipython_notebook
}

function setup_defaults_slac {
    setup_general_slac_alias
    setup_svn
    setup_personal_code
    setup_lsf
    fix_matplotlib
    setup_science_tools_development 
}
setup_defaults_slac

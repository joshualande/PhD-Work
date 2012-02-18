

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
    export MATPLOTLIBRC=~/.matplotlib/
    # whereas this says to use as a temp folder random scratch space.
    export MPLCONFIGDIR=/scratch/
}


function set_bldtype {
    # Pick the $BILDTYPE based upon which version of red hat current computer is
    if [[ `cat /etc/redhat-release` =~ "release 5" ]]; then
        if [[ `uname -m` == i686 ]]; then
            export BLDTYPE=redhat5-i686-32bit-gcc41
        elif [[ `uname -m` == 'x86_64' ]]; then
            export BLDTYPE=redhat5-x86_64-64bit-gcc41
        else
            echo 'ERROR: UNABLE TO DETERMINE COMPUTER TYPE'
        fi

    elif [[ `cat /etc/redhat-release` =~ "release 6" ]]; then
        if [[ `uname -m` == 'x86_64' ]]; then
            export BLDTYPE=redhat6-x86_64-64bit-gcc44
        else
            echo 'ERROR: UNABLE TO DETERMINE COMPUTER TYPE'
        fi

    else
        echo 'ERROR: UNABLE TO DETERMINE COMPUTER TYPE'
    fi
}


function stockscons {
    export SCTOOLS=09-26-02
    set_bldtype
    export GLAST_EXT=/afs/slac/g/glast/ground/GLAST_EXT/${BLDTYPE}
    export BUILDS=/nfs/farm/g/glast/u35/ReleaseManagerBuild
    export INST_DIR=${BUILDS}/${BLDTYPE}/Optimized/ScienceTools/$SCTOOLS
    source ${INST_DIR}/bin/${BLDTYPE}-Optimized/_setup.sh

    #export PATH=$GLAST_EXT/python/2.7.1/gcc41/bin:$PATH
    #export PATH=$GLAST_EXT/python/2.6.5/gcc41/bin:$PATH

    # Get custom irfs
    export CUSTOM_IRF_DIR=$FERMI/irfs
    export CUSTOM_IRF_NAMES=P7SOURCE_V4PSF,P7SOURCE_V6,P7SOURCE_V4

    fix_matplotlib

    export setup="${setup} stockscons"
}

function headscons {
    # stock version of science tools with head version of pointlike on top of it.
    stockscons 

    export head=/u/gl/lande/head/
    # point at the most up to teh cvs version of all the pointlike code

    # To get the code:
    #   cvs co -d uw ScienceTools-scons/pointlike/python/uw
    export PYTHONPATH=$head:$PYTHONPATH

    # Temporarily, get pyLikelihood 
    #   cvs co -d pyLikelihood ScienceTools-scons/pyLikelihood/python
    export PYTHONPATH=/u/gl/lande/head/pyLikelihood/:$PYTHONPATH



    export PATH=~/svn/lande/trunk/extended_catalog/code/:~/svn/lande/trunk/pointlike/:$PATH
    export PYTHONPATH=~/svn/lande/trunk/extended_catalog/code/:~/svn/lande/trunk/pointlike/:$PYTHONPATH

    export PYTHONPATH=/u/gl/lande/lib/python2.7/site-packages:$PYTHONPATH

    export python=$head/uw/like

    export setup=`echo $setup | sed 's/stockscons/headscons/g'`
}

function headscons26 {
    # same as headscons but uses python 2.6
    headscons
    export PATH=$GLAST_EXT/python/2.6.5/gcc41/bin:$PATH
    export PYTHONPATH=`echo $PYTHONPATH | sed 's/python2.7/python2.6/g'`
    export setup=`echo $setup | sed 's/headscons/headscons26/g'`
}


function devscons {
    # path of scons code
    export PATH=$PATH:/afs/slac/g/glast/applications/SCons/1.3.0/bin

    export GLAST_EXT=/afs/slac/g/glast/ground/GLAST_EXT/${BLDTYPE}

    export INST_DIR=/u/gl/lande/dev/ScienceTools-scons
    source ${INST_DIR}/bin/${BLDTYPE}-Optimized/_setup.sh

    export PATH=~/svn/lande/trunk/extended_catalog/code/:~/svn/lande/trunk/pointlike/:$PATH
    export PYTHONPATH=~/svn/lande/trunk/extended_catalog/code/:~/svn/lande/trunk/pointlike/:$PYTHONPATH

    # point at the most up to the cvs version of all the pointlike code
    export PYTHONPATH=/u/gl/lande/dev/ScienceTools-scons/pointlike/python:$PYTHONPATH

    export python=$INST_DIR/pointlike/python/uw/like

    export PFILES=".;$PFILES"

    export CALDB=${INST_DIR}/irfs/caldb/CALDB/

    export setup="${setup} sconsdev"
}

function buildscons {
    scons --with-GLAST-EXT=${GLAST_EXT} --compile-opt pointlike 
    scons --with-GLAST-EXT=${GLAST_EXT} --compile-opt skymaps
    scons --with-GLAST-EXT=$GLAST_EXT --compile-opt setup
}


function slac_alias {

    # places at SLAC
    export u31="/nfs/farm/g/glast/u31/lande" # Josh's u31 home
    export afs=/afs/slac/g/glast/users/lande
    export markus=/u/gl/markusa/disk/glast_data/gammas/
    export sass="/afs/slac/www/slac/sass"

    export ki03="/nfs/slac/g/ki/ki03/lande"
    export FERMI=$ki03/fermi/data
    export FERMILANDE=$FERMI # in case I have to share with others
    export CATALOG=$ki03/fermi_data/catalog_mirror/catalog_jan_31_2011/

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
slac_alias

export PYTHONPATH="$HOME/bin:$HOME/python:$PYTHONPATH"

function mathematica_setup {
    PATH=$PATH:/afs/slac.stanford.edu/g/ki/software/Wolfram/Mathematica/6.0/Executables/
}

export PATH=~/bin:~/svn/lande/trunk/general/bin/:$PATH

# local stuff
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/lib


function lsf_setup {
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
        eval "function $queue { bsub -q $queue -oo log.txt python $PWD/$1; }"
    done
    
    #function xxl { bsub -q xxl -oo log.txt python $PWD/$1 }

    # Alias to show just the queues I like
    alias bq="bqueues short medium long xlong xxl kipac-ibq"

}
lsf_setup


export CVSROOT=/nfs/slac/g/glast/ground/cvs



# Get hte program STAG
export PATH="/afs/slac.stanford.edu/g/glast/applications/stag/i386_rhel40/:$PATH"

function tagCollector {
    # Tag the science tools
    echo python tagCollector.py ScienceTools --new=HEAD -r True
}


function snrcat1setup {
    GREENCAT=/nfs/slac/g/ki/ki03/lande/green_catalog/v1
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
    export CVSROOT=/nfs/slac/g/glast/ground/paper_drafts/
    #cvs co ScienceGroups/CandA/Pass7Validation

    #The paper is in this folder: /u/gl/lande/cvs/ScienceGroups/CandA/Pass7Validation/

    # Add text here on bad psf vs high level science
    # /u/gl/lande/cvs/ScienceGroups/CandA/Pass7Validation/pointSpreadFunction/psfHighLevel.tex

    # Add text here on
    # 10 year vs 2 year sensitivity: to ~/cvs/ScienceGroups/CandA/Pass7Validation/sciencePerformance/perf_spatialExtent.tex

}

function dm_satellite_setup {
    export SHERIDAN=~szalewsk
}



function pwncat_setup {
    export alice=~allafort/ki05/pwncatalog/
    export marianne=/nfs/farm/g/glast/u54/lemoine/PWNCat

    export pwncode=~/svn/lande/trunk/pwncatalog/PWNCAT2/code
    export pwnplots=~/svn/lande/trunk/pwncatalog/PWNCAT2/code/lande/publication_plots/
    export pwnpaper=~/svn/lande/trunk/pwncatalog/PWNCAT2/paper
    export pwndata=$ki03/pwncatalog/PWNCAT2/analyze_psr/
    export pwnpersonal=/u/gl/lande/work/fermi/pwncatalog/PWNCAT2
    export pwnmc=~/svn/lande/trunk/pwncatalog/PWNCAT2/mc

    export tevdata=$ki03/pwncatalog/PWNCAT2/analyze_tev/

    export PYTHONPATH=$PYTHONPATH:$pwncode/lande/publication_plots/plot_helper
    export PYTHONPATH=$PYTHONPATH:$pwncode/lande/tables

    #export PWNSCRIPTS=~lande/svn/lande/trunk/pwncatalog_1yr/
}
pwncat_setup



function setup_pysed {
    export PYTHONPATH=~/svn/lande/trunk/:$PYTHONPATH
    export sed=~/svn/lande/trunk/pysed/
}
setup_pysed



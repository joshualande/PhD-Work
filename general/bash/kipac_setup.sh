
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

function mathematica_setup {
    PATH=$PATH:/afs/slac.stanford.edu/g/ki/software/Wolfram/Mathematica/8.0/Executables
}

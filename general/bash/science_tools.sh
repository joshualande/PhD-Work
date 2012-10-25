
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


function _stockscons {
    export SCTOOLS=$1
    export optflag=$2

    set_bldtype
    export GLAST_EXT=/afs/slac/g/glast/ground/GLAST_EXT/${BLDTYPE}
    export BUILDS=/nfs/farm/g/glast/u35/ReleaseManagerBuild
    export INST_DIR=${BUILDS}/${BLDTYPE}/$optflag/ScienceTools/$SCTOOLS
    source ${INST_DIR}/bin/${BLDTYPE}-$optflag/_setup.sh

    export setup="${setup} stockscons"
}

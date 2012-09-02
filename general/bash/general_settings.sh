# These are my bash

function setup_terminal_tweaks {
    [ -z "$PS1" ] && return
    export TERM=xterm-color

    # http://blog.pclewis.com/2010/03/tip-make-bash-tab-completion-ignore-svn-directories/
    export FIGNORE=.svn 

    set -o vi # vi like navigation of command line.
    export EDITOR=vim

    # I like this simple prompt
    export PS1="\h:\W $ " 

    # Disable all core dump files. I am not sure this works correctly
    ulimit -c 0 



    #stty sane;stty erase ^H # This stuff makes backspace work
    shopt -s checkwinsize
}




function get_known_hosts {
    # Not sure which commadn will work
    echo wget -O ~/.ssh/known_hosts ftp://ftp.slac.stanford.edu/admin/known_hosts 
    echo curl ftp://ftp.slac.stanford.edu/admin/known_hosts  > ~/.ssh/known_hosts
}

function setup_alias_general {

    alias clean="rm -f *~;rm -f .*~;rm -f '#'*;rm -rf .*.swp;rm -rf .'#'*"
    alias screen='screen -RD'
    alias root='root -l'
    alias killeverything='for x in `jobs -p`; do kill -9 $x; done'
    alias rm="rm -iv" # warn before removing & verbose
    alias mv="mv -fi"
    alias cp="cp -afi"
    alias less='less -I' # case insensitive search
    alias l="ls --color" # print out size next to each of them
    alias duh='du -h --max-depth=1' # human readable and not recursive
    alias ack='ack -i'
    alias grep='grep -i'

    alias tarup="tar -czvf" # tar -czvf MyArchive.tgz Source_folder
    alias untar="tar -xzvf" # tar -xzvf MyArchive.tgz

    alias sng="sed 's/:/\n/g'"

    # Command taken from 
    # http://www.workingwith.me.uk/blog/a_useful_cvs_status_checker
    alias cvstat='cvs -q status | grep ^[?F] | grep -v "to-date"'


    # alias public slac machiens
    for input in ki-rh29 `cat ~/.ssh/known_hosts | awk -F',' '{print $1}'  | grep -v '#' | grep -v "^$"`; do
        alias $input="ssh lande@$input.slac.stanford.edu"
        input=`echo $input | sed 's/[0-9]//g'`
        alias $input="ssh lande@$input.slac.stanford.edu"
    done

    alias svnvimdiff='svn diff --diff-cmd ~/bin/svnvimdiff'
    alias svstat='svn stat'


    # Don't tab complete for files that begin with a dot.
    # http://svn.haxx.se/users/archive-2004-12/0809.shtml
    bind 'set match-hidden-files off' 
}

function setup_python_general {
export PYTHONUNBUFFERED=True
}


function setup_svn_lande {
    # Best to put my SVN in the same place on all machine so
    # aliases are the same
    export svn=$HOME/svn/lande/trunk
    export presentations=$svn/presentations/
    export lande=/u/gl/lande/svn/lande/trunk/code/lande
}


function setup_default_general {
    setup_terminal_tweaks
    setup_alias_general
    setup_python_general
    setup_svn_lande
}
setup_default_general

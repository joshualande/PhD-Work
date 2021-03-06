
function ipyssh {

	if [ $# -ne 2 ]; then
	  echo "Usage: ipyssh SSH_HOST KERNEL"
	  echo "Example: ipyssh lande@ki-ls03.slac.stanford.edu kernel-dd803c1b-65bc-468a-8e55-67655476a9f3.json"
	  return 0
	fi

        host=$1
        kernel=$2
	profile=nbserver

        tempfile=`mktemp /tmp/XXXXXXXXXX`

        ssh $host "cat ~/.config/ipython/profile_$profile/security/$kernel" > $tempfile

        ipython qtconsole --ssh $host --existing $tempfile

        rm -f $tempfile
}


function launch_ipython_notebook {
        ipython notebook --pylab inline
}


function setup_paths {
    export ipython=/Users/joshualande/Google\ Drive/Career/ipython
    export PATH=/usr/local/mysql/bin:$PATH
    export svn="$HOME/Documents/work_svn/trunk/"
    export MY_BIN=$svn/general/bin

}

function setup_coursera_ml {
    #export coursera_ml=/Users/joshualande/Google\ Drive/Career/resources/courses/Stanford\ Machine\ Learning/My\ Work/homework
    export coursera_ml=/Users/joshualande/Documents/work_svn/trunk/courses/coursera_ml/homework/
    export ps1=$coursera_ml/ps1/ex1
    export ps2=$coursera_ml/ps2/ex2-003/mlclass-ex2
    export ps3=$coursera_ml/ps3/ex3-003/mlclass-ex3
    export ps4=$coursera_ml/ps4/ex4-003/mlclass-ex4
    export ps5=$coursera_ml/ps5/ex5-003/mlclass-ex5

    alias octave="exec '/Applications/Octave.app/Contents/Resources/bin/octave'"

}

function setup_preferences {
	set -o vi
}

function setup_insight {
    export insight_project="/Users/joshualande/Google Drive/Career/Insight Data Science Fellows Program/project"
    export reviewskim="/Users/joshualande/Documents/ReviewSkim/"
    export PYTHONPATH=$reviewskim
    export insight_imdb_db="$project/insight_imdb_db"
}


function setup_defaults {
    setup_insight
	setup_paths
	setup_preferences
	setup_coursera_ml
}
setup_defaults



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
}


function setup_preferences {
	set -o vi
}

function setup_defaults {
	setup_paths
	setup_preferences
}


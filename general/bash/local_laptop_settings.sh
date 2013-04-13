
function ipyssh {

	if [ $# -ne 2 ]; then
	  echo "Usage: ipyssh SSH_HOST KERNEL"
	  echo "Example: ipyssh lande@ki-ls03.slac.stanford.edu kernel-dd803c1b-65bc-468a-8e55-67655476a9f3.json"
	  return 0
	fi

        host=$1
        kernel=$2

        tempfile=`mktemp /tmp/XXXXXXXXXX`

        ssh $host "cat ~/.config/ipython/profile_nbserver/security/$kernel" > $tempfile

        ipython qtconsole --ssh $host --existing $tempfile

        rm $tempfile
}

set -o vi


function launch_ipython_notebook {
        ipython notebook --pylab inline
}



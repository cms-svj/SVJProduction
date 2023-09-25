#!/bin/bash -e

case `uname` in
	Linux) ECHO="echo -e" ;;
	*) ECHO="echo" ;;
esac

# defaults
ACCESS=https
YEAR=2022
declare -A CMSSW_YEARS
CMSSW_YEARS[2022]=CMSSW_12_4_15
CMSSW_YEARS[2023]=CMSSW_13_0_13
WHICH_CMSSW=
FORK=cms-svj
BRANCH=Run3
CORES=8
HLT=""

usage() {
	$ECHO "setup.sh [options]"
	$ECHO
	$ECHO "Options:"
	$ECHO "-y [year]     \tyear to simulate, determines default CMSSW release (choices: ${!CMSSW_YEARS[@]}) (default = $YEAR)"
	$ECHO "-c [release]  \tCMSSW release to install (default = ${CMSSW_YEARS[$YEAR]})"
	$ECHO "-f [fork]     \tclone from specified fork (default = $FORK)"
	$ECHO "-b [branch]   \tclone specified branch (default = $BRANCH)"
	$ECHO "-s [protocol] \tuse protocol to clone (default = ${ACCESS}, alternative = ssh)"
	$ECHO "-j [cores]    \t# cores for CMSSW compilation (default = ${CORES})"
	$ECHO "-h            \tprint this message and exit"
	exit $1
}

CUR_DIR=`pwd`
#check arguments
while getopts "y:c:f:b:s:j:th" opt; do
	case "$opt" in
	y) YEAR=$OPTARG
	;;
	c) WHICH_CMSSW=$OPTARG
	;;
	f) FORK=$OPTARG
	;;
	b) BRANCH=$OPTARG
	;;
	s) ACCESS=$OPTARG
	;;
	j) CORES=$OPTARG
	;;
	h) usage 0
	;;
	esac
done

if [[ -z "${CMSSW_YEARS[$YEAR]}" ]]; then
	$ECHO "Unknown year $YEAR"
	usage 1
fi

if [ -z "$WHICH_CMSSW" ]; then
	WHICH_CMSSW=${CMSSW_YEARS[$YEAR]}
fi

if [ "$ACCESS" = "ssh" ]; then
	export ACCESS_GITHUB=git@github.com:
	export ACCESS_CMSSW=--ssh
elif [ "$ACCESS" = "https" ]; then
	export ACCESS_GITHUB=https://github.com/
	export ACCESS_CMSSW=--https
else
	usage 1
fi

# OS check: try redhat-release first to handle Singularity case
# kept in view of handling post-SL7 OS
declare -A OS_PREFIX
OS_PREFIX[7]=slc7
OS_PREFIX[8]=el8
POSSIBLE_VERSIONS=( 7 8 )
if [[ -f "/etc/redhat-release" ]]; then
	VERSION_TMP=`awk -F'[ .]' '{print $4}' "/etc/redhat-release"`
	if [[ "${POSSIBLE_VERSIONS[@]} " =~ "${VERSION_TMP}" ]]; then
		SLC_VERSION="${OS_PREFIX[${VERSION_TMP}]}"
	else
		echo "WARNING::Unknown SLC version. Defaulting to SLC7."
		SLC_VERSION="slc7"
	fi
else
	for POSVER in ${POSSIBLE_VERSIONS[@]}; do
		if [[ `uname -r` == *"el${POSVER}"* ]]; then
			SLC_VERSION="${OS_PREFIX[$POSVER]}"
			break
		fi
	done
	if [ -z "$SLC_VERSION" ]; then
		echo "WARNING::Unknown SLC version. Defaulting to SLC7."
		SLC_VERSION="slc7"
	fi
fi

install_CMSSW(){
	THIS_CMSSW="$1"

	# -------------------------------------------------------------------------------------
	# CMSSW release area
	# -------------------------------------------------------------------------------------
	if [ -n "$THIS_CMSSW" ]; then
		case $THIS_CMSSW in
		CMSSW_12_4_*)
			export SCRAM_ARCH=${SLC_VERSION}_amd64_gcc10
		;;
		CMSSW_13_0_*)
			export SCRAM_ARCH=${SLC_VERSION}_amd64_gcc11
		;;
		*)
			$ECHO "Unknown architecture for release $THIS_CMSSW"
			exit 1
		;;
		esac
		scramv1 project CMSSW $THIS_CMSSW
		cd $THIS_CMSSW
		eval `scramv1 runtime -sh`
		$ECHO "setup $CMSSW_VERSION"
	fi

	# -------------------------------------------------------------------------------------
	# CMSSW compilation
	# -------------------------------------------------------------------------------------

	if [ -n "$THIS_CMSSW" ]; then
		# reinitialize environment
		eval `scramv1 runtime -sh`
		cd src
		git cms-init $ACCESS_CMSSW

		git clone ${ACCESS_GITHUB}kpedro88/CondorProduction Condor/Production
		git clone ${ACCESS_GITHUB}${FORK}/SVJProduction SVJ/Production -b ${BRANCH}

		# use as little of genproductions as possible
		git clone --depth 1 --no-checkout ${ACCESS_GITHUB}cms-svj/genproductions -b Run3 Configuration/GenProduction
		# setup sparse checkout
		cd Configuration/GenProduction
		git config core.sparsecheckout true
		{
			echo '/Utilities'
			echo '/bin/MadGraph5_aMCatNLO'
			echo '!/bin/MadGraph5_aMCatNLO/cards'
			echo '/MetaData'
		} > .git/info/sparse-checkout
		git read-tree -mu HEAD

		cd $CMSSW_BASE/src
		scram b -j $CORES
		cd SVJ/Production/batch
		python $CMSSW_BASE/src/Condor/Production/python/linkScripts.py
		python $CMSSW_BASE/src/Condor/Production/python/cacheAll.py
		ln -s $CMSSW_BASE/src/Condor/Production/python/manageJobs.py .
		ln -s $CMSSW_BASE/src/Condor/Production/python/createChain.py .
	fi
}

# run the installations
cd $CUR_DIR
install_CMSSW $WHICH_CMSSW

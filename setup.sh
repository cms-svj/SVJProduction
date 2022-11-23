#!/bin/bash -e

case `uname` in
	Linux) ECHO="echo -e" ;;
	*) ECHO="echo" ;;
esac

# defaults
ACCESS=https
WHICH_CMSSW=CMSSW_10_6_29_patch1
FORK=cms-svj
BRANCH=Run2_UL
CORES=8
HLT=""

usage() {
	$ECHO "setup.sh [options]"
	$ECHO
	$ECHO "Options:"
	$ECHO "-c [release]  \tCMSSW release to install (default = $WHICH_CMSSW)"
	$ECHO "-f [fork]     \tclone from specified fork (default = $FORK)"
	$ECHO "-b [branch]   \tclone specified branch (default = $BRANCH)"
	$ECHO "-s [protocol] \tuse protocol to clone (default = ${ACCESS}, alternative = ssh)"
	$ECHO "-j [cores]    \t# cores for CMSSW compilation (default = ${CORES})"
	$ECHO "-t            \tinstall HLT releases"
	$ECHO "-h            \tprint this message and exit"
	exit $1
}

CUR_DIR=`pwd`
#check arguments
while getopts "c:f:b:s:j:th" opt; do
	case "$opt" in
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
	t) HLT=true
	;;
	h) usage 0
	;;
	esac
done

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
if [[ -f "/etc/redhat-release" ]]; then
	VERSION_TMP=`awk -F'[ .]' '{print $4}' "/etc/redhat-release"`
	POSSIBLE_VERSIONS=( 7 )
	if [[ "${POSSIBLE_VERSIONS[@]} " =~ "${VERSION_TMP}" ]]; then
		SLC_VERSION="slc${VERSION_TMP}"
	else
		echo "WARNING::Unknown SLC version. Defaulting to SLC7."
		SLC_VERSION="slc7"
	fi
elif [[ `uname -r` == *"el7"* ]]; then
	SLC_VERSION="slc7"
else
	echo "WARNING::Unknown SLC version. Defaulting to SLC7."
SLC_VERSION="slc7"
fi

install_CMSSW(){
	THIS_CMSSW="$1"
	MINIMAL=
	UPDATE_HLT=

	# -------------------------------------------------------------------------------------
	# CMSSW release area
	# -------------------------------------------------------------------------------------
	if [ -n "$THIS_CMSSW" ]; then
		case $THIS_CMSSW in
		CMSSW_8_0_*)
			export SCRAM_ARCH=${SLC_VERSION}_amd64_gcc530
			UPDATE_HLT=1
			MINIMAL=1
		;;
		CMSSW_9_4_*)
			export SCRAM_ARCH=${SLC_VERSION}_amd64_gcc630
			MINIMAL=1
		;;
		CMSSW_10_2_*)
			export SCRAM_ARCH=${SLC_VERSION}_amd64_gcc700
			MINIMAL=1
		;;
		CMSSW_10_6_*)
			export SCRAM_ARCH=${SLC_VERSION}_amd64_gcc700
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

		if [ -n "$UPDATE_HLT" ]; then
			git cms-merge-topic -u cms-svj:ScoutingContent80Xmin
		fi

		if [ -n "$MINIMAL" ]; then
			# don't need to compile SVJ-specific code for HLT
			cd SVJ/Production
			git config core.sparsecheckout true
			{
				echo '/batch'
				echo '/python'
				echo '/test'
			} > .git/info/sparse-checkout
			git read-tree -mu HEAD
			# skip genproductions entirely
		else
			# use as little of genproductions as possible
			git clone --depth 1 --no-checkout ${ACCESS_GITHUB}cms-svj/genproductions -b Run2_UL Configuration/GenProduction
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
		fi

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
if [ -n "$HLT" ]; then
	HLT_DIR=${CUR_DIR}/HLT
	mkdir -p $HLT_DIR
	for HLT_CMSSW in CMSSW_8_0_33_UL CMSSW_9_4_14_UL_patch1 CMSSW_10_2_16_UL; do
		cd $HLT_DIR
		install_CMSSW $HLT_CMSSW
	done
fi

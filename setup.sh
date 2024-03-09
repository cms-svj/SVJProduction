#!/bin/bash -e

case `uname` in
	Linux) ECHO="echo -e" ;;
	*) ECHO="echo" ;;
esac

# defaults
ACCESS=https
YEAR=2022
declare -A CMSSW_YEARS
CMSSW_YEARS[2022]="CMSSW_12_4_17,CMSSW_12_6_5,CMSSW_13_0_13"
CMSSW_YEARS[2023]="CMSSW_13_0_13"
WHICH_CMSSW=
FORK=cms-svj
BRANCH=Run3
CORES=8
TOOLS=(
pythia8 \
evtgen \
tauolapp \
)

usage() {
	$ECHO "setup.sh [options]"
	$ECHO
	$ECHO "Options:"
	$ECHO "-y [year]     \tyear to simulate, determines default CMSSW release (choices: ${!CMSSW_YEARS[@]}) (default = $YEAR)"
	$ECHO "-c [release]  \tCMSSW release(s) to install, comma-separated (default = ${CMSSW_YEARS[$YEAR]})"
	$ECHO "-f [fork]     \tclone from specified fork (default = $FORK)"
	$ECHO "-b [branch]   \tclone specified branch (default = $BRANCH)"
	$ECHO "-s [protocol] \tuse protocol to clone (default = ${ACCESS}, alternative = ssh)"
	$ECHO "-j [cores]    \t# cores for CMSSW compilation (default = ${CORES})"
	$ECHO "-h            \tprint this message and exit"
	exit $1
}

CUR_DIR=`pwd`
# check arguments
while getopts "y:c:f:b:s:j:h" opt; do
	case "$opt" in
	y) YEAR=$OPTARG
	;;
	c) IFS="," read -a WHICH_CMSSW <<< "$OPTARG"
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
	IFS="," read -a WHICH_CMSSW <<< "${CMSSW_YEARS[$YEAR]}"
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
	VERSION_TMP=$(grep -o "[0-9]\.\?" /etc/redhat-release | head -n1 | cut -d'.' -f1)
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

install_tools(){
	BUILD_BRANCH=$1
	TOOLS=($2)

	# patched pythia
	cd $CMSSW_BASE
	git clone ${ACCESS_GITHUB}cms-svj/build -b $BUILD_BRANCH
	cd build
	CMSSW_BRANCH=$(echo $THIS_CMSSW | cut -d'_' -f1-3)"_X"
	PDIR=${CMSSW_BRANCH}/${SCRAM_ARCH}/tools
	if [ -d $PDIR ]; then
		# only keep relevant artifacts
		git config core.sparsecheckout true
		echo $PDIR > .git/info/sparse-checkout
		git read-tree -mu HEAD
		# link the unchanged external files
		for TOOL in ${TOOLS[@]}; do
			LATESTDIR=$(ls -drt ${PDIR}/${TOOL}/* | tail -1)
			ORIGDIR=$(dirname $(cd $CMSSW_RELEASE_BASE && scram tool tag $TOOL LIBDIR) || echo "")
			if [ -n "$ORIGDIR" ]; then
				# existing (changed) files will be kept
				lndir $ORIGDIR $LATESTDIR
			fi
			cp ${PDIR}/${TOOL,,}.xml ${CMSSW_BASE}/config/toolbox/${SCRAM_ARCH}/tools/selected/
			scram setup $TOOL
		done
		cd $CMSSW_BASE/src
		scram b checkdeps
	else
		$ECHO "WARNING: patched ${TOOLS[@]} not found for $PDIR"
		cd $CMSSW_BASE
		rm -rf $CMSSW_BASE/build
	fi
}

install_CMSSW(){
	THIS_CMSSW="$1"
	if [ -z "$THIS_CMSSW" ]; then
		return
	fi

	# -------------------------------------------------------------------------------------
	# CMSSW release area
	# -------------------------------------------------------------------------------------

	case $THIS_CMSSW in
	CMSSW_12_4_*)
		export SCRAM_ARCH=${SLC_VERSION}_amd64_gcc10
	;;
	CMSSW_12_6_*)
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

	# -------------------------------------------------------------------------------------
	# CMSSW compilation
	# -------------------------------------------------------------------------------------

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

	if [[ $THIS_CMSSW = CMSSW_12_4_* ]]; then
		install_tools "main" "pythia8 evtgen tauolapp"
	elif [[ $THIS_CMSSW = CMSSW_13_0_* ]]; then
		install_tools "CICADA" "hls4mlEmulatorExtras CICADA"
		git cms-merge-topic -u cms-svj:CICADA_backport-13_0_13_from_14_0_0_pre2_Paper_Mods
	fi

	cd $CMSSW_BASE/src
	scram b -j $CORES
	$CMSSW_BASE/src/Condor/Production/scripts/postInstall.sh -b $CMSSW_BASE/src/SVJ/Production/batch -c -p
}

# run the installations
for WC in ${WHICH_CMSSW[@]}; do
	cd $CUR_DIR
	install_CMSSW $WC
done

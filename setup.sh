#!/bin/bash -e

case `uname` in
	Linux) ECHO="echo -e" ;;
	*) ECHO="echo" ;;
esac

usage() {
	$ECHO "setup.sh [options]"
	$ECHO
	$ECHO "Options:"
	$ECHO "-c <RELEASE>  \tCMSSW release to install (e.g. CMSSW_7_1_26)"
	$ECHO "-f [fork]     \tclone from specified fork (default = kpedro88)"
	$ECHO "-b [branch]   \tclone specified branch (default = master)"
	$ECHO "-p            \tinstall Pythia 8.230 w/ ME correction"
	$ECHO "-a            \tinstall analysis code"
	$ECHO "-h            \tprint this message and exit"
	exit $1
}

# -------------------------------------------------------------------------------------
# pythia installation
# -------------------------------------------------------------------------------------

installPythia() {
	cd ${CMSSW_BASE}

	# some really bad ways to get info out of scram
	HEPMC_BASE=$(scram tool info hepmc | grep "HEPMC_BASE" | sed 's/HEPMC_BASE=//')
	BOOST_BASE=$(scram tool info boost | grep "BOOST_BASE" | sed 's/BOOST_BASE=//')
	LHAPDF_BASE=$(scram tool info lhapdf | grep "LHAPDF_BASE" | sed 's/LHAPDF_BASE=//')

	# get pythia8 source and compile
	git clone git@github.com:kpedro88/pythia8 -b "MECorr230"
	cd pythia8
	# configure for c++11 if 7_1_X
	EXTRA=""
	case $CMSSW_VERSION in
	CMSSW_7_1_*)
		EXTRA='--cxx-common="-std=c++11 -fPIC"'
	;;
	esac
	./configure --enable-shared --with-boost=${BOOST_BASE} --with-hepmc2=${HEPMC_BASE} --with-lhapdf6=${LHAPDF_BASE} --with-lhapdf6-plugin=LHAPDF6.h "$EXTRA"
	make -j 8
	make install

	# create xml for tool
	cd $CMSSW_BASE
	cat << 'EOF_TOOLFILE' > pythia8.xml
<tool name="pythia8" version="230">
  <lib name="pythia8"/>
  <client>
    <environment name="PYTHIA8_BASE" default="$CMSSW_BASE/pythia8"/>
    <environment name="LIBDIR" default="$PYTHIA8_BASE/lib"/>
    <environment name="INCLUDE" default="$PYTHIA8_BASE/include"/>
  </client>
  <runtime name="PYTHIA8DATA" value="$PYTHIA8_BASE/share/Pythia8/xmldoc"/>
  <use name="hepmc"/>
  <use name="lhapdf"/>
</tool>
EOF_TOOLFILE

	# install tool in scram
	cp ${CMSSW_BASE}/pythia8.xml ${CMSSW_BASE}/config/toolbox/${SCRAM_ARCH}/tools/selected
	scram setup pythia8

	# better to use 'scram b checkdeps' but this is not available in 71X
	scram b echo_pythia8_USED_BY | tr ' ' '\n' | grep "self" | cut -d'/' -f2-3 | sort -u > pkgs.txt

	# update CMSSW dependencies
	cd $CMSSW_BASE/src
	git cms-addpkg -f ../pkgs.txt
}

CUR_DIR=`pwd`
WHICH_CMSSW=""
FORK=kpedro88
BRANCH=master
INSTALL_PYTHIA=""
INSTALL_ANALYSIS=""
#check arguments
while getopts "c:f:b:pah" opt; do
	case "$opt" in
	c) WHICH_CMSSW=$OPTARG
	;;
	f) FORK=$OPTARG
	;;
	b) BRANCH=$OPTARG
	;;
	p) INSTALL_PYTHIA=yes
	;;
	a) INSTALL_ANALYSIS=yes
	;;
	h) usage 0
	;;
	esac
done

if [ -z "$WHICH_CMSSW" ] && [ -z "$INSTALL_PYTHIA" ]; then
	usage 1
fi

# -------------------------------------------------------------------------------------
# CMSSW release area
# -------------------------------------------------------------------------------------
if [ -n "$WHICH_CMSSW" ]; then
	case $WHICH_CMSSW in
	CMSSW_7_1_*)
		export SCRAM_ARCH=slc6_amd64_gcc481
	;;
	CMSSW_8_0_*)
		export SCRAM_ARCH=slc6_amd64_gcc530
	;;
	CMSSW_9_3_*)
		export SCRAM_ARCH=slc6_amd64_gcc630
	;;
	CMSSW_9_4_*)
		export SCRAM_ARCH=slc6_amd64_gcc630
	;;
	*)
		$ECHO "Unknown architecture for release $WHICH_CMSSW"
		exit 1
	;;
	esac
	scramv1 project CMSSW $WHICH_CMSSW
	cd $WHICH_CMSSW
	CUR_DIR=`pwd`
	eval `scramv1 runtime -sh`
	$ECHO "setup $CMSSW_VERSION"
fi

# -------------------------------------------------------------------------------------
# CMSSW compilation
# -------------------------------------------------------------------------------------

if [ -n "$WHICH_CMSSW" ]; then
	# reinitialize environment
	eval `scramv1 runtime -sh`
	cd src
	git cms-init
	if [[ $WHICH_CMSSW = CMSSW_9_4_* ]]; then
		git cms-merge-topic -u kpedro88:debugEventSetupMultithreaded9410
	fi

	if [ -n "$INSTALL_ANALYSIS" ]; then
		git clone git@github.com:kpedro88/Analysis -b SVJ2017-gen
	fi

	# get packages
	if [ -n "$INSTALL_PYTHIA" ]; then
		installPythia
		eval `scramv1 runtime -sh`
	fi
	git clone git@github.com:kpedro88/CondorProduction Condor/Production
	git clone git@github.com:${FORK}/SVJProduction SVJ/Production -b ${BRANCH}
	scram b -j 8
	cd SVJ/Production/batch
	ln -s $CMSSW_BASE/src/Condor/Production/scripts/* .
fi

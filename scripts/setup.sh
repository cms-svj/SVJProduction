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
	$ECHO "-p            \tinstall Pythia 8.226"
	exit 1
}

CUR_DIR=`pwd`
WHICH_CMSSW=""
INSTALL_PYTHIA=""
#check arguments
while getopts "c:p" opt; do
	case "$opt" in
	c) WHICH_CMSSW=$OPTARG
	;;
	p) INSTALL_PYTHIA=yes
	;;
	esac
done

if [ -z "$WHICH_CMSSW" ] && [ -z "$INSTALL_PYTHIA" ]; then
	usage
fi

# -------------------------------------------------------------------------------------
# CMSSW release area
# -------------------------------------------------------------------------------------
if [ -n "$WHICH_CMSSW" ]; then
	export SCRAM_ARCH=slc6_amd64_gcc481
	scramv1 project CMSSW $WHICH_CMSSW
	cd $WHICH_CMSSW
	CUR_DIR=`pwd`
	eval `scramv1 runtime -sh`
	$ECHO "setup $CMSSW_VERSION"
fi

# -------------------------------------------------------------------------------------
# pythia installation
# -------------------------------------------------------------------------------------

if [ -n "$INSTALL_PYTHIA" ]; then
	if [ -n "$WHICH_CMSSW" ]; then
		# create xml for tool
		cat << 'EOF_TOOLFILE' > pythia8.xml
<tool name="pythia8" version="226">
  <lib name="pythia8"/>
  <client>
    <environment name="PYTHIA8_BASE" default="$CMSSW_BASE/pythia8226"/>
    <environment name="LIBDIR" default="$PYTHIA8_BASE/lib"/>
    <environment name="INCLUDE" default="$PYTHIA8_BASE/include"/>
  </client>
  <runtime name="PYTHIA8DATA" value="$PYTHIA8_BASE/share/Pythia8/xmldoc"/>
  <use name="hepmc"/>
  <use name="lhapdf"/>
</tool>
EOF_TOOLFILE
	fi

	# get pythia8 source and compile
	wget -q http://home.thep.lu.se/~torbjorn/pythia8/pythia8226.tgz
	tar -xzf pythia8226.tgz
	export PYTHIA8DATA=$CUR_DIR/pythia8226/share/Pythia8/xmldoc
	cd pythia8226/
	gmake

	if [ -n "$WHICH_CMSSW" ]; then
		cd $CUR_DIR
		# install tool in scram
		cp ${CMSSW_BASE}/pythia8.xml ${CMSSW_BASE}/config/toolbox/${SCRAM_ARCH}/tools/selected
		scram setup pythia8

		$ECHO "you can now link to the pythia8 libraries through scram!"
	fi

	# cleanup
	rm pythia8226.tgz
fi

# -------------------------------------------------------------------------------------
# CMSSW compilation
# -------------------------------------------------------------------------------------

if [ -n "$WHICH_CMSSW" ]; then
	# reinitialize environment
	eval `scramv1 runtime -sh`
	cd src

	# get packages
	if [ -n "$INSTALL_PYTHIA" ]; then
		git cms-addpkg GeneratorInterface/EvtGenInterface GeneratorInterface/PartonShowerVeto GeneratorInterface/Pythia8Interface
		if [[ "$WHICH_CMSSW" == "CMSSW_7_1_"* ]]; then
			$ECHO "Merging FixPythia7126"
			git cms-merge-topic kpedro88:FixPythia7126
		fi
	fi
	git clone git@github.com:kpedro88/SVJProduction SVJ/Production
	scram b -j 8
fi

#!/bin/bash

export JOBNAME=""
export PART=""
export OUTDIR=""
export REDIR=""
export MODE=""
export USEFOLDERS=""
export OPTIND=1
while [[ $OPTIND -le $# ]]; do
	OPTOLD=$OPTIND
	# getopts in silent mode, don't exit on errors
	getopts ":fj:p:o:x:m:" opt || status=$?
	case "$opt" in
		f) export USEFOLDERS="true"
		;;
		j) export JOBNAME=$OPTARG
		;;
		p) export PART=$OPTARG
		;;
		o) export OUTDIR=$OPTARG
		;;
		x) export REDIR=$OPTARG
		;;
		m) export MODE=$OPTARG
		;;
		# keep going if getopts had an error, but make sure not to skip anything
		\? | :) OPTIND=$((OPTOLD+1))
		;;
	esac
done

echo "parameter set:"
echo "OUTDIR:     $OUTDIR"
echo "JOBNAME:    $JOBNAME"
echo "PART:       $PART"
echo "REDIR:      $REDIR"
echo "MODE:       $MODE"
echo "USEFOLDERS: $USEFOLDERS"
echo ""

if [[ "$MODE" == "madgraph" ]]; then
	EXE=python
	SCRIPT=runMG.py
	FTYPE=.tar.xz
else
	EXE=cmsRun
	SCRIPT=runSVJ.py
	FTYPE=.root
fi

# link files from CMSSW dir
ln -fs ${CMSSWVER}/src/SVJ/Production/test/${SCRIPT}

# run CMSSW
ARGS=$(cat args_${JOBNAME}.txt)
ARGS="$ARGS part=$PART"
if [[ -n "$REDIR" ]]; then
	ARGS="$ARGS redir=${REDIR}"
fi
if [[ "${USEFOLDERS}" == "true" ]] && [[ "$ARGS" != *"useFolders"* ]] ; then
	ARGS="$ARGS useFolders=1"
fi
echo "${EXE} ${SCRIPT} ${ARGS} 2>&1"
${EXE} ${SCRIPT} ${ARGS} 2>&1

CMSEXIT=$?

# cleanup
rm ${SCRIPT}
if ls *.pkl >& /dev/null; then
	rm *.pkl
fi

if [[ $CMSEXIT -ne 0 ]]; then
	rm *${FTYPE}
	echo "exit code $CMSEXIT, skipping xrdcp"
	exit $CMSEXIT
fi

# check for gfal case
CMDSTR="xrdcp"
GFLAG=""
if [[ "$OUTDIR" == "gsiftp://"* ]]; then
	CMDSTR="gfal-copy"
	GFLAG="-g"
fi
# copy output to eos
echo "$CMDSTR output for condor"
for FILE in *${FTYPE}; do
	FILE_DST=${FILE}
	if [[ "${USEFOLDERS}" == "true" ]]; then
		echo "Changing to folder structure: <sample>/<part>.root"
		echo -e "\tPrior to change: ${FILE_DST}"
		FILE_DST=$(echo ${FILE_DST} | sed -E 's~(.*)_part~\1/part~'
		echo -e "\t   After change: ${FILE_DST}"
	fi

	echo "${CMDSTR} -f ${FILE} ${OUTDIR}/${FILE_DST}"
	stageOut ${GFLAG} -x "-f" -i ${FILE} -o ${OUTDIR}/${FILE_DST} -r -c '*'${FTYPE} 2>&1
	XRDEXIT=$?
	if [[ $XRDEXIT -ne 0 ]]; then
		echo "exit code $XRDEXIT, failure in ${CMDSTR}"
		exit $XRDEXIT
	fi
done

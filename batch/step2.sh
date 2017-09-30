#!/bin/bash

export JOBNAME=""
export PART=""
export OUTDIR=""
export REDIR=""
export OPTIND=1
while [[ $OPTIND -lt $# ]]; do
	# getopts in silent mode, don't exit on errors
	getopts ":j:p:o:x:" opt || status=$?
	case "$opt" in
		j) export JOBNAME=$OPTARG
		;;
		p) export PART=$OPTARG
		;;
		o) export OUTDIR=$OPTARG
		;;
		x) export REDIR=$OPTARG
		;;
		# keep going if getopts had an error
		\? | :) OPTIND=$((OPTIND+1))
		;;
	esac
done

echo "parameter set:"
echo "OUTDIR:     $OUTDIR"
echo "JOBNAME:    $JOBNAME"
echo "PART:       $PART"
echo "REDIR:      $REDIR"
echo ""

# link files from CMSSW dir
ln -fs ${CMSSWVER}/src/SVJ/Production/test/runSVJ.py

# run CMSSW
ARGS=$(cat args_${JOBNAME}.txt)
ARGS="$ARGS part=$PART"
if [[ -n "$REDIR" ]]; then
 ARGS="$ARGS redir=${REDIR}"
fi
echo "cmsRun runSVJ.py ${ARGS} 2>&1"
cmsRun runSVJ.py ${ARGS} 2>&1

# cleanup
rm runSVJ.py
PUFILE=Neutrino_E-10_gun_RunIISpring15PrePremix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v2-v2_GEN-SIM-DIGI-RAW.pkl
if [ -e $PUFILE ]; then
  rm $PUFILE
fi

CMSEXIT=$?

if [[ $CMSEXIT -ne 0 ]]; then
  rm *.root
  echo "exit code $CMSEXIT, skipping xrdcp"
  exit $CMSEXIT
fi

# copy output to eos
echo "xrdcp output for condor"
for FILE in *.root
do
  echo "xrdcp -f ${FILE} ${OUTDIR}/${FILE}"
  xrdcp -f ${FILE} ${OUTDIR}/${FILE} 2>&1
  XRDEXIT=$?
  if [[ $XRDEXIT -ne 0 ]]; then
    rm *.root
    echo "exit code $XRDEXIT, failure in xrdcp"
    exit $XRDEXIT
  fi
  rm ${FILE}
done


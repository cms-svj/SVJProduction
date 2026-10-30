#!/bin/bash

USERS=6
declare -A YEARJOBS
YEARJOBS[2016]=20
YEARJOBS[2017]=22
YEARJOBS[2018]=33
# total scan for summary statistics
YEARJOBS[201X]=$((YEARJOBS[2016]+YEARJOBS[2017]+YEARJOBS[2018]))
for YEAR in "${!YEARJOBS[@]}"; do
	echo ${YEAR}
	python generateScanScouting.py base -x ${YEAR}
	python generateScanScouting.py first -i signals_scouting_scan_${YEAR}_base_v0.py -a 2 -x ${YEAR} -j ${YEARJOBS[$YEAR]} -p ${USERS} -s jobs
done

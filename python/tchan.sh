#!/bin/bash -x

USERS=6

declare -A YEARJOBS
# per-year scans for actual submission
YEARJOBS[2016]=23
YEARJOBS[2017]=26
YEARJOBS[2018]=38
# total scan for summary statistics
YEARJOBS[201X]=$((YEARJOBS[2016]+YEARJOBS[2017]+YEARJOBS[2018]))
for YEAR in "${!YEARJOBS[@]}"; do
	echo ${YEAR}
	python generateScanTchan.py base -x ${YEAR}
	python generateScanTchan.py first -i signals_tchan_scan_${YEAR}_base_v0.py -a 2 -x ${YEAR} -j ${YEARJOBS[$YEAR]} -p ${USERS} -s num
	python generateScanTchan.py extend -i signals_tchan_scan_${YEAR}_base_v1.py -e signals_tchan_extend.py -x ${YEAR}_ext -m 5 -j ${YEARJOBS[$YEAR]} -p ${USERS} -s jobs
done

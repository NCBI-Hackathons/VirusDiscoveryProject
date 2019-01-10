#!/bin/bash

set -u
export k=8
export s=1
CONTIG=3000
export INDIR="/rsgrps/bhurwitz/mattmiller899/LSTM/ismb2017_lstm/data_${CONTIG}"
export POSNAME="girus_unsplit_${CONTIG}"
export NEGNAME="virus_unsplit_${CONTIG}"
export WINDOW=15
ARGS="-q standard -W group_list=bhurwitz -M mattmiller899@email.arizona.edu -m a"
JOB_ID=`qsub $ARGS -v k,s,INDIR,POSNAME,NEGNAME,WINDOW -N LSTM_3000_8mer -J 1-7 ./run_lstm.sh`
if [ "${JOB_ID}x" != "x" ]; then
    echo Job: \"$JOB_ID\"
else
    echo Problem submitting job. Job terminated.
    exit 1
fi
echo "job successfully submitted"

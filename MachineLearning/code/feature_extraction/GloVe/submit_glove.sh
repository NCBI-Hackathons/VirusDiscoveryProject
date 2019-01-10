#!/bin/bash

set -u
CONTIG=3000
export NAME="gv_unsplit_${CONTIG}_train"
export k=6
export stride=1
export IN_DIR="/rsgrps/bhurwitz/mattmiller899/LSTM/ismb2017_lstm/data_${CONTIG}"
export EXT="fasta"
ARGS="-q standard -W group_list=bhurwitz -M mattmiller899@email.arizona.edu -m a"
JOB_ID=`qsub $ARGS -v NAME,k,stride,IN_DIR,EXT -N GloVe3000_gv -J 1-7 ./glove.sh`
if [ "${JOB_ID}x" != "x" ]; then
    echo Job: \"$JOB_ID\"
else
    echo Problem submitting job. Job terminated.
    exit 1
fi
echo "job successfully submitted"


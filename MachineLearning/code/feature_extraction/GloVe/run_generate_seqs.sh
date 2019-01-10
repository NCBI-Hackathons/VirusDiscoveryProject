#!/bin/bash
#PBS -l select=1:ncpus=4:mem=24gb:pcmem=6gb
#PBS -l walltime=24:00:00

cd $PBS_O_WORKDIR
source activate LSTM
pos_name="${P_NAME}_${PBS_ARRAY_INDEX}.${EXT}"
neg_name="${N_NAME}_${PBS_ARRAY_INDEX}.${EXT}"
python generate_seqs_${EXT}.py $k $s $pos_name $neg_name $IN_DIR $TYPE

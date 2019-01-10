#PBS -l select=1:ncpus=28:mem=168gb:ngpus=1
#PBS -l walltime=24:00:00

echo "hello"
cd $PBS_O_WORKDIR
module load singularity
#THEANO_FLAGS='device=cpu' python lstm.py -batchsize 100 -s 1 -k 6
singularity run --nv keras_gpu3.img lstm_matt.py -batchsize 100 -s $s -k $k -indir $INDIR -posname $POSNAME -negname $NEGNAME -iteration $PBS_ARRAY_INDEX -window $WINDOW

set -u

step=2
k=6
name=""
while getopts :i:k:s:h OPT; do
  case $OPT in
    h)
      USAGE
      ;;
    i)
      name="$OPTARG"
      ;;
    s)
      step=$OPTARG
      ;;
    k)
      k="$OPTARG"
      ;;
    :)
      echo "Error: Option -$OPTARG requires an argument."
      exit 1
      ;;
    \?)
      echo "Error: Invalid option: -${OPTARG:-""}"
      exit 1
  esac
done

# Makes prokmers, downloads sample data, trains a GloVe model, and then evaluates it.
# One optional argument can specify the language used for eval script: matlab, octave or [default] python
WINDOW_SIZE=$((k * 2))
#    name="${NAME}_${PBS_ARRAY_INDEX}.${EXT}"
CORPUS=${name}_${k}kmer_${step}step_oneline
VOCAB_FILE=${name}_${k}kmer_${step}step_vocab.txt
COOCCURRENCE_FILE=${name}_${k}kmer_${step}step_cooccurrence_${WINDOW_SIZE}window.bin
COOCCURRENCE_SHUF_FILE=${name}_${k}kmer_${step}step_cooccurrence.shuf_${WINDOW_SIZE}window.bin
SAVE_FILE=${name}_${k}kmer_${step}step_${WINDOW_SIZE}window_vectors
OVERFLOW_FILE=${name}_${k}kmer_${step}_tmp
BUILDDIR=./GloVe/build
VERBOSE=2
MEMORY=160.0
VOCAB_MIN_COUNT=10
VECTOR_SIZE=100
MAX_ITER=300
BINARY=2
NUM_THREADS=28
X_MAX=30000

echo "$ $BUILDDIR/vocab_count -min-count $VOCAB_MIN_COUNT -verbose $VERBOSE < $CORPUS > $VOCAB_FILE"
$BUILDDIR/vocab_count -min-count $VOCAB_MIN_COUNT -verbose $VERBOSE < $CORPUS > $VOCAB_FILE
echo "$ $BUILDDIR/cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE -overflow-file $OVERFLOW_FILE < $CORPUS > $COOCCURRENCE_FILE"
$BUILDDIR/cooccur -memory $MEMORY -vocab-file $VOCAB_FILE -verbose $VERBOSE -window-size $WINDOW_SIZE -overflow-file $OVERFLOW_FILE  < $CORPUS > $COOCCURRENCE_FILE
echo "$ $BUILDDIR/shuffle -memory $MEMORY -verbose $VERBOSE -temp-file $OVERFLOW_FILE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE"
$BUILDDIR/shuffle -memory $MEMORY -verbose $VERBOSE -temp-file $OVERFLOW_FILE < $COOCCURRENCE_FILE > $COOCCURRENCE_SHUF_FILE
echo "$ $BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE"
$BUILDDIR/glove -save-file $SAVE_FILE -threads $NUM_THREADS -input-file $COOCCURRENCE_SHUF_FILE -x-max $X_MAX -iter $MAX_ITER -vector-size $VECTOR_SIZE -binary $BINARY -vocab-file $VOCAB_FILE -verbose $VERBOSE

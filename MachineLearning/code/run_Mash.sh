#### requirement : download MASH from https://github.com/marbl/mash

export CWD=$PWD
# where programs are
export BIN_DIR="PATH_TO_BIN/mash-Linux64-v2.1"
# where the dataset to prepare is
export DIR="PATH_TO_IMPUT_DIR"
export DATASET_LIST="PATH_TO_IMPUT_DIR/list_files.txt"
export OUT_DIR="PATH_TO_OUTPUT_DIR"
#parameters for MASH
export kmer=21 #kmer size
export sketch_size=10000 #sketch size
export filter=2 #remove kmers present in < filter size

cd $DIR
while read p; do
        NAME=${p:2}
        OUT="$OUT_DIR/$NAME"
        $BIN_DIR/mash sketch -k $kmer -s $sketch_size -r -m $filter $NAME -o $OUT
done < $DATASET_LIST


$BIN_DIR/mash paste all.msh *.fasta.msh

$BIN_DIR/mash dist -t all.msh all.msh > all_vs_all_matrix.txt

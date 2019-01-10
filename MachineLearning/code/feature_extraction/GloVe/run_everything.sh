set -u
INPUT_DIR=""
WORK_DIR=""
STEP=2
KMER=6
while getopts :i:k:s:h:w OPT; do
  case $OPT in
    h)
      ADVANCED_USAGE
      ;;
    i)
      INPUT_DIR="$OPTARG"
      ;;
    w)
      WORK_DIR="$OPTARG"
      ;;
    s)
      STEP=$OPTARG
      ;;
    k)
      KMER="$OPTARG"
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

echo "INPUT_DIR = '$INPUT_DIR'"
echo "WORK_DIR = '$WORK_DIR'"
echo "KMER = '$KMER'"
echo "STEP = '$STEP'"

if [[ "$WORK_DIR" = "" ]]; then
    echo "WORK_DIR is required"
    exit 1
fi

if [[ "$INPUT_DIR" = "" ]]; then
    echo "INPUT_DIR is required"
    exit 1
fi

INPUT_FILES=$(mktemp)
if [[ -f "$INPUT_DIR" ]]; then
    echo "$INPUT_DIR" > "$INPUT_FILES"
elif [[ -d "$INPUT_DIR" ]]; then
    find "$INPUT_DIR" -type f > "$INPUT_FILES"
else
    echo "-i \"$INPUT_DIR\" is neither file nor directory"
    exit 1
fi

NUM_INPUT=$(wc -l "$INPUT_FILES" | awk '{print $1}')
if [[ $NUM_INPUT -lt 1 ]]; then
    echo "There are no files to process."
    exit 1
fi

echo "I will process NUM_INPUT \"$NUM_INPUT\" files"
cat -n "$INPUT_FILES"

while read -r FILE; do
    sh change_bad_chars_to_ns.sh $FILE $WORK_DIR
    NEW_FILE="${WORK_DIR}/$(basename $FILE).no_bad_chars"
    python3 generate_seqs_fasta.py -s $STEP -k $KMER -infile $NEW_FILE -w $WORK_DIR
    NEW_FILE="${WORK_DIR}/$(basename $FILE)"
    sh glove.sh -i $NEW_FILE -k $KMER -s $STEP
done < "$INPUT_FILES"

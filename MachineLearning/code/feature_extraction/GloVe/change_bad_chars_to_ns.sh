INPUT_FILE=$1
OUT_DIR=$2
OUT_FILE="$OUT_DIR/$(basename $INPUT_FILE).no_bad_chars"
> $OUT_FILE
COUNT=0
while read -r LINE; do
    if [ $COUNT -eq 1 ]; then
        echo "$LINE" | sed 's/[R,Y,S,W,K,M,B,D,H,V]/N/g' >> ${OUT_FILE}
        COUNT=0
    else
        COUNT=1
    fi
done < $INPUT_FILE

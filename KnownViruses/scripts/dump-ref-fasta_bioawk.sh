cat wgs_datasets_ERR10_2.txt | while read LINE ; do 
dump-ref-fasta -l /data/realign/$LINE.realign | bioawk -c fastx '{ if(length($seq) > 1000) { print ">"$name; print $seq }}' > $LINE.1000bp.fasta ; 
done

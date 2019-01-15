mkdir ref_virus_blastout ; 
cat wgs_datasets.agree.rand3000.txt | while read SRR_NUM ; do 
dump-ref-fasta -l /data/realign/$SRR_NUM.realign | bioawk -c fastx '{ if(length($seq) > 1000) { print ">"$name; print $seq }}' | blastn -db ref_viruses_rep_genomes_v5 -evalue 0.001 -num_alignments 1 -num_threads 32 -outfmt "6 qseqid qlen sacc staxids sscinames slen pident evalue bitscore length" -out ref_virus_blastout/$SRR_NUM.blastout; 
done

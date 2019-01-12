#!/bin/bash

# Usage: $ ./director.sh
# This script directs the usage of VIGA by making use of parallel
# It parallelises all different fasta files with target contigs and runs VIGA pipeline single threaded for each one of them

parallel '      name=$(basename {} | sed "s/\.fasta//g")
		mkdir result/${name}
		cp run-viga result/${name}
		cp modifiers.txt result/${name}
		cp ${name}.fasta result/${name}
		cd result/${name}
		./run-viga --input ${name}.fasta --diamonddb /data/databases/RefSeq_Viral_DIAMOND/refseq_viral_proteins.dmnd --blastdb /data/databases/RefSeq_Viral_BLAST/refseq_viral_proteins --rfamdb /data/databases/rfam/Rfam.cm --hmmerdb /data/databases/pvogs/pvogs.hmm --threads 1 --modifiers modifiers.txt
		python /home/tully.bj/genbankfeature.py ${name}_annotated.gbk
		perl /home/tully.bj/unmapvigaannotations3.pl ${name}.fasta ${name}_annotated.fasta ${name}_annotated.csv ${name}_annotated_rename.csv ${name}_annotated.protein.faa ${name}_annotated.protein_rename.faa
		python /home/tully.bj/addvq.py ${name}_annotated_rename.csv ViralQuotient.txt ${name}_annotated_rename_vq.csv
		python /home/tully.bj/converter.py -i ${name}_annotated_rename_vq.csv -o ${name}_annotated_rename_vq.json


' ::: $(ls *.fasta)

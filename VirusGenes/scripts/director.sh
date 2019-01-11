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
		perl <working-dir>unmapvigaannotations.pl ${name}_annotated.csv ${name}.fasta ${name}_annotated_rename.csv
		python <working-dir>genbankfeature.py ${name}_annotated.gbk
		perl <working-dir>unmapvigaannotations2.pl ${name}_annotated.protein.faa ${name}.fasta ${name}_annotated_rename.protein.faa
		python <working-dir>addvq.py ${name}_annotated_rename.csv ViralQuotient.txt ${name}_annotated_rename_vq.csv
		python <working-dir>converter.py -i ${name}_annotated_rename_vq.csv -o ${name}_annotated_rename_vq.json


' ::: $(ls *.fasta)

#/bin/bash

#docker run -a stdout  --rm  -it -v /novel:/novel christiam/sra-toolkit:latest align-info /novel/datasets/no_phage_selection/ERR1913918.realign 
srr_dir=$1
srr=$2.realign
fasta=$2.fa
host_dbdir=/mmseqdbs

echo -n "" >  $fasta

for i in $(docker run -a stdout --rm -it -v $srr_dir:$srr_dir christiam/sra-toolkit:latest align-info $srr_dir/$srr | cut -d, -f1)
  do
	 docker run -a stdout  --rm  -it -v $srr_dir:$srr_dir christiam/sra-toolkit:latest dump-ref-fasta   $srr_dir/$srr $i >> $fasta
  done 
docker run --rm -v ${PWD}:${PWD}  -v ${host_dbdir}:${host_dbdir} mmseqs2 mmseqs createdb ${PWD}/$fasta  $host_dbdir/$2

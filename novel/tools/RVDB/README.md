# RVDB


```bash

/home/joan.marti.carreras/bin/prodigal -i SRR918250.realign.local.unknowns.fasta -a SRR918250.realign.local.unknowns.prodigal.genes.faa -g 11 -s SRR918250.realign.local.unknowns.prodigal.genes.txt -d SRR918250.realign.local.unknowns.prodigal.genes.fasta -o SRR918250.realign.local.unknowns.prodigal.genes.out &

hmmscan --noali -E 0.01 --domE 0.01 --cpu 32 -o test/SRR918250.realign.local.unknowns.RVDB.out --tblout test/SRR918250.realign.local.unknowns.RVDB.tblout --domtblout test/SRR918250.realign.local.unknowns.RVDB.domtblout --pfamtblout test/SRR918250.realign.local.unknowns.RVDB.pfamtblout databases/RVDB/U-RVDBv14.0-prot-new.hmm test/SRR918250.realign.local.unknowns.prodigal.genes.faa &
        ## 40 min aprox

./RVDB2LCA.sh

```

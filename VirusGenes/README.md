# Virus Genes 

## Ab initio gene predition

Use prodigal for provisional gene annotation:

```bash

bin/prodigal -i DRR128724.realign.local.fa -a prodigal/DRR128724.realign.local.prodigal.11.meta.faa -d prodigal/DRR128724.realign.local.prodigal.11.meta.fna -s prodigal/DRR128724.realign.local.prodigal.11.meta.txt -g 11 -o prodigal/DRR128724.realign.prodigal.11.meta.fa

```

See results in GitHub folder `prodigal/` in this team.


## HMM annotation

Both pVOG and RVDB hidden-Markov models will be used to annotate our contigs.

```bash

hmmscan -o pVOGs/DRR128724.realign.local.prodigal.11.meta.out --tblout pVOGs/DRR128724.realign.local.prodigal.11.meta.tblout --cpu 32 /novel/databases/pVOGs/all_vogs.hmm prodigal/DRR128724.realign.local.prodigal.11.meta.faa &
hmmscan -o RVDB/DRR128724.realign.local.prodigal.11.meta.out --tblout RVDB/DRR128724.realign.local.prodigal.11.meta.tblout --cpu 32 /novel/databases/RVDB/U-RVDBv14.0-prot-new.hmm prodigal/DRR128724.realign.local.prodigal.11.meta.faa &

```

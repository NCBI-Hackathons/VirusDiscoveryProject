# VirusDiscoveryProject
Software, architecture, and data index design for the 2018/2019 Virus Discovery Project

## Here we present a compromise pipeline for extracting virological information from publicly available metagenomic datasets, in order to present a usable index to the virological research community.  

# Look at the cool new sh*& NCBI built for us!

## NCBI Blast Docker:

### https://github.com/ncbi/docker/blob/blast2.8.1/blast/README.md

##### Theres also a nice cookbook here, with thanks to @christiam!

### GS Blast dbs

#### BLAST Databases currently being updated to the NIH STRDES GCP bucket (gs://blast-db/)

##### nr, nt, etc.  

##### Virus specific ones!

ref_viruses_rep_genomes_v5	Subset of refseq_genomes “latest_refseq[Prop] AND viruses[Organism]”	

ref_viroids_rep_genomes_v5	Subset of refseq_genomes “latest_refseq[Prop] AND viroids[Organism]”	

NCBI_VIV_protein_sequences_v5	nr	Sergey Resenchuk supplied GI list	

NCBI_VIV_nucleotide_sequences_v5	nt	Sergey Resenchuk supplied GI list	

#### CONTIGS!

##### Available from <>

##### Accessible using SRA toolkit

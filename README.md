# VirusDiscoveryProject
Software, architecture, and data index design for the 2018/2019 Virus Discovery Project

## Here we present a compromise pipeline for extracting virological information from publicly available metagenomic datasets, in order to present a usable index to the virological research community.  

# Look at the cool new sh*& NCBI built for us!

### https://github.com/ncbi/docker/blob/blast2.8.1/blast/README.md

### GS Blast dbs

#### BLAST Databases currently being updated to the NIH STRDES GCP bucket (gs://blast-db/)



##### Virus specific ones!

ref_viruses_rep_genomes_v5	Assembly Entrez	Entrez query: "latest_refseq[Prop] AND viruses[Organism]”	Subset of refseq_genomes, but also exists as a standalone BLASTDB
ref_viroids_rep_genomes_v5	Assembly Entrez	Entrez query: “latest_refseq[Prop] AND viroids[Organism]”	Subset of refseq_genomes, but also exists as a standalone BLASTDB
NCBI_VIV_protein_sequences_v5	nr	Sergey Resenchuk supplied GI list	
NCBI_VIV_nucleotide_sequences_v5	nt	Sergey Resenchuk supplied GI list	

#### Virus specific BLAST dbs

#### CONTIGS!


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

1. ref_viruses_rep_genomes_v5 
  * Virus RefSeq; Reference Viral sequences
  * Entrez query - “latest_refseq[Prop] AND viruses[Organism]”

2. ref_viroids_rep_genomes_v5	
  * Viroid RefSeq; Reference Viroid Sequences 
  * Entrez Query - “latest_refseq[Prop] AND viroids[Organism]”

3. NCBI_VIV_protein_sequences_v5	
  * Proteins from coding-complete, genomic viral sequences
  * Equivalent to protein records in https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus/Vira%252C%2520taxid%253A10239

4. NCBI_VIV_nucleotide_sequences_v5	
  * Coding-complete, genomic viral sequences
  * Equivalent to nucleotide records in https://www.ncbi.nlm.nih.gov/labs/virus/vssi/#/virus/Viruses%252C%2520taxid%253A10239

#### CONTIGS!

##### XXXnumber are available from <>

###### gsutil -m ls gs://ncbi_sra_realign/*.realign -- about 300K datasets with contigs so far -- will be public soon!

##### Accessible using SRA toolkit with remote-fuser/fusera <Documentation Needed>
 




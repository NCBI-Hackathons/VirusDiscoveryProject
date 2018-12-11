# VirusDiscoveryProject
Software, architecture, and data index design for the 2018/2019 Virus Discovery Project

## Here we present a compromise pipeline for extracting virological information from publicly available metagenomic datasets, in order to present a usable index to the virological research community.  

# Teams and Objectives (See Project Kanban Boards):

### “Known Virus Index” Matching contigs to known viruses
     Determining a heuristic for what is a “known” virus
### Detecting recombination and variation from/in known viruses
### Determination of phylogenetic position of viruses similar to knowns
### Detection of novel contigs and novel viruses
### Containerization, distribution, and contribution mechanism + Scaling
### User interface (likely Jupyter notebooks)

# Look at the cool new sh*& NCBI built for us!

## NCBI Blast Docker:

### https://hub.docker.com/r/ncbi/blast/

## BLAST workbench docker (+magicBLAST, +EDirect) -- beta

### https://hub.docker.com/r/ncbi/blast-workbench/

## NCBI_Powertools (+ sra toolkit)

##### Theres also a nice cookbook here, with thanks to @christiam!

### BLAST databases

BLAST Databases currently being updated to the NIH STRIDES GCP bucket
and can be obtained via [update_blastdb.pl][getting-blastdbs-documentation] or
obtained pre-configured via the BLAST GCP VM.

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
 


[getting-blastdbs-documentation]: https://www.ncbi.nlm.nih.gov/books/NBK532645/

# VirusDiscoveryProject
Software, architecture, and data index design for the 2018/2019 Virus Discovery Project

## Here we present a compromise pipeline for extracting virological information from publicly available metagenomic datasets, in order to present a usable index to the virological research community.  

# Objectives (See Project Kanban Boards):

## Known Virus Index

content here

Presentation here - https://docs.google.com/presentation/d/1NGXwqCb5mgfOGq4jqpiK5cjHoW48sMGTLPX0IglHIOE/edit?usp=sharing
    
## Detection of novel contigs and novel viruses

Presentation  here - https://docs.google.com/presentation/d/1U9_ryV0uzO0VXC77vzhur2lJmBunA4F5aNSmhQXrgJU/edit#slide=id.g4a4e9be9b9_41_11

## Scaling: Containerization, distribution, and user interface + contribution mechanism?

Presentation here - https://docs.google.com/presentation/d/1ESJwy6Wkh6VH0SD-vVEA4gjVYbkh0R1ynuQ8E_ZoO_s/edit?usp=sharing

## Test Data Selection

### <links to content>

### Detecting recombination and variation from/in known viruses
### Determination of phylogenetic position of viruses similar to knowns


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

## SRA realign project

SRA public metagenome data has been aligned and assembled in Google cloud and the results are stored in the bucket gs://ncbi_sra_realign/.
The project is an ongoing activity and as of the 12/11/2018 there is almost 150000 realigned runs available for the hackathon. 

The URLs to individual files can be built using SRA run accession, for example:
gs://ncbi_sra_realign/ERR2227558.realign

Here is an example how to download a realigned file:
gsutil cp gs://ncbi_sra_realign/ERR2227558.realign .

To list all realign file:
gsutil -m ls gs://ncbi_sra_realign/*.realign

SRA toolkit provides means to read the data stored in realigned files. For example, to view references: 
align-info ERR2227558.realign

To extract a contig by name:
dump-ref-fasta ERR2227558.realign Contig_100000_4.78977

To dump reads in fasta format:
fastq-dump -Z --fasta ERR2227558.realign Contig_100000_4.78977 | head


## Realign metadata
For the duration of the hackathon additional information is available in BigQuery: coverage, contig taxonomy and summary with breakdown of host/viral/denovo/unmapped reads.
Please note that the processing is still ongoing, so the numbers provided are not final. 

Some BigQuery examples:
* number of available SRA runs (133200):
  `select count(distinct accession) from ncbi_sra_realign.coverage`

* number of guided contigs (274928):
  `select count(1) from ncbi_sra_realign.coverage where contig not like 'Contig_%' and REGEXP_CONTAINS(contig, '_[[:digit:]]$') `

* number of denovo contigs (2674975354):
  `select count(1) from ncbi_sra_realign.coverage where contig like 'Contig_%'`

* number of SRA runs with available contig taxonomy (100):
  `select count(distinct accession) from  ncbi_sra_realign.taxonomy`


[getting-blastdbs-documentation]: https://www.ncbi.nlm.nih.gov/books/NBK532645/

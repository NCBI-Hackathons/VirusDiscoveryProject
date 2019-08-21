# VirusDiscoveryProject
Software, architecture, and data index design for the 2018/2019 Virus Discovery Project

![exaple plot from indexed results](https://github.com/NCBI-Hackathons/VirusDiscoveryProject/blob/master/updated_coverage_v_length.PNG "contig length v. coverage")


# Publication

The initial results and learned lessons have been compiled into a manuscript
currently under review. The following layout indicates the directories
containing the material related to this publication and the related
sections within.

```
.
|-- DarkMatter1         3.5 Domain Mapping / 3.6 Gene Annotation
|-- DataSelection       3.2 Data Selection
|-- DomainLabeling      3.4 Data Clustering / 3.5 Domain Mapping
|-- KnownViruses        3.3 Data Segmentation / 3.5 Domain Mapping
|-- MachineLearning     3.7 Metadata Analysis
`-- Phylo               3.4 Data Clustering
```

## Here we present a compromise pipeline for extracting virological information from publicly available metagenomic datasets, in order to present a usable index to the virological research community.

# Objectives (See Project Kanban Boards):

## Known Virus Index

Presentation here - https://docs.google.com/presentation/d/1NGXwqCb5mgfOGq4jqpiK5cjHoW48sMGTLPX0IglHIOE/edit?usp=sharing

The 'Knowns' portion of the VirusDiscovery pipeline processes data from the guided assembly database to sort for virus-like contigs. Specifically, contigs are processed with BLASTN, sorting for an average nucleotide identity ('ANI') of greater than 80% or other defined cutoff. For contigs identified as viral, an index entry is generated as below.

Index for 'Known' viral contigs:
- Metagenome SRR accession [string]
- Contig name [string]
- Assembly type [denovo, reference guided]
- Median depth of coverage by reads of contig [int]
- Length [int]
- Covered length from hit [int]
- NCBI taxonomy id by kmer [int]
- NCBI taxonomic species by kmer [string]
- Unique kmer hits [int]
- Species for reference-guided assembly [string]
- Accession for subject in blastn [string]
- NCBI taxonomy id for subject in blastn [string]
- Percent idendity of blastn hit [float]
- Evalue of blastn hit [float]
- Bit score of blastn hit [float]
- Length of blastn hit [int]

We assume that the contigs db will remain as part of the VirusDiscoveryProject Index ('VDPI') and that indices to that db will be adequate for access rather than having to store individual contigs with the VDPI. This contig db is assumed to include metagenome accession IDs. From those IDs search can make available access to other desirable data features, as provided in the NCBI Virus DB, such as species, source material, country of origin, etc. so we need not provide such information.

The Knowns pipeline generates a possible taxonomic level based on more 85% ANI and more than 80% of coverage by blastn hit and provides that in the index. We propose that there also be entries allowing for expert curation when and if any occurs. The auto-generated taxonomic identity id simply derived from the best blastn hit.

Contigs that have an ANI and coverage lower than the cutoff are sorted and their indices are provided to the Novel Virus processing pipeline.


## Detection of novel contigs and novel viruses

Presentation  here - https://docs.google.com/presentation/d/1U9_ryV0uzO0VXC77vzhur2lJmBunA4F5aNSmhQXrgJU/edit#slide=id.g4a4e9be9b9_41_11

## Scaling: Containerization, distribution, and user interface + contribution mechanism?

Presentation here - https://docs.google.com/presentation/d/1ESJwy6Wkh6VH0SD-vVEA4gjVYbkh0R1ynuQ8E_ZoO_s/edit?usp=sharing

## Test Data Selection

### <links to content>

### Detecting recombination and variation from/in known viruses
### Determination of phylogenetic position of viruses similar to knowns


# Look at what NCBI built for us!

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

All reads from an SRR archive were aligned  against the human genome reference sequence (GRCh38.p12) using HISAT2 (--no-spliced-alignment --no-discordant
guidedassembler_graph options: --extend_ends  --word 11 --seed_prec 6 --min_hit_len 1000  --fraction 0.1 --no_filter_by_reads --no_filter_by_pairs)


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

# Conclusions

### Premature scaling is the root of all evil.
## Diversity of test data -- and by extension, real data -- is critical
## Reference sets are critical and must be large, diverse and accurate
#### They also must be dynamic and grow quickly
## Massive datasets may be able to dynamically reduce unknown space
### i/o is a huge limitation, even in cloud
#### Permission and access issues can be a huge limitations
#### Networks of fast databases dynamically created from stable databases may be the optimal structure for serving disparate use cases
### Communication between data generators and processors is ideally (initially) done in person
#### If it can’t be communicated, the (meta)datasets and toolsets should not exist.
### All meta-analysis should be done on exactly the same set
## Domain profiles have immense potential for sorting things in massive datasets
#### They should be treated as first-class reference objects
#### A massive expansion of these data objects (computationally) may be the most effective way to expand into new data spaces
### Contigs are much more popular than reads with the participants here.  Knowing which reads map to those contigs is also helpful
### Easy-to-use ensemble-method pipelines are critical for rapid implementation
### Theoretical calculations are no replacement for experiencing fast compute first-hand
## Clean metadata on metagenomes is really important
#### Motivation to work hard on a dataset
#### When we spend time curating datasets we should work on the ones with the most metadata
## It is easier to make novel discoveries from a homogenous information space.

# Want to be a part of this:

## https://biohackathons.github.io

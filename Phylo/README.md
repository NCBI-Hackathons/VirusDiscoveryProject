
# Clustering and Phylogeny
This part of the ViralDiscoveryProject aims to answer the question: **How are these new contigs related to known viruses and each other**?

This is done through a simple and full clustering processes aimed at determining the relationships between the contigs, through MMSeq2 and Blast analyses (*Figure 1*).

![alt text](https://raw.githubusercontent.com/NCBI-Hackathons/VirusDiscoveryProject/master/Phylo/Phylo_summary.jpg)

*Figure 1. Overall methodology for phylogenetic analyses.*

## 'Simple' Clustering using MMSeq2
The goal of this section is to provide the simplest answer to users who are searching through the database, find a putative virus they're interested in, and wonder: "Are there any similar contigs?" 

Each contig will be assigned to a single cluster, and each cluster will be represented by one "representative contig".  Often times a contig will be the "representative contig" in its own cluster. We colloquially refer to these as 'lonely contigs'.

| Cluster Representative Sequence | Sequence in Cluster |
|----------------------------------------|--------------------------------------------------------|
| NC_027054_Porcine_kobuvirus | NC_027054_Porcine_kobuvirus |
| NC_027054_Porcine_kobuvirus | NC_011829_Porcine_kobuvirus_swine/S-1-HUN/2007/Hungary |
| NC_027054_Porcine_kobuvirus | NC_016769_Porcine_kobuvirus_SH-W-CHN/2010/China |
| NC_018226_Pasivirus_A1 | NC_018226_Pasivirus_A1 |
| NC_016156_Feline_picornavirus | NC_016156_Feline_picornavirus |
| NC_001479_Encephalomyocarditis_virus | NC_001479_Encephalomyocarditis_virus |
| NC_010810_Human_TMEV-like_cardiovirus | NC_010810_Human_TMEV-like_cardiovirus |
| NC_010810_Human_TMEV-like_cardiovirus | NC_009448_Saffold_virus |
| NC_038306_Coxsackievirus_A2 | NC_038306_Coxsackievirus_A2 |
| NC_015936_Mouse_kobuvirus_M-5/USA/2010 | NC_015936_Mouse_kobuvirus_M-5/USA/2010 |
| NC_022332_Eel_picornavirus_1 | NC_022332_Eel_picornavirus_1 |
| NC_024765_Chicken_picornavirus_1 | NC_024765_Chicken_picornavirus_1 |
| NC_024765_Chicken_picornavirus_1 | NC_028380_Chicken_sicinivirus_JSY |
| NC_024768_Chicken_picornavirus_4 | NC_024768_Chicken_picornavirus_4 |
| NC_024768_Chicken_picornavirus_4 | NC_023858_Melegrivirus_A |
| NC_024768_Chicken_picornavirus_4 | NC_021201_Turkey_hepatitis_virus_2993D |


## Full Clustering using BLASTN
Here we aim to cluster all contigs and all refseq viruses (again) but extract actual edge weights between the nodes in the cluster. This will be done using blastn and extracting the top non-self hit. If a virus has no non-self hits, it's 'lonely' and wont show up to the graph.

Clustering and networks are generated with Gephi or Japek (although other software can be employed). Two nodes will have an edge if a blast result was obtained (with the e-value established below). The weight of the graph will be equal to be bit score for the alignment.

## Commands and Scripts
### blastn:
`blastn -query known_knowns.fasta -db known_knowns.fasta -out known_knowns.blastn -num_threads 96 -outfmt 7 -evalue 1e-10 -max_hsps 1`
### blast_pairs.py
This script extracts three columns from the blastn output, the three columns are:
Contig1  |  Contig2  |  bit score
`python3 blast_pairs.py -i example_files/knowns.blastn -o example_files/example_blast_paris.tsv`
### fasta_duplicator.py
This script duplicates entries in a fasta file *n* times. Every header will have the value of *n* insterted in the header. For example, with *n* = 3, ">seq1"   will become  >0seq1  >1seq1  >2seq1
`fasta_duplicator.py -i example_files/test_contigs.fasta -o example_files/dup_contigs.fasta -n 3`

### longest_in_cluster.py
This script has two functions. 
First, it can rename the representative sequence of a cluster to the longest (bp) sequence in the cluster. This prevents clusters from being named after a small contig.

`python3 longest_in_cluster.py -f example_files/test_contigs.fasta -c example_files/test_clusters.tsv -o example_files/newclusters.tsv`

Second, it can write a new FASTA file of only the longest sequence in each cluster. **This is done with the "-e" flag**

`python3 longest_in_cluster.py -f example_files/test_contigs.fasta -c example_files/test_clusters.tsv -o example_files/newclusters.tsv -e`

###  blastnToGraph.tar.gz 
This tar file contains the scripts required for running the full clustering blastn pipeline, starting from a multifasta and generating files which can be later plugged to network analysis software. The process involves generating a blast database for the multifasta (`makeblastdb`) and blasting the sequences against themselves (`blastn`). Then, using custom scripts (see below) self hits are removed and the blast output is formated to generate both a tsv file with pairwirse distances between sequences and a complete distance matrix. The bitscore of the blast alignments is used as the distance criteria. The tsv file and distance matrices produced can be loaded to network analysis software (e.g.: Gephi, Cytoscape, or Pajek). 

To run the pipeline, untar the file and execute the master script (blastnToGraph, see below). Results will be placed inside the blastPipeline/results directory, including the blast database (`testDB`), blast results (`results.blastn`), tsv and distance matrix files (`blast_pairs.tsv` and `disMat.csv` respectively).

The customs scripts for the pipeline are described below in order of usage:

#### blastnToGraph.sh
General script for the pipeline. Carries out all of the processes. Syntax is as follows:

`bash blastToGraph.sh <input_file.fasta> <e-value> <minimum_identity>`

Where e-value and minimum identity correspond to the options -evalue and -perc_identity in blastn. The resulting files (blast dabatase, blastn results, and distance matrix) will be located in the results directory. Other parameters of blast can be tweaked inside the script.

#### blast_pairs.py
As described above.

#### toMatrix.py
Generates the distance matrix from the csv file. Syntax is:

`python3 toMatrix.py blast_pairs.tsv`

Where `blast_pairs.tsv` is the output of the blast_pairs.py command (name can be changed inside `blastnToGraph.sh`). Generates a csv file, `disMat.csv` with the bitscore between all contigs. Contigs with no hits reported in the blastn have their distance set to 0.

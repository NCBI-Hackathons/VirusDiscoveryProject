
# Clustering and Phylogeny
This part of the ViralDiscoveryProject aims to answer the question: **How are these new contigs related to known viruses and each other**?

This is done through a simple and full clustering processes aimed at determining the relationships between the contigs, through MMseqs2 and Blast analyses (**Figure 1**).

![alt text](https://raw.githubusercontent.com/NCBI-Hackathons/VirusDiscoveryProject/master/Phylo/Phylo_summary.jpg)

**Figure 1. Overall methodology for phylogenetic analyses.**

## 'Simple' Clustering using MMseqs2

MMseqs2 is needed for this part of the pipeline, see:

https://github.com/soedinglab/MMseqs2

The goal of this section is to provide the simplest answer to users who are searching through the database, find a putative virus they're interested in, and wonder: "Are there any similar contigs?"

This is achieved by clustering all presumed-to-be viral contigs together with all sequences currently present in virus refseq. Each contig will be assigned to a single cluster, and each cluster will be represented by one "representative contig". This “representative contig” is the refseq sequence present in the cluster or, if there is none, the longest sequence in the cluster. Often times a contig will be the "representative contig" in its own cluster. We colloquially refer to these as 'lonely contigs'.

First, contigs of interested are joined with a fasta-file containing all virus refseq entries (downloaded from NCBI GenBank using (viruses[orgn] NOT bacteria [orgn]) and (refseq) as keywords.)

`cat <contigs.fasta> <virus_refseq.fasta> > <fullset.fasta>`

Then, a database is built.

`mmseqs createdb <fullset.fasta> <fullset_DB> --dbtype 2`

Clustering is done using the linclust algorithm:

`mmseqs linclust <fullset_DB> <out_DB> <tmp_dir> --sub-mat nucleotide.out --alph-size 4 -c 0.1 --min-seq-id 0.85 -e 1e-10 --alignment-mode 4`

use createtsv to convert the output to .tsv

`mmseqs createtsv <fullset_DB> <fullset_DB> <out_DB> <out_DB.tsv>`

The clusters are then renamed if they contain a known RefSeq virus. An example of this is shown below, the full data is available [here](https://github.com/NCBI-Hackathons/VirusDiscoveryProject/blob/master/Phylo/example_files/kk_ku_ref_outDB2.tsv). The command used to rename a cluster is:
`python3 longest_in_cluster.py -c example_files/test_clusters.tsv -o example_files/newclusters.tsv`



| Cluster Representative Sequence | Contig in Cluster |
|------------------------------------------|-----------------------------------------|
| SRR6659405_Contig_237_223.049:1.3224 | SRR6659405_Contig_237_223.049:1.3224 |
| SRR6659405_Contig_237_223.049:1.3224 | SRR6659597_Contig_1523_15.6439:1.3224 |
| SRR6659405_Contig_237_223.049:1.3224 | SRR6659435_Contig_5949_81.708:1.2547 |
| SRR6659405_Contig_237_223.049:1.3224 | ERR1711665_Contig_47824_41.9819:1.1128 |
| NC_001609.1 | NC_001609.1 |
| NC_001609.1 | SRR7524180_Contig_2887_4.15617:1.8613 |
| NC_001609.1 | SRR6028274_Contig_14203_56.7802:1.11362 |
| NC_001609.1 | SRR4101292_Contig_16607_60.2093:1.3030 |
| NC_001609.1 | ERR2749714_Contig_151_21.3722:1.2535 |
| NC_001609.1 | SRR4101324_Contig_236_136.623:1.3030 |


## Full Clustering using BLASTN
Here we aim to cluster all contigs and all refseq viruses (again) but extract actual edge weights between the nodes in the cluster. This will be done using blastn and extracting the top non-self hit. If a virus has no non-self hits, it's 'lonely' and wont show up to the graph.

Clustering and networks are generated with Gephi or Pajek (although other software can be employed). Two nodes will have an edge if a blast result was obtained (with the e-value established below). The weight of the graph will be equal to be bit score for the alignment.

## Commands and Scripts
### blastn:
`blastn -query known_knowns.fasta -db known_knowns.fasta -out known_knowns.blastn -num_threads 96 -outfmt 7 -evalue 1e-10 -max_hsps 1`
### blast_pairs.py
This script extracts three columns from the blastn output, the three columns are:
Contig1  |  Contig2  |  bit score
`python3 blast_pairs.py -i example_files/knowns.blastn -o example_files/example_blast_paris.tsv`
### fasta_duplicator.py
This script duplicates entries in a fasta file *n* times. Every header will have the value of *n* inserted in the header. For example, with *n* = 3, ">seq1"   will become  >0seq1  >1seq1  >2seq1
`fasta_duplicator.py -i example_files/test_contigs.fasta -o example_files/dup_contigs.fasta -n 3`

### longest_in_cluster.py
This script has two functions. 
First, it can rename the representative sequence of a cluster to the longest (bp) sequence in the cluster. This prevents clusters from being named after a small contig.

`python3 longest_in_cluster.py -f example_files/test_contigs.fasta -c example_files/test_clusters.tsv -o example_files/newclusters.tsv`

Second, it can write a new FASTA file of only the longest sequence in each cluster. **This is done with the "-e" flag**

`python3 longest_in_cluster.py -f example_files/test_contigs.fasta -c example_files/test_clusters.tsv -o example_files/newclusters.tsv -e`

###  blastnToGraph.tar.gz 
This tar file contains the scripts required for running the full clustering blastn pipeline, starting from a multifasta and generating files which can be later plugged to network analysis software. The process involves generating a blast database for the multifasta (`makeblastdb`) and blasting the sequences against themselves (`blastn`). Then, using custom scripts (see below) self hits are removed and the blast output is formatted to generate both a tsv file with pairwise distances between sequences and a complete distance matrix. The bitscore of the blast alignments is used as the distance criteria. The tsv file and distance matrices produced can be loaded to network analysis software (e.g.: Gephi, Cytoscape, or Pajek). 

To run the pipeline, untar the file and execute the master script (blastnToGraph, see below). Results will be placed inside the blastPipeline/results directory, including the blast database (`testDB`), blast results (`results.blastn`), tsv and distance matrix files (`blast_pairs.tsv` and `distMat.csv` respectively).

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

Where `blast_pairs.tsv` is the output of the blast_pairs.py command (name can be changed inside `blastnToGraph.sh`). Generates a csv file, `ditMat.csv` with the bitscore between all contigs. Contigs with no hits reported in the blastn have their distance set to 0.

## Results from Sample Data
Contigs clustered are available in the example_clusters.tsv. The largest 10 clusters are displayed below (if a known refseq virus is in the cluster, then the cluster is named with the refseq accession.)

| NC_001422.1 | 209 |
|----------------------------------------|-----|
| SRR4101321_Contig_99_104.661:1.2144 | 164 |
| SRR6659424_Contig_425_59.3234:1.1631 | 137 |
| ERR1711614_Contig_36997_17.9674:1.3762 | 136 |
| SRR6659585_Contig_718_60.183:1.19044 | 130 |
| NC_026014.1 | 127 |
| SRR6659538_Contig_420_96.6643:1.1709 | 122 |
| SRR1490934_Contig_145_68.9628:1.1957 | 116 |
| SRR6659449_Contig_11442_1446.67:1.3897 | 109 |
| ERR1308128_Contig_292_17.1635:1.1561 | 108 |

The results were 13,173 clusters with 239 of them containing at least 10 contigs.

|Title|numbers|
| ------------------------- | ------ |
| # of clusters             | 13,173 |
| # of singleton clusters   | 11,120 |
| # of non-singleton clusters  | 2,053 |
| # of singleton refseq-clusters  | 8,333 |
| # of non-singleton that have refseq-clusters  | 1,013 |
| # of non-singleton that have no refseq-clusters  | 998 |

Below we show a visualization of the diversity of cluster sizes. This dataset contains only the known-known and known-unknown contigs, it does not contain refseq viruses or unknown-unknown contigs (contigs that are likely bacterial). This figure was made using [Pajek](http://mrvar.fdv.uni-lj.si/pajek/) and the labeling was added manually. 
![examplenpng](https://github.com/NCBI-Hackathons/VirusDiscoveryProject/blob/master/Phylo/example_files/kk_ku_no_refseq_labelled.jpg)

The next figure is an example of the results of [Gephi](https://gephi.org/) clustering the blastn results. Bigger nodes have a higher weighted grade. Communities with high modularity are coloured.
![examplenpng](https://github.com/NCBI-Hackathons/VirusDiscoveryProject/blob/master/Phylo/example_files/finalNet_Clust.png)






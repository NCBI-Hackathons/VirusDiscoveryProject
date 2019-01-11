
**Input data from NCBI SRR**


**_De novo_ and reference-guided assembly**

[SKESA](https://github.com/ncbi/SKESA) is a sequence read assembler for microbial genomes based on debruijn graphs. It uses conservative heuristics for *de novo* and refenrece guided assembly. SKESA can process read information by accessing reads from SRA (option --sra_run) or from files in fasta (option --fasta) or fastq (option --fastq) format. Any combination of input streams is allowed.

**Taxonomic assignment by kmer match**

STAT tool from NCBI was run on each contig from the skesa assembly
The web interface for STAT is available [here] (https://www.ncbi.nlm.nih.gov/Traces/sra_stat_search/). There is no command line version available at the moment but in the works.

STAT is used for the [taxonomic analysis](https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR4098608) of SRA accessions. You can get the tool from [Github](https://github.com/ncbi/ngs-tools/tree/tax/tools/tax)

**Taxonomic assignment blastn hit**

The commands to do the blastn of the assembled contigs against NCBI Refseq virus genomes database are:
```
for i in *.fa.gz; 
	do 
		gunzip -c $i | blastn -db ref_viruses_rep_genomes_v5 -evalue 0.001 -num_alignments 1 -num_threads 32 -outfmt "6 qseqid qlen sacc stitle slen pident evalue bitscore length" -out ${i%.fa.gz}.blastout.taxid.test; 
	done
```

Output is tab separated file in the following format:

| Contig name | Contig length | Blast hit acc | Blast hit name | Blast hit total length | % identity | evalue | Bit score | Length aligned to blast hit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Contig_805_73.4912:1.2127 | 2127 | NC_027339 | Enterobacteria phage SfI, complete genome | 38389 | 96.330 | 1.11e-42 | 178 | 109 |


**Features from the blastn hits**

Index for 'Known' viral contigs:
- Metagenome SRR accession [string]
- Contig name [string]
- Assembly type [denovo, reference guided]
- Median depth of coverage by reads of contig [int]
- Length [int]
- Covered length from hit [int]
- ~~Compressed size of realigned object in bytes [int]~~
- ~~Original size in bytes [int]~~
- ~~Ratio of compressed size / original size [float]~~
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

**Workflow**

![image](/KnownViruses/images/KnownVirusesWorkflow.png)


**Known virus data sets**

| Description | Count | Blastn length cutoff | Blastn identity cutoff | 
| --- | --- | --- | --- |
| Known knowns | 525,346 | >80% | >85% |
| Known unknowns | 64,309 | > 80% | >50% and <85% |
| Known unknowns | 104,154 | >50% to <80% | >85% |
| Unknown unknowns with blast hits| 1,351,557 | <50% | NA |
| Unknown unknowns without blast hits| 20,181,350 | NA | NA |

Output is provided in .CSV and .JSON formats. We also have FASTA for all these sets.

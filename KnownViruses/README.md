
**Input data from NCBI SRR**


***De novo* and reference-guided assembly**


**Taxonomic assignment by kmer match**


**Taxonomic assignment blastn hit**


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

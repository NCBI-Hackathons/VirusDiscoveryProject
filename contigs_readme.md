# Contigs ReadMe

## Description 

  Approximately 3.9 billion contigs were created to support the Virus Discovery Hackathon, coordinated by NCBI and hosted by SDSU on Jan 9, 2019 (10.3390/genes10090714). SRA data selection is described in the associated publication, but, briefly, runs were selected to enrich for WGS metagenomic studies likely to contain crassphage. Contigs were then assembled using SKESA (10.1186/s13059-018-1540-z). First, human reads were filtered out via HISAT2 (10.1038/nmeth.3317). Next, viral contigs were assembled via guided assembly. Finally, the remaining reads were assembled, if possible, via de novo assembly. How to access these contigs and the naming conventions used are described below. Additionally, descriptive metadata, of the contigs, and the associated biosample records was put in tabular format, with details on how to access this information included below as well. Currently the information is hosted in both Amazon and Google’s cloud environments, as reflected in the access instructions provided here.

**If publishing results which make use of these contigs please cite**: 
  Connor R, Brister R, Buchmann JP, et al. NCBI's Virus Discovery Hackathon: Engaging Research Communities to Identify Cloud Infrastructure Requirements. Genes (Basel). 2019;10(9)

## Contigs
	
  All the contigs derived from a single SRR are included in a single fasta file. The naming convention for these files is: `SRR_ACCESSSION.fa` 
  
  Within each fasta the definition line of each contig is constructed as follows: `SRR_ACCESSION.CONTIG_NAME.NUMBER` Where CONTIG_NAME can take one of two formats. For guided assemblies `RefSeqID_NUMBER`, and for de novo assemblies `Contig_AlphaNumeric.AlphaNumberic`

## Getting Data
	
  The contig sequences are available from GCP and AWS platforms. In general it is preferable to work from a machine in the same region the data is located.

### Google
	
  The bucket containing the data is experimental-sra-metagenome-contigs and it is located in us-east1.

**Examples of how the data might be accessed**:

`gsutil cp -r gs://experimental-sra-metagenome-contigs/ <dest>`

`wget https://storage.googleapis.com/experimental-sra-metagenome-contigs/DRR000019.contigs.fasta`

### Amazon

  The bucket containing the data is experimental-sra-metagenome-contigs and is located in us-east-1.

**Examples of how the data might be accessed**:
 
`aws s3 cp s3://experimental-sra-metagenome-contigs.s3.amazonaws.com/DRR000019.contigs.fasta <dest>`

`wget http://experimental-sra-metagenome-contigs.s3.amazonaws.com/DRR000019.contigs.fasta`

## Searching Metadata

Metadata associated with the contigs can be found in both GCP and AWS environments. The available metadata fields are outlined below. For blast related statistics, blastn was used and only viral targets were checked.

|field | description|
| ---- | ---- |
|accession | the accession for the SRR the contig is derived from|
|contig | the contig ID|
|defline | the defline seen in the associated fasta file|
|type | either guided_contig or denovo_contig|
|guide | the accession for the guide sequence if type is guided_contig|
|mean_coverage | average coverage for the contig|
|contig_length | contig length in bases|
|subject | accession for best blast hit|
|subject_taxid | taxid for best blast hit|
|subject_title | defline for best balst hit|
|pident | percent identity for best blast hit|
|evalue | evalue for best blast hit|
|bitscore | bitscore for best blast hit|
|alignment_length | alignment length for best blast hit|

### Google

  The metadata is loaded into BigQuery and can be accessed via the web console by pinning the project `research-sra-cloud-pipeline` and opening the dataset `realign` and looking at the table `experimental_sra_metagenome_contigs`

### Amazon

  The metadata is loaded into s3 and can be accessed via the Athena web console by creating a new database. First select query data in Amazon S3, then Add a table manually, then specify the location of the input data set as `s3://experimental-sra-metagenome-contigs-us-east-1/metadata/`, then select csv as the data format, then select bulk add columns and paste the field below intot he text box

```
  accession string,
  contig string,
  defline string,
  type string,
  guide string,
  mean_coverage float,
  contig_length int,
  subject string,
  subject_taxid int,
  subject_title string,
  pident float,
  evalue float,
  bitscore float,
  alignment_length int
```

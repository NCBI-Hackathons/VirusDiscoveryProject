
**Input data from NCBI SRR**


**_De novo_ assembly**

[SKESA](https://github.com/ncbi/SKESA) is a sequence read assembler for microbial genomes based on debruijn graphs. It uses conservative heuristics for *de novo* assembly. SKESA can process read information by accessing reads from SRA (option --sra_run) or from files in fasta (option --fasta) or fastq (option --fastq) format. Any combination of input streams is allowed.

**Realigned objects**

The realigned object is a compilation of human alignment, viral guided assembly or alignment, SKESA assembly and unmapped reads.

Realign objects are effectively the same reads (bases) as the original SRA runs but aligned onto host (human) and either viral contigs or references and onto *de novo* contigs assembled with SKESA. 


**Taxonomic assignment by kmer match**

STAT tool from NCBI was run on each realign sequence. The web interface for STAT is available [here] (https://www.ncbi.nlm.nih.gov/Traces/sra_stat_search/). There is no command line version available at the moment but in the works.

STAT is used for the [taxonomic analysis](https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR4098608) of SRA accessions. You can get the tool from [Github](https://github.com/ncbi/ngs-tools/tree/tax/tools/tax)


**Taxonomic assignment by HMM match**

**Taxonomic assignment by rpstblast match**

**Taxonomic assignment blastn hit**

The commands to do the blastn of the realigned sequences against NCBI Refseq virus genomes database are:
```
mkdir ref_virus_blastout
for i in *.fa.gz
	do il=$( echo $i | sed 's/.*\///g' )
		gunzip -c $i | bioawk -c fastx '{ if(length($seq) > 1000) { print ">"$name; print $seq }}' | blastn -db ref_viruses_rep_genomes_v5 -evalue 0.001 -num_alignments 1 -num_threads 32 -outfmt "6 qseqid qlen sacc staxid sscinames slen pident evalue bitscore length" -out ref_virus_blastout/${il%.fa.gz}.blastout
	done
```

Output is tab separated file in the following format:

| Contig name | Contig length | Blast hit acc | Taxon ID | Blast hit name | Blast hit total length | % identity | evalue | Bit score | Length aligned to blast hit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Contig_805_73.4912:1.2127 | 2127 | NC_027339 | 1732063 | Enterobacteria phage SfI, complete genome | 38389 | 96.330 | 1.11e-42 | 178 | 109 |


**Parse blastn hits for contigs in each class**

Generate list of contig names in the following classes

| Description | Blastn length cutoff | Blastn identity cutoff | 
| --- | --- | --- |
| Known knowns | >80% | >85% |
| Known unknowns | > 80% | >50% and <85% |
| Known unknowns | >50% to <80% | >85% |
| Unknown unknowns with blast hits | <50% | NA |


```
for blout in *.realign.local.blastout
	do 
		sort -u -k1,1 $blout | awk '{FS="\t"; OFS="\t"} {if ($10/$2 > 0.799 && $7 > 84.99) {print $1}}' > ${blout%.realign.local.blastout}.known_knowns_85id_80len.txt
		sort -u -k1,1 $blout | awk '{FS="\t"; OFS="\t"} {if ($10/$2 > 0.499 && $10/$2 < 0.8 && $7 > 84.99) {print $1}}' > ${blout%.realign.local.blastout}.known_unknowns_85id_50len.txt
		sort -u -k1,1 $blout | awk '{FS="\t"; OFS="\t"} {if ($10/$2 > 0.499 && $7 < 84.99 && $7 > 49.99) {print $1}}' > ${blout%.realign.local.blastout}.known_unknowns_50id_50len.txt
	done
```

Generate the fasta file for each class
```
for raw_fasta in /home/vpeddu/testing/*.fa.gz
	do 
		il=$( echo $raw_fasta | sed 's/.*\///g' )
		gunzip -c $raw_fasta | bioawk -c fastx '{ if(length($seq) > 1000) { print}}' > ${il%.realign.local.fa.gz}.temp.tab
		if [ -s ${il%.realign.local.fa.gz}.temp.tab ]
		then
			grep -f ${il%.realign.local.fa.gz}.known_knowns_85id_80len.txt ${il%.realign.local.fa.gz}.temp.tab | awk '{print ">"$1; print $2}' | sed '/--/d' > ${il%.realign.local.fa.gz}.known_knowns_85id_80len.fasta
			grep -f ${il%.realign.local.fa.gz}.known_unknowns_85id_50len.txt ${il%.realign.local.fa.gz}.temp.tab | awk '{print ">"$1; print $2}' | sed '/--/d' > ${il%.realign.local.fa.gz}.known_unknowns_85id_50len.fasta
			grep -f ${il%.realign.local.fa.gz}.known_unknowns_50id_50len.txt ${il%.realign.local.fa.gz}.temp.tab | awk '{print ">"$1; print $2}' | sed '/--/d' > ${il%.realign.local.fa.gz}.known_unknowns_50id_50len.fasta
			cat ${il%.realign.local.fa.gz}.known_unknowns_50id_50len.txt ${il%.realign.local.fa.gz}.known_unknowns_85id_50len.txt ${il%.realign.local.fa.gz}.known_knowns_85id_80len.txt > ${il%.realign.local.fa.gz}.legit_blasthits.txt
			grep -v -f ${il%.realign.local.fa.gz}.legit_blasthits.txt ${il%.realign.local.fa.gz}.temp.tab | awk '{print ">"$1; print $2}' | sed '/--/d' > ${il%.realign.local.fa.gz}.unknown_unknowns_refviral.fasta
		fi
	done
```

Create CSV for blastn hits

Known knowns 85id 80len
```
for KK in /home/michael.tisza/ref_virus_blast1/ref_virus_blastout/*.known_knowns_85id_80len.txt
	do 
		echo "$KK"
		ACC=`echo "$KK"| sed -e 's,\/.*\/,,g' -e 's,\..*,,g'`
		echo "$ACC"
		while read CONTIG
			do 
				ACC_VALUES=`grep -m1 "$CONTIG" /home/michael.tisza/ref_virus_blast1/ref_virus_blastout/${ACC}.realign.local.blastout`; printf "$ACC\t$ACC_VALUES\n"
			done >> acc_known_knowns_85id_80len.txt < "$KK"
	done
```

Remove contigs viral contaminants in assemblies /home/michael.tisza/viral_ref_contigs1.sort1.txt
```
sed 's,\,,\t,' viral_ref_contigs1.sort1.txt > viral_ref_contigs1.sort1.txt.tab
grep -v -f viral_ref_contigs1.sort1.txt.tab acc_known_knowns_85id_80len.txt > acc_known_knowns_85id_80len_re_artif.txt
```
Convert TSV to CSV and JSON (using [perl](https://github.com/nevostruev/csv2json))
```
sed 's,\t,\,,g' acc_known_knowns_85id_80len_re_artif.txt > acc_known_knowns_85id_80len_re_artif.csv
perl ~/csv2json/csv2json.pl acc_known_unknowns_50id_50len.csv > acc_known_unknowns_50id_50len.json
```

Known unknowns 85id 50len
```
for KK in /home/michael.tisza/ref_virus_blast1/ref_virus_blastout/*.known_unknowns_85id_50len.txt; do echo "$KK"; ACC=`echo "$KK"| sed -e 's,\/.*\/,,g' -e 's,\..*,,g'`;echo "$ACC"; while read CONTIG; do ACC_VALUES=`grep -m1 "$CONTIG" /home/michael.tisza/ref_virus_blast1/ref_virus_blastout/${ACC}.realign.local.blastout`; printf "$ACC\t$ACC_VALUES\n"; done >> acc_known_unknowns_85id_50len.txt < "$KK"; done
```
Convert TSV to CSV and JSON (using [perl](https://github.com/nevostruev/csv2json))
```
sed 's,\t,\,,g' acc_known_unknowns_85id_50len.txt > acc_known_unknowns_85id_50len.csv
perl ~/csv2json/csv2json.pl acc_known_unknowns_85id_50len.csv > acc_known_unknowns_85id_50len.json 
```

Known unknowns 50id 50len
```
for KK in /home/michael.tisza/ref_virus_blast1/ref_virus_blastout/*.known_unknowns_50id_50len.txt; do echo "$KK"; ACC=`echo "$KK"| sed -e 's,\/.*\/,,g' -e 's,\..*,,g'`;echo "$ACC"; while read CONTIG; do ACC_VALUES=`grep -m1 "$CONTIG" /home/michael.tisza/ref_virus_blast1/ref_virus_blastout/${ACC}.realign.local.blastout`; printf "$ACC\t$ACC_VALUES\n"; done >> acc_known_unknowns_50id_50len.txt < "$KK"; done
```
Convert TSV to CSV and JSON (using [perl](https://github.com/nevostruev/csv2json))
```
sed 's,\t,\,,g' acc_known_unknowns_50id_50len.txt > acc_known_unknowns_50id_50len.csv
perl ~/csv2json/csv2json.pl acc_known_unknowns_50id_50len.csv > acc_known_unknowns_50id_50len.json


```

**Features from the blastn hits**

Index for 'Known' viral contigs indipendent blastn run
- Metagenome SRR accession [string]
- Contig name [string]
- Contig length [int]
- Accession for subject in blastn [string]
- NCBI taxonomy id for subject in blastn hit [string]
- Name of subject in blastn hit [string]
- Length of subject in blastn hit [int]
- Percent idendity of blastn hit [float]
- Evalue of blastn hit [float]
- Bit score of blastn hit [float]
- Length aligned in blastn hit [int]

Index for 'Known' viral contigs from bq tables
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

These are the counts from the new blastn run on Jan 11th against all contigs in test_dataset

| Description | Count | Blastn length cutoff | Blastn identity cutoff | 
| --- | --- | --- | --- |
| Known knowns | 12,650 | >80% | >85% |
| Known unknowns | 1,836 | > 80% | >50% and <85% |
| Known unknowns | 4,713 | >50% to <80% | >85% |
| Unknown unknowns | 4,204,364 | NA | NA |

The CSV and JSON files are in /home/ss2489/Jan11_run
The fasta files are in /home/michael.tisza/ref_virus_blast1/ref_virus_blastout

File types EXTENSIONS:
* UNKNOWN UNKNOWNS - .unknown_unknowns_refviral.fasta
* KNOWN UNKNOWNS1 - .known_unknowns_50id_50len.fasta
* KNOWN UNKNOWNS2 - .known_unknowns_85id_50len.fasta
* KNOWN KNOWNS - .known_85id_80len_re_artif.fasta
* BLAST OUTPUTS - .blastout

Here are the virus species from Refseq with more than 100 hits in the 12,650 known knowns
* 101 Escherichia phage D108
* 114 Enterobacteria phage BP-4795
* 139 Enterobacteria phage YYZ-2008
* 145 Escherichia phage TL-2011b
* 146 Enterobacteria phage fiAA91-ss
* 147 Salmonella phage 118970_sal3
* 161 Escherichia phage PBECO 4
* 162 Escherichia phage 121Q
* 163 Escherichia phage APCEc01
* 167 Shigella phage SfIV
* 196 Escherichia virus P1
* 214 Enterobacteria phage SfV
* 277 Enterobacteria phage phiP27
* 279 Enterobacteria phage cdtI
* 320 Enterobacteria phage mEp460
* 351 Stx2-converting phage 1717
* 409 Enterobacteria phage P88
* 608 Enterobacteria phage HK630
* 3398 uncultured crAssphage


These are the counts from the old run in bq. Please note that these sets are not from all the same fasta files.

| Description | Count | Blastn length cutoff | Blastn identity cutoff | 
| --- | --- | --- | --- |
| Known knowns | 525,346 | >80% | >85% |
| Known unknowns | 64,309 | > 80% | >50% and <85% |
| Known unknowns | 104,154 | >50% to <80% | >85% |
| Unknown unknowns with blast hits | 1,351,557 | <50% | NA |
| Unknown unknowns without blast hits | 20,181,350 | NA | NA |

Output is provided in .CSV and .JSON formats. We also have FASTA for all these sets.

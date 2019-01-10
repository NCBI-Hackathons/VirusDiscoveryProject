# Domain Labeling using rpstblastn
Using full CDD database:
 - rpstblastn with e-value cut-off of 1e-3
 - bitscore cut-off >50
 - output in JSON
 - split CDD database in :
    - Viral CDD --> Provided by Rodney 
    - Cellular CDD --> Provided by Rodney
    - Prokaryotic CDD --> Provided by Rodney 
    - mixed CDD

## Samples to test:
 - Negative:
    - No phage sel from data selection (10 datasets)
    - REFSEQ bacterial sequences (random 100 sequences, chopped in smaller pieces; cut-off: from 1kbp to 1Mbp)
    - REFSEQ cellular sequences (random 31 sequences belonging to fungi, invertebrate and protozoa, chopped in smaller pieces; cut-off: from 1kbp to 1Mbp)
    - optional: minimal Bacillus (deletion strains) WGS
 - Positive:
    - REFSEQ viral genomes
    - Selected SRA from data selection
    - crassphage DB (the 249 crAss-like phage contigs from Guerin et al., 2018)
    - known-known contigs (1330 datasets)

## Metrics:
 - Evalue
 - Number of hits
 - Length of sequence and/or hit
 - Bitscore

## Output:
 - putative viral - pro - cellular
 - ambigious
 - unknowns

 - putative viral to phylogeny
 - drop PRO
 - drop cellular
 - ambigious / unkown to Genes / darkmatter?
 - Darkmatter wants a list of 'definitive viral'


##TODO:
#Running RPSTBLN
 - Test dataset:
 	- dataselection - (10 samples)
	- dataselection + (10 samples)
	- Crassphage dataset (140 contigs, Done)
	- REFSEQ viral genomes (ongoing)
	- Cellular organisms (ongoing) --> CHOP contigs
	- Prokaryotic organisms (ongoing) --> CHOP contigs
 - Scale up to multiple instances
 - run RPSTBLN for known knowns (RUNNING)
 - run RPSTBLN for known unknown / unknown unknown (ON HOLD)
#Parsing results
 - combine JSON files / sample
 - Parse JSON files + run basic statistic metrics for cutoff
 - Divide contigs in parts

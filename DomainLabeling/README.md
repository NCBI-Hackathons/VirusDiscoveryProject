# Domain Labeling using rpstblastn
Using full CDD database:
 - rpstblastn with e-value cut-off of 1e-3
 - output in JSON
 - split CDD database in :
    - Viral CDD --> Provided by Rodney 
    - Cellular CDD
    - Prokaryotic CDD --> Provided by Rodney 
    - mixed CDD

## Samples to test:
 - Negative:
    - No phage sel from data selection (10 datasets)
    - REFSEQ bacterial sequences
    - REFSEQ cellular sequences
 - Positive:
    - REFSEQ viral genomes
    - Selected SRA from data selection
    - crassphage DB
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


##TODO:
 - run RPSTBLN
 - Chop positive control samples from REFSEQ
 - set up jupyter notebook for analysis
 - generate control samples
 - combine JSON formats
 - 

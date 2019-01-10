# Domain Labeling using rpstblastn
Using full CDD database:
 - rpstblastn with e-value cut-off of 1e-3
 - output in JSON
 - split CDD database in :
    - Viral CDD
    - Cellular CDD
    - Prokaryotic CDD
    - mixed CDD

## Samples to test:
 - Negative:
    - No phage sel from data selection
    - REFSEQ bacterial sequences
    - REFSEQ cellular sequences
 - Positive:
    - REFSEQ viral genomes
    - Selected SRA from data selection
    - crassphage DB (249 contigs)

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


# README

## Synopsis

Pipeline to identify SRR contigs with novel viruses and indexing them for lookup
and further analysis. Due to the ludicrous number of contigs, pre-selection
steps are implemented to reduce the number of contigs for the downstream
analysis.

## Prefilter steps
Currently, a contig needs to meet the following requiremnts before
being analyzed further:

- length >= 1kb


## Structure

```
novel
|
+--tools   // directory for tools
   |
   +-bash  // bash tools
   |
   +-contig-filter


```

## Steps

- Clustering
    - mmseq2
    - HMM
    - Other....

### MMseq2

 - Walltime approx 1 hrs to search  NCBI_VIV_protein_sequences_v5
 (513,755 sequences) in ERR210051 contigs (146 contigs, 5 are human chromosomes)
 using 32 cpus.

### ToDo

 - Test if clustering of  target database, e.g. NCBI_VIV_protein_sequences_v5
   improves time.
 - Why is contig-filter.py not reading sys.stdout when reading Docker stdout?
## Notes

- Docker and piping using STDIN and STDOUT is really awful.

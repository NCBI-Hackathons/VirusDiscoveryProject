# README

## Synopsis

Pipeline to identify SRR contigs with novel viruses and indexing them for lookup
and further analysis. Due to the ludicrous number of contigs, pre-selection
steps are implemented to reduce the number of contigs for the downstream
analysis.

## Prefilter steps
Currently, a contig needs to meet the following requirements before
being analyzed further: (key = reduce clutter + runs fast)

- length >= 1kb
- discussed during meeting:
    - removal contigs w/ rRNA (Silva?)
    - list of 'basal Pro/Eu genes

## Input

```bash

sed -i s/>// SRR918250.realign.local.unknowns.txt

seqtk subseq/home/michael.tisza/mt_contigs1/SRR918250.realign.local.1000bp.fa SRR918250.realign.local.unknowns.txt > unk_test.fasta

```


## Output

What and how should we report?
#### JSON ?
```
{
  Contig : SRRXX.contig.N,
  methods :
  {
    mmseq2 :
    {
      parameters : {....},
      total_hits : int,
      hits : [ {accession: AC12345.1, simil:80% ....}   ]
    }
    rpstblastn :
    {
      parameters : {....},
      total_hits : int,
      hits : [ {accession: AC12345.1, simil:80% ....}   ]
    }
  }
}
```

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
    - RPStblastn
    - pVOG

### MMseq2

 - Walltime approx 1 hrs to search  NCBI_VIV_protein_sequences_v5
 (513,755 sequences) in ERR210051 contigs (146 contigs, 5 are human chromosomes)
 using 32 cpus.

### rpstblastn

 - Walltime 2 hrs, ERR1913430 contigs (filtered for length >= 1kb), 560 sequences done
against entire CDD, but on 1 thread

### ToDo

 - Test if clustering of  target database, e.g. NCBI_VIV_protein_sequences_v5
   improves time.
 - Why is contig-filter.py not reading sys.stdout when reading Docker stdout?
 - Walltime for pVOGs
 - Walltime for RPStblastn --> multithreading?

## Notes

- Docker and piping using STDIN and STDOUT is really awful.

# README

## Synopsis

Pipeline to identify SRR contigs with novel viruses and indexing them for lookup
and further analysis. Due to the ludicrous number of contigs, pre-selection
steps are implemented to reduce the number of contigs for the downstream
analysis.

## Prefilter steps
-   Contigs provided should be prefiltered at >= 1kb
-   Further reduction of clutter?  
        -   removal contigs w/ rRNA (Silva?)  
        -   list of 'basal Pro/Eu genes  

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
    - ~~mmseq2~~
    - HMM
    - RPStblastn
    - pVOG
    - RVDB

### MMseq2

 - Walltime approx 1 hrs to search  NCBI_VIV_protein_sequences_v5
 (513,755 sequences) in ERR210051 contigs (146 contigs, 5 are human chromosomes)
 using 32 cpus.
 - Reject, rpstblastn is better suited so far

### rpstblastn

 - Walltime 2 hrs, ERR1913430 contigs (filtered for length >= 1kb), 560 sequences done
against entire CDD, but on 1 thread

### ToDo

 - Walltime for pVOGs
 - Walltime for RVDBs
 - Walltime for RPStblastn --> multithreading?
 - Better cross-referencing to gather metadata of hits
    - `tools/result-reporter` can query Entrez but   
       needs refinment.

## HMMER3 vs RVDB v Oct 2018

```bash


/home/joan.marti.carreras/bin/prodigal -i SRR918250.realign.local.unknowns.fasta -a SRR918250.realign.local.unknowns.prodigal.genes.faa -g 11 -s SRR918250.realign.local.unknowns.prodigal.genes.txt -d SRR918250.realign.local.unknowns.prodigal.genes.fasta -o SRR918250.realign.local.unknowns.prodigal.genes.out &

hmmscan --noali -E 0.01 --domE 0.01 --cpu 32 -o test/SRR918250.realign.local.unknowns.RVDB.out --tblout test/SRR918250.realign.local.unknowns.RVDB.tblout --domtblout test/SRR918250.realign.local.unknowns.RVDB.domtblout --pfamtblout test/SRR918250.realign.local.unknowns.RVDB.pfamtblout databases/RVDB/U-RVDBv14.0-prot-new.hmm test/SRR918250.realign.local.unknowns.prodigal.genes.faa &
	## 40 min aprox

```

## Notes

- Docker and piping using STDIN and STDOUT is really awful.

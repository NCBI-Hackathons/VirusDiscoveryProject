Program `blast_overlaps.pl` takes blast output with `-max_hsps 1` and `-outfmt 6`, such as:

`blastn -outfmt 6 -db /hd2/database/ref_viruses/ref_viruses_rep_genomes_v5 -query ../refseq_viral_human_only_101918.fasta -max_hsps 1 > sample.blast.txt`

The program expects the output to be ordered by query, but this could be easily overcome by sorting or buffering and sorting (at memory expense). The usage is:

```
perl blast_overlaps.pl <blast.txt> [--nonoverlap-threshold <float>] [--overlap-threshold <float>] [--allow-self]
	-N|--nonoverlap_threshold <float>	Takes a float from 0 to 1, default 1. Basis for detecting chimera.
	-O|--overlap_threshold <float>		Takes a float from 0 to 1, default 0. Basis for merging similar matches.
	-A|--allow-self				Allows a match where query and subject are the same.
```

The program filters for queries with multiple subject matches below the `nonoverlap` threshold to detect chimera. This thresholdis in terms of the [overlap coefficient](https://en.wikipedia.org/wiki/Overlap_coefficient), computed as the number of intersecting match bases (two subjects to one query) divided by the minimum match length versus each subject. The program then tries to reduce the output further by removing subject pair members that cover a similar region of the query. Priotization is given to subject matches with higher bitscores and bigger match lengths. Output is listed below. The first three lines (headers) are writtent currently to STDERR.

Set **nonoverlap** coefficient to `0.25`:
```
$ cat sample.blast.txt 
NC_038357.1	NC_014093.1	85.777	914	100	14	2279	3168	2339	3246	0.0	941
NC_038357.1	NC_009225.1	85.652	920	98	21	2279	3169	2325	3239	0.0	937
NC_038357.1	NC_038350.1	86.183	427	55	2	20	444	1	425	5.30e-127	459
NC_038357.1	NC_038351.1	82.201	427	65	9	20	442	1	420	1.99e-96	357
NC_038357.1	NC_007014.1	94.608	204	8	3	18	221	1	201	4.37e-83	313
NC_038357.1	NC_007013.1	96.203	158	4	1	64	221	1	156	2.08e-66	257
NC_038357.1	NC_025726.1	85.455	55	5	3	2900	2952	5	58	2.92e-05	54.7
$
$ perl blast_overlaps.pl sample.blast.txt 
NONOVERLAP THRESHOLD	(i < thresh)	1
OVERLAP THRESHOLD	(i >= thresh)	1
Q_id	S1_id	S2_id	Overlap_coeff	S1_start	S1_end	Bitscore1	S2_start	S2_end	Bitscore2
NC_038357.1	NC_007014.1	NC_014093.1	0.0000	18	221	313	2279	3168	941
NC_038357.1	NC_007014.1	NC_038350.1	0.9902	18	221	313	20	444	459
NC_038357.1	NC_014093.1	NC_038350.1	0.0000	2279	3168	941	20	444	459
$
$ perl blast_overlaps.pl sample.blast.txt  -N 0.25
NONOVERLAP THRESHOLD	(i < thresh)	0.25
OVERLAP THRESHOLD	(i >= thresh)	1
Q_id	S1_id	S2_id	Overlap_coeff	S1_start	S1_end	Bitscore1	S2_start	S2_end	Bitscore2
NC_038357.1	NC_007014.1	NC_014093.1	0.0000	18	221	313	2279	3168	941
NC_038357.1	NC_014093.1	NC_038350.1	0.0000	2279	3168	941	20	444	459
```

Now ease the **overlap** threshold definition down (`0.75`) to merge redundant subject loci:
```
$ perl blast_overlaps.pl sample.blast.txt  -N 0.25 -O 0.75
NONOVERLAP THRESHOLD	(i < thresh)	0.25
OVERLAP THRESHOLD	(i >= thresh)	0.75
Q_id	S1_id	S2_id	Overlap_coeff	S1_start	S1_end	Bitscore1	S2_start	S2_end	Bitscore2
NC_038357.1	NC_014093.1	NC_038350.1	0.0000	2279	3168	941	20	444	459
```
In this case,`NC_007014` was removed because it overlaps to query with `NC_038350` but in an inferior way. Thus, ` NC_014093` does not overlap with `NC_038350` the best with respect to matches to ` NC_014093`. 

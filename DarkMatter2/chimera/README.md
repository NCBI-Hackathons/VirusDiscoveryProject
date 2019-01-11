Program `blast_overlaps.pl` takes blast output with `-max_hsps 1` (unless `--allow-multiples`) and `-outfmt 6`, such as:

`blastn -outfmt 6 -db /hd2/database/ref_viruses/ref_viruses_rep_genomes_v5 -query ../refseq_viral_human_only_101918.fasta -max_hsps 1 > sample.blast.txt`

The program expects the output to be ordered by query, but this could be easily overcome by sorting or buffering and sorting (at memory expense). The usage is:

```
perl blast_overlaps.pl <blast.txt> [--nonoverlap-threshold <float>] [--overlap-threshold <float>] [--allow-self]
	-N|--nonoverlap_threshold <float>	Takes a float from 0 to 1, default 1. Basis for detecting chimera.
	-O|--overlap_threshold <float>		Takes a float from 0 to 1, default 0. Basis for merging similar matches.
	-A|--allow-self				Allows a match where query and subject are the same.
	-M|--allow-multiples			Allows multiple high scoring segment per hit.
	-R|--no-redundant			Reduces the pairwise output for multiple hits to something more sequential.
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
In this case, subject match `NC_007014` was removed because it overlaps to query with subject match `NC_038350` but in an inferior way. Thus, only subject match ` NC_014093` is non-overlapping with subject match `NC_038350` with respect to query ` NC_038357`.  Finally, let us turn to looking at multiple hits per subject in a mycophage example.

```
$ cat mycophage_sample.txt 
GU247133.1	DQ398046.1	99.494	51569	233	10	1	51562	1	51548	0.0	93759
GU247133.1	DQ398046.1	98.692	7719	95	4	57822	65538	57405	65119	0.0	13690
GU247133.1	DQ398046.1	99.825	3999	7	0	51867	55865	51550	55548	0.0	7347
GU247133.1	DQ398046.1	99.583	2876	10	2	65696	68569	65552	68427	0.0	5243
GU247133.1	DQ398046.1	99.505	202	1	0	57626	57827	57035	57236	5.13e-102	368
GU247133.1	DQ398046.1	98.876	89	1	0	56177	56265	55570	55658	3.36e-39	159
GU247133.1	DQ398046.1	91.765	85	4	2	61971	62052	60868	60952	7.38e-26	115
GU247133.1	DQ398046.1	91.765	85	4	2	61289	61373	61550	61631	7.38e-26	115
GU247133.1	DQ398046.1	89.552	67	5	1	20131	20195	2428	2362	2.08e-16	84.2
GU247133.1	DQ398046.1	89.552	67	5	1	2362	2428	20184	20120	2.08e-16	84.2
GU247133.1	DQ398046.1	86.667	75	7	2	40436	40508	2429	2356	2.69e-15	80.5
GU247133.1	DQ398046.1	87.324	71	7	2	65403	65472	40421	40490	2.69e-15	80.5
GU247133.1	DQ398046.1	86.667	75	7	2	2356	2429	40494	40422	2.69e-15	80.5
GU247133.1	DQ398046.1	87.324	71	7	2	40435	40504	64983	65052	2.69e-15	80.5
GU247133.1	DQ398046.1	91.667	48	4	0	59042	59089	41119	41166	2.10e-11	67.6
GU247133.1	DQ398046.1	91.667	48	4	0	41133	41180	58625	58672	2.10e-11	67.6
GU247133.1	DQ398046.1	93.023	43	1	2	61031	61073	61365	61405	9.75e-10	62.1
GU247133.1	DQ398046.1	97.222	36	0	1	61786	61820	60611	60646	3.51e-09	60.2
AF547430.1	DQ398046.1	99.747	47870	108	4	1	47870	1	47857	0.0	87716
AF547430.1	DQ398046.1	99.942	20578	10	2	48423	68999	47851	68427	0.0	37933
AF547430.1	DQ398046.1	91.765	85	4	2	62122	62203	60868	60952	7.43e-26	115
AF547430.1	DQ398046.1	91.765	85	4	2	61440	61524	61550	61631	7.43e-26	115
AF547430.1	DQ398046.1	89.552	67	5	1	20133	20197	2428	2362	2.09e-16	84.2
AF547430.1	DQ398046.1	89.552	67	5	1	2362	2428	20184	20120	2.09e-16	84.2
AF547430.1	DQ398046.1	86.667	75	7	2	40435	40507	2429	2356	2.71e-15	80.5
AF547430.1	DQ398046.1	87.324	71	7	2	65555	65624	40421	40490	2.71e-15	80.5
AF547430.1	DQ398046.1	86.667	75	7	2	2356	2429	40494	40422	2.71e-15	80.5
AF547430.1	DQ398046.1	87.324	71	7	2	40434	40503	64983	65052	2.71e-15	80.5
AF547430.1	DQ398046.1	91.667	48	4	0	59196	59243	41119	41166	2.11e-11	67.6
AF547430.1	DQ398046.1	91.667	48	4	0	41132	41179	58625	58672	2.11e-11	67.6
AF547430.1	DQ398046.1	93.023	43	1	2	61182	61224	61365	61405	9.82e-10	62.1
AF547430.1	DQ398046.1	97.222	36	0	1	61937	61971	60611	60646	3.53e-09	60.2
$ 
$ perl blast_overlaps.pl -M -R -N 0.75 -O 0.25 mycophage_sample.txt 
NONOVERLAP THRESHOLD	(i < thresh)	0.75
OVERLAP THRESHOLD	(i >= thresh)	0.25
Q_id	S1_id	S2_id	Overlap_coeff	S1_start	S1_end	Bitscore1	S2_start	S2_end	Bitscore2
GU247133.1	DQ398046.1	DQ398046.1	0.0000	1	51562	93759	51867	55865	7347
GU247133.1	DQ398046.1	DQ398046.1	0.0000	51867	55865	7347	56177	56265	159
GU247133.1	DQ398046.1	DQ398046.1	0.0000	56177	56265	159	57626	57827	368
GU247133.1	DQ398046.1	DQ398046.1	0.0297	57626	57827	368	57822	65538	13690
GU247133.1	DQ398046.1	DQ398046.1	0.0000	57822	65538	13690	65696	68569	5243
AF547430.1	DQ398046.1	DQ398046.1	0.0000	1	47870	87716	48423	68999	37933
```

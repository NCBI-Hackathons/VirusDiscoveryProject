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
$ perl blast_overlaps.pl sample.bast.txt -N 0.25
NONOVERLAP THRESHOLD: 0.25
OVERLAP THRESHOLD: 0
Q_id	S1_id	S2_id	Overlap_coeff	S1_start	S1_end	Bitscore1	S2_start	S2_end	Bitscore2
NC_038357.1	NC_007013.1	NC_038352.1	0.1438	64	2250	2682	2085	3238	1037
NC_038357.1	NC_007013.1	NC_038353.1	0.1331	64	2250	2682	2099	3240	1171
NC_038357.1	NC_007013.1	NC_038354.1	0.1891	64	2250	2682	2019	3245	1109
NC_038357.1	NC_007013.1	NC_038355.1	0.2333	64	2250	2682	1950	3239	1164
NC_038357.1	NC_007013.1	NC_038356.1	0.2091	64	2250	2682	1988	3245	976
NC_038357.1	NC_007013.1	NC_038361.1	0.1938	64	2250	2682	2013	3240	1208
```

Now move up the **overlap** threshold (`0.21`) to merge redundant subject loci:
```
$ perl blast_overlaps.pl sample.bast.txt -N 0.25 -O 0.21
NONOVERLAP THRESHOLD: 0.25
OVERLAP THRESHOLD: 0.21
Q_id	S1_id	S2_id	Overlap_coeff	S1_start	S1_end	Bitscore1	S2_start	S2_end	Bitscore2
NC_038357.1	NC_007013.1	NC_038355.1	0.2333	64	2250	2682	1950	3239	1164
```

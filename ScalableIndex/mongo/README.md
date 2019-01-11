# Loading Data Into MongoDB

The Makefile contains targets to download data (`make data`) and load it
(`make load`). 

After loading contigs, samples, and metadata, you need to run `flatten.pl`
to denormalize the data for querying.

# Querying MongoDB

You can use the `query.pl` to get data from Mongo:

```
./query.pl -f contig__length '>=100' \
  -f meta__center 'UNIVERSITY OF OXFORD' \
  -f sample__sacc 'NC_005856'
```

Run with `-h` for help.

You can benchmark with `--bench` and a number of iterations.

# Author 

Ken Youens-Clark <kyclark@email.arizona.edu>

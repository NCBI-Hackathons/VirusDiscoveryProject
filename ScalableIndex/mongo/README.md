# Loading Data Into MongoDB

The Makefile contains targets to download data (`make data`) and load it
(`make load`). 

After loading contigs, samples, and metadata, you need to run `flatten.pl`
to denormalize the data for querying.

# Querying MongoDB

You can use the `query.pl` to get data from Mongo:

```
./query.pl -l '>=100' -c 'UNIVERSITY OF OXFORD' -s 'NC_005856'
```

Run with `-h` for help.

You can benchmark with `--bench` and a number of iterations.

```
$ ./query.pl -l '>=100' -c 'UNIVERSITY OF OXFORD' -s 'NC_005856' -b 1000000
{
  length => { "\$gte" => 100 },
  meta__center => "UNIVERSITY OF OXFORD",
  sample__sacc => "NC_005856",
}
Benchmarking 1000000 iterations...
timethis 1000000: 15 wallclock secs (15.12 usr +  0.00 sys = 15.12 CPU) @ 66137.57/s (n=1000000)
```

# Author 

Ken Youens-Clark <kyclark@email.arizona.edu>

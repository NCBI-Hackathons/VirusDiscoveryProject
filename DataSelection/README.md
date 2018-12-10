# Data Selection

Take a look at the [datasets](datasets.ipynb) jupyter notebook that summarizes everything.

The [WGS datasets](wgs_datasets.tsv.gz) file (*Note*: This is gzip compressed) has all the raw data. This is a `.tsv` file and so you can load it into a spreadsheet program.

The [random selection](random_selection.txt) file has a set of 1,000 metagenomes chosen at random.

The [size selection](size_selection.txt) file has 999 metagenome IDs chosen as small, medium, or large data sets.

The [phage selection](phage_size_selection.txt) file has 999 metagenome IDs chosen as small, medium, or large data sets but that have the most number of phage fragments.


We should use the data sets listed in the [phage selection](phage_size_selection.txt) file.


We should add metagenomes that have 0% hits to phages to be able to calculate accuracy metrics like false positives, negatives, etc.

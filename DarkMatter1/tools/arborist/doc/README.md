# arborist.py

Prototype to score contigs for novel virus pipeline.

usage:

Show interval coverage (simple scoring demo):

`novel/tools/arborist/src/arborist.py --srr 12334 -b rpstblastn < novel/tools/arborist/doc/cdd.example`

Print interval tree (requires dot from graphviz):

`head -n 200 novel/tools/arborist/doc/cdd.example | novel/tools/arborist/src/arborist.py --srr 12334 -b rpstblastn | dot -Tpdf > out.pdf`


## Dark Matter 1 
![](http://vignette4.wikia.nocookie.net/callofduty/images/7/79/Dark_Matter_Camouflage_menu_icon_BO3.png/revision/latest?cb=20160506200857)

_Jan Buchmann, Cody Glickman, Laura Milena, Forero Junco, Lindsay Rutter, Ryan Shean_

### Objective
Collating output of multiple teams to identify novel viral contigs in metagenomic datasets

### Overview
```
Using bucket gs://ncbi_intact for input and output (being currently set up)
```

### Internal JSON data
```
{
  domains: [
            {start: int, end: int,name: char},
            {start: int, end: int,name: char}
            ],
  orfs: [
          {start: int, end: int,name: char},
          {start: int, end: int,name: char}
        ]
}
```
### Required Tools and Databases
HMMer
VIGA

RVDB
Viral RefSeq 
pVOGs

### Expected Input
Assembled fasta files and associated metadata

### Projected Output
JSON file of ORFs with names, annotation, and possibly a scoring methodology? 

### Methods
We are currrently exploring two options and comparing the overlap: 

1. Our predicted ORFs from unknown contigs are subjected to an iterative HMM search against proteins regarded as viral upstream (Team 3, known knowns and known unknowns). We will create a scoring metric that combines features such as contig length, domain abundances, and others?


2. Scoring will consider if the same ORFs/regions have been identified by different databases and tools.

We will use jackhmmer to assign putatitive names to contigs that Team 5 passed to us. We will parse jackhmmer output and generate a JSON in the outlined format to team scaling. 

### Scripts and Parameters



### Contact


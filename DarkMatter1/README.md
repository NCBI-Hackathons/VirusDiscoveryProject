## Dark Matter 1 
![](http://vignette4.wikia.nocookie.net/callofduty/images/7/79/Dark_Matter_Camouflage_menu_icon_BO3.png/revision/latest?cb=20160506200857)

_Jan Buchmann, Cody Glickman, Laura Milena Forero Junco, Lindsay Rutter, Ryan Shean_

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

1. Our predicted ORFs from unknown contigs (OrfM) are subjected to an iterative HMM search against proteins regarded as viral upstream (Definitive viral + proteins predicted by Team 3). We will use Jackhmmer for this approach. We will create a scoring metric that combines features such as contig length, domain hit abundances, ORF abundances, strand, e-value, and others. 
   * *Negative Control*: Bacterial contigs discovered by the domains team will be run to calculate the number of false positives


2. Utilizing the viral annotation pipeline (VIGA), we are developing a scoring method to split contigs for additional processing. VIGA uses blastx annotation and pVOG databases to annotate prodigal predicted genes. The resulting tabular output contains features including strand, amino acid size, location start, annotations, and pVOG hits. The scoring system will determine which contigs to port downstream to team 7 or retain for expanded processing. The high scoring contigs will be additionally processed using the approach defined in method 1 to expand the search space for domains. 
   * *Negative control*: Bacterial contigs discovered by the domains team will be passed through the pipeline and scoring metric to calculate the number of false positives
   * *Postive control*: Viral contigs discovered by the domains team will be passed through the pipeline and scoring metric to calculate the number of false positives
   * *Sample Data*: 7 Known knowns contigs have been passed through the pipeline and the scoring system is currently being developed against this output
   * *Scaling*: The VIGA pipeline can be run in parallel and completed quickly (>10s wall time) with positive control. It is unknown how scaling the data in each run affects processing speed. 



The resulting information on each contig will be stored in JSON format. The JSON file is passed in the outlined format to team scaling. 

### Example results
New norovirus sequence was recovered from ERR2030176 and automatically annotated with [VAPiD](https://github.com/rcs333/VAPiD)
### Scripts and Parameters

We will write most of our scripts with Python.

### Contact

rcs333@uw.edu  
https://github.com/lrutter


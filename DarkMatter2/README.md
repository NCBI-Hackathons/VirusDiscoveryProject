In accession SRR5260890, which is putatively a freshwater metagenome sample from Crystal Bog Wisconsin, there were five large contigs named with RefSeq.

  - NC_001479.1 – Encephalomyocarditis virus
  - NC_001352.1 – Human papillomavirus 2 
  - NC_00933.1 – Human herpesvirus 8
  - NC_001716.2 – Human herpesvirus 7
  - NC_001664.3 – Human herpesvirus 6A

They had been assembled in their entirety.  We learned that they are reference sequences and not actual contigs.  Why they are exported in the nominal de novo fasta is not clear.  A hypothesis is that there were telomeric-like sequences or other low-complexity sequence repeats that trip the k-mer wire for these human herpesviruses.  For ECMV, it has a classic poly-C tract that might be given k-mer hits.  The code that NCBI screened the reads with then took the reads and performed a directed alignment to these reference genomes.  It then exported the reference genome in the contig set.

These are present in hundreds of assemblies. A hallmark of these issues is full-length sequence, low coverage (1X), and NC_ header.

  - SRR5131927.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR514227.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5209941.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5260890.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5261043.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5271510.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5382269.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5382285.realign.local.fa.gz:>NC_001664.3:1.159321
  SRR5383919.realign.local.fa.gz:>NC_001664.3:1.159321
  SRR5429532.realign.local.fa.gz:>NC_001664.3:1.159321
  SRR5567687.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5601447.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5601453.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5675744.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5675746.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5675761.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5675777.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5678966.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5720301.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5720324.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5788318.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5855497.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5865004.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5865037.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5912597.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5940705.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5940707.realign.local.fa.gz:>NC_001664.3:1.159321
SRR5983464.realign.local.fa.gz:>NC_001664.3:1.159321

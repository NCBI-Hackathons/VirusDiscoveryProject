# Dark Matter 2

### QC: Understanding the realign.local.fa files


#### They are not all contigs.



In accession SRR5260890, which is putatively a freshwater metagenome sample from Crystal Bog Wisconsin, there were five large contigs named with RefSeq identifiers.

  - NC_001479.1 – Encephalomyocarditis virus
  - NC_001352.1 – Human papillomavirus 2 
  - NC_00933.1 – Human herpesvirus 8
  - NC_001716.2 – Human herpesvirus 7
  - NC_001664.3 – Human herpesvirus 6A

They had been assembled in their entirety.  They aligned with >99.9% identity with 100% coverage to their respective virus in NT.  They came from fresh-water metagenomic samples.  We think they are reference sequences and not actual contigs.  Why they are exported in the nominal de novo fasta is not clear.  A hypothesis is that there were telomeric-like sequences or other low-complexity sequence repeats that trip the k-mer wire for these human herpesviruses.  For ECMV, it has a classic poly-C tract that might be given k-mer hits.  The code that NCBI screened the reads with then took the reads and performed a directed alignment to these reference genomes.  We're concerned it then exported the reference genome in the contig set.

These are present in many assemblies. A hallmark of these issues is full-length sequence, low coverage (1X), and NC_ header.  If you just look through the 406 SRR5*.fa.gz files, there are 5,128 "contigs" with NC_0 names...so maybe expecting ~10 of these per contig file.  That could be a lot of meatballs.  Some of them could be legit assemblies, but there's a lot of fishiness.  Here are just the full-length HHV-6A ones from SRR5*.fa.gz files with 1X coverage and full-length sequence.

  - SRR5131927.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR514227.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5209941.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5260890.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5261043.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5271510.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5382269.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5382285.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5383919.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5429532.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5567687.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5601447.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5601453.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5675744.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5675746.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5675761.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5675777.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5678966.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5720301.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5720324.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5788318.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5855497.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5865004.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5865037.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5912597.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5940705.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5940707.realign.local.fa.gz:>NC_001664.3:1.159321
  - SRR5983464.realign.local.fa.gz:>NC_001664.3:1.159321
  
  ### Prioritizing true Dark Matter
  
  #### We don't have true Dark Matter yet, but many of the realign.local.fa files have dark matter.  
  
  Assuming the upstream classification steps work, existing reference databases -- NT, NR, PFAM, CDD -- will not help us annotate these contigs much.  So, let's assume that we have one of the world's greatest datasets of Dark Matter and so we will use our own unannotated contigs as reference.  We have set up All x All self-tblastx to look for relationships among different datasets.  This will allow us to 
  - 1) check potential annotations (are we using the correct genetic codes for translation?  Do starts and stops jive?)
  - 2) prioritize Dark Matter for characterization in the future (pull sample metadata, screen SRA for it, etc.)
  
  We have "validated" the All x All tblastx on a select dataset that identified non-Dark Matter from multiple datasets.  Basically it found all the human gut/feces metagenomes.  Though this was not performed on Dark Matter, it was tblastx based and so could see pretty distant stuff in this space.
  
  ### Rule-out trivial reasons for Dark Matter
  
  #### Chimeras
    see ReadMe in chimera folder
  #### Low complexity
    Unclear how much of a problem if we only look at contigs > 1 kb
  

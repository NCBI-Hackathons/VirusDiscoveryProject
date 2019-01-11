# Machine Learning Team: Data-based Metadata Interpolation

## Problem 1: Unsupervised clustering of datasets using viral MASH (Ondov et al 2016) contig features and extraction of highly associated metadata terms
- Feature set: Using MASH to construct kmer composition of contigs
- Label set: SRAdb to extract SRR metadata
- Learning: Pricipal Coordinate Analysis (PCoA)
- Learning: kNN to share common descriptors accross similar SRRs in MASH kmer space

## Problem 1_b: Network Smoothing for interpolation of continuous variables in kmer-space
- Network/Matrix: MASH kmer composition
- Label: % Dark Matter, % Herpes...whatever
- Method: Network Smoothing

## Problem 2 : Predicting the amount of "Dark Matter"
- Feature set : doc2vec, Paragraph Vector parsing of the SRR metadata (library preparation....) 
- label : %Dark Matter
- Learning: ataboost, random forest, generalized linear regression

## Shortcomings
There are none, the computers are sentient so we can relax.

# Run instructions

## Feature set collection

### SRAdb: collect abstracts, descriptions (to "SRA.sel") and all bioproject data (to "SRA.all")
Query SRA and bioprojects study description, abstracts...data for string-based learning and annotation
```R
# install
source("https://bioconductor.org/biocLite.R")
biocLite("SRAdb") # requires additional install of openssl in the bash environment
# input: VirusDiscoveryProject/MachineLearning/data_in/allSRR.txt
source('VirusDiscoveryProject/MachineLearning/data_in/SRAdb/sra_query.r')
# output: SRA.all_SRR.csv & SRA.sel_SRR.csv in VirusDiscoveryProject/MachineLearning/data_in/SRAdb/
```
SRA data was cleaned and tabulated for word frequency using
```
source('/MachineLearning/feature_computed/SRA_meta_matrix.r')
```
This produced feature_computed/SRA_meta_matrix.word_count.csv and feature_computed/SRA_meta_matrix.word_frequency.csv

## File Structure
```
MachineLearning/
+-- data_in/
|   +-- known_contigs.json
|   +-- known_contig_metadata.json
+-- feature_computed/
|   +-- contig_features.GLOVE.json
|   +-- contig_features.prodigal.json
|   +-- contif_features.TE_informatoin.json
+-- data_out/
|   +-- contig_features.all.json
+-- code
|   +-- taxID.py # convert tax ID to taxanomic groups
|   +-- feature_extraction/
|       +-- feature_extract.GLOVE.py
|       +-- feature_extract.prodigal.py
|       +-- feature_extract.TE_information.py
|   +-- predictors/
|       +-- training.viral_groups.py # random forest, ataboost, logit :: features.all --> taxanomic groups
|       +-- model.viral_groups.pickle
|       +-- run_model.viral_groups.py ## take contig and generate prediction
```
## To do list
- [ ] get "known" contig set from #known team 
- [ ] choose the taxanomic groups # taxID.py
- [ ] generate contig_features.GLOVE.json
- [ ] generate contig_features.prodical.json
- [ ] generate contig_features.TE_informatoin.json
- [ ] aggregate contig_features to .all
- [ ] training.viral_groups.py 
- [ ] run_model.viral_groups.py

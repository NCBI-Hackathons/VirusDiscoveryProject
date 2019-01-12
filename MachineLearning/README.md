# Machine Learning Team: Data-based Metadata Interpolation

## Problem 1: Unsupervised clustering of datasets using viral MASH (Ondov et al 2016) contig features and extraction of highly associated metadata terms

Using MASH to estimate Jaccard distances between samples based on their viral content. Ward's method was used to cluster datasets. Samples with less than 3 contigs were removed from the analysis. A kmer size of 21pb and a sketch size of 10 000 was used.

![alt text](https://github.com/NCBI-Hackathons/VirusDiscoveryProject/blob/master/MachineLearning/figures/Slide1.png "Clustering")


In order to identify some drivers that could explain this content-based clusters, the words from the SRA study comments and abstracts were extracted using SRAdb(DOI: 10.18129/B9.bioc.SRAdb). 
A vector of word frequencies was constructed across the selected samples. A manual cleaning of the terms was performed to remove punctuation and low-informative terms. 

The most frequent meaningfull words for each clusters were represented 

![alt text](https://github.com/NCBI-Hackathons/VirusDiscoveryProject/blob/master/MachineLearning/figures/clusters_hack.png "word frequencies")

In total, 210 samples with abstract and comments were analyzed. A PLS was performed in order to identify any co-variance between the identified clusters using MASH and the word frequencies associated to the samples. No strong co-variance could identified using this approach, suggesting that abstracts and comments vocabularies are too vague to automatically caracterize samples.

![alt text](https://github.com/NCBI-Hackathons/VirusDiscoveryProject/blob/master/MachineLearning/figures/network_PLS.png "PLS_analysis")


## Problem 2: Inferring metadata 

As a proof of concept, we show that natural language processing (NLP) trained on SRA and associated project metadata can identify SRA’s from human gut microbiome metagenomes. 

Doc2vec, an NLP algorithm that uses unsupervised learning to embed variable-length texts into a vector, was trained on the SRA metadata of 628 samples and transformed the metadata into a 300-dimension vector. t-SNE, a popular dimensionality reduction tool, was trained and transformed the vectors into coordinates for a 2D space. 
The SRA metadata was labeled based on the center_project_name, which is typically used to identify the environment from which the metagenome was sequenced from. Three “center_project_name” classes were examined: “human gut microbiome”, “NA”/“None”, and other. The Figure shows that all three classes are easily and cleanly separable. Next, NA samples were removed from the dataset and Doc2vec and t-SNE were retrained on this new dataset. In this setting, SRA metadata from human gut microbiome projects can still be distinguished from other projects.

![alt text](https://github.com/NCBI-Hackathons/VirusDiscoveryProject/blob/master/MachineLearning/figures/hgm_na_other.png "HMG")

Some possible uses of this technique include correcting mislabeled metadata or annotating SRA’s with missing metadata.





# Run Overview

## Feature set collection

### MASH: kmer clustering on contigs

```
source('MachineLearning/code/run_Mash.sh')
```

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
source('MachineLearning/feature_computed/SRA_meta_matrix.r')
```
This produced feature_computed/SRA_meta_matrix.word_count.csv and feature_computed/SRA_meta_matrix.word_frequency.csv

### Word counting 

```R
source('MachineLearning/learning/wordFreq2MASHgroups.r')
```
produces MachineLearning/learning/wordFreq2MASHgroups.json which contains frequent words by MASH group

Figures were generated in python using ... *MATT*

### Partial Least Squares Analysis
```R
source('MachineLearning/code/PLS.R')
```

### Final thoughts :
https://twitter.com/kareem_carr/status/1083412004642213895

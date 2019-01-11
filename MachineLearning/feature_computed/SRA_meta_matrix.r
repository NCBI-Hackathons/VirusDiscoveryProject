library(stringr)
library(reshape2)

#
setwd('~/VirusDiscoveryProject')
# load meta data
meta_sel = read.csv("MachineLearning/data_in/SRAdb/SRA.sel_SRR.csv")

# word vector
words = strsplit(gsub('NA','',apply(meta_sel[,4:5],1,paste,collapse=' ')),"\\s+")
names(words) = as.character( meta_sel$run_accession ) 
word_melt = melt(words)
word_melt$value = str_replace_all(as.character(word_melt$value), "[[:punct:]]", " ")

# out 
tab = table(word_melt)
write.csv(tab,file='MachineLearning/feature_computed/SRA_meta_matrix.csv')

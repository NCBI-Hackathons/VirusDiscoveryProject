library(jsonlite)

setwd('~/VirusDiscoveryProject')

# load word frequency
wf_in = read.csv('MachineLearning/feature_computed/SRA_meta_matrix.word_frequency.csv')
wf = t(data.matrix(wf_in[,-1]))
names = as.character(wf_in[,1])
colnames(wf) = names

# load MASH groups
groups = read.csv('MachineLearning/feature_computed/MASH/groups_all_vs_all_corr.csv')
groupID = colnames(groups)[-1]

# merge
data = merge(wf,groups,by.x='row.names',by.y='X')
#data = data[,colSums(data)>0]

# look for word ~ group associations
names = names[names%in%colnames(data)]
most_freq_words = list()
for( g in groupID){
	most_freq_words[[g]] = lapply( sort(unique(data[[g]])) , function(gi){
		s=sort( colSums( data[ data[[g]]==gi , names ] ),decreasing=T)
		s = s[s>0]
		s
	})
	names(most_freq_words[[g]]) = sort(unique(data[[g]]))
}


#### write out
write(toJSON(most_freq_words),file='MachineLearning/learning/wordFreq2MASHgroups.json')

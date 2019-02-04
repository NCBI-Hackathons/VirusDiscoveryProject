### Network Word Smoothing

# load network
A = read.csv('MachineLearning/feature_computed/MASH/all_vs_all.txt',sep='\t')
A=A[,-1]
names_A = unlist(lapply( strsplit( colnames(A) , '\\.' ), function(x) x[1]))
colnames(A) = names_A
A$srr = names_A
A_orig = A

# load word frequency
wf_in = read.csv('MachineLearning/feature_computed/SRA_meta_matrix.word_frequency.csv')
wf = t(data.matrix(wf_in[,-1]))
names_wf = as.character(wf_in[,1])
colnames(wf) = names_wf
wf = as.data.frame(wf)
wf$srr = rownames(wf)
wf_orig = wf

## match network to annotation
data = merge(A,wf,by='srr')
A = data[,data$srr]
wf = data[,names_wf[names_wf%in%colnames(data)]]

# smoothing function
smooth <- function(A,x,steps=5,a=0.5){
	A[diag(A)] = 0
	x0 = x
	xi_prev = x
	# Random walk with restarts 
	for(i in steps){
		x = ((1 - a) * (A %*% xi_prev)) +  a * x0
		xi_prev = x
	}
	x
}

cool_words = c('coli','human','ibd','endoscopy','cyanobacteria','artic')

w_out = list()
# iterate over each word
smoothing = lapply( colnames(wf) , function(w){
	print(w)
	# smooth word over network
	scale( smooth(1-data.matrix(A),wf[[w]],) )
})
smoothing = do.call(cbind,smoothing)
colnames(smoothing) = colnames(wf)

smoothing = smoothing[,-(1:146)] # remove numbers of gibberish
write.table(smoothing,file='MachineLearning/learning/smoothed_metadata.csv',sep=',')

#n='human'
#plot(wf[[n]],smoothing[,colnames(smoothing)==n])

### make graph
library( igraph )
rownames(smoothing) = data$srr
A_net = 1-data.matrix(A)
A_net[A_net<.6] = 0
A_net[lower.tri(A_net,diag=T) & upper.tri(A_net,diag=T)] = 0
g = graph_from_adjacency_matrix(A_net)

n=20
V(g)$color = cm.colors(n)[cut(smoothing[,colnames(smoothing)=='endoscopy'],n)]
plot(g ) #, vertex.size =1, arrow.size=.1 )

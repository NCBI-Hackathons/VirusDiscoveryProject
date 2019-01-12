library(gplots)
library(RColorBrewer) 
#settings for the colors of the heatmap
my_palette <- colorRampPalette(c("green", "yellow", "red"))(n = 299)
col_breaks = c(seq(0,0.33,length=100),seq(0.34,0.66,length=100), seq(0.67,1,length=100))
#download distance matrix from MASH/LIBRA
file="/Users/aponsero/Documents/hackathon/all_vs_all_corr.csv"
mydata = read.csv(file, sep = ",", header=TRUE)
graph1=mydata #or graph1=1-mydata when it is a similarity matrix
mat_graph1<-data.matrix(graph1)
#clustering method : Ward.D2
rc=hclust(as.dist(mat_graph1), method="ward.D2")
#plot the clustering result
plot(rc)
#construct the heatmap with the clustering dendogram
hc=heatmap.2(mat_graph1, Rowv=rev(as.dendrogram(rc)), 
          Colv=as.dendrogram(rc), trace="none",  margins =c(15,15), col=cm.colors, 
          breaks=col_breaks, distfun=as.dist)

#cutree(hc, k = 1:5) #k = 1 is trivial
cut <- cutree(as.hclust(hc$colDendrogram), h = c(6,4,3,2,1.5,1,.5,.25))

write.csv(cut, file = "/Users/aponsero/Documents/hackathon/groups_all_vs_all_corr.csv")

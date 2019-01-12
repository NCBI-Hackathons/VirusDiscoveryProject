library(mixOmics)
library(igraph)
data_groups<- read.csv(file="head_selected_groups_all_vs_all_corr.csv", header=TRUE, sep=",")
data_words<- read.csv(file="head_selected_swSRA_meta_matrix.word_frequency.csv", header=TRUE, sep=",")

X <- data_words
Y <- data_groups

head(cbind(rownames(X), rownames(Y))) 

toy_data.pls <- pls(X, Y, ncomp = 8, mode = "regression")
tune.pls <- perf(toy_data.pls, validation = "loo", progressBar = FALSE, nrepeat = 50)
plot(tune.pls$Q2.total)
abline(h = 0.0975)
tune.pls$Q2.total

plotIndiv(toy_data.pls, comp = 1:2, rep.space= 'Y-variate',
          legend = FALSE, title = 'Data_toy, PLS comp 1 - 2, Y-space')

plotIndiv(toy_data.pls, comp = 1:2, rep.space= 'X-variate',
          legend = FALSE, title = 'Data_toy, PLS comp 1 - 2, X-space')

plotIndiv(toy_data.pls, comp = 1:2, rep.space= 'XY-variate', 
          legend = FALSE, title = 'Data_toy, PLS comp 1 - 2, XY-space')

plotVar(toy_data.pls, comp = 2:3, cutoff = 0.5, var.names = c(TRUE, TRUE), title = 'toy_data, rCCA comp 1 - 2')

color.edge <- color.GreenRed(50)
network(toy_data.pls, comp = 1:3, shape.node = c("rectangle", "circle"),
        color.node = c("white", "pink"), color.edge = color.edge, cutoff = 0.15)

cim(toy_data.pls, comp = 1:2, xlab = "metabolites", ylab = "taxon", 
    margins = c(7, 7))

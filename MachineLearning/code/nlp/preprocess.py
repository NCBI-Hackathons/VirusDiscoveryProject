import os
import numpy as np
import sys
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
from sklearn.manifold import TSNE
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn import preprocessing
import matplotlib.cm as cm


#input_file = "../../../../data/total_metadata.csv"
input_file = "../../../../data/results-20190110-153559.csv"
sentences = []
labels = []
with open(input_file, 'r') as f:
    for l in f:
        if l == "\n":
            continue
        l = l[:-1]
        larr = l.split(",")
        labels.append(larr[17])
        sentences.append(' '.join(larr[0:17] + larr[18:]))
labels.pop(0)
sentences.pop(0)
le = preprocessing.LabelEncoder()
le.fit(labels)
labels = list(le.transform(labels))
print(labels)

tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[labels[i]]) for i, _d in enumerate(sentences)]

max_epochs = 10
vec_size = 300
alpha = 0.025

model = Doc2Vec(size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                dm =1)
model.build_vocab(tagged_data)
for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha
vecs = []
for label in labels:
    vecs.append(model.docvecs[label])
tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)
new_values = tsne.fit_transform(vecs)
x = []
y = []
for value in new_values:
    x.append(value[0])
    y.append(value[1])

#colors = cm.hsv(np.linspace(0, 1, len(np.unique(labels))))
#print(colors)
    
plt.figure(figsize=(16, 16)) 
#for i in range(len(x)):
plt.scatter(x,y, c = labels, cmap = cm.get_cmap('hsv'))
"""
    plt.annotate(labels[i],
                 xy=(x[i], y[i]),
                 xytext=(5, 2),
                 textcoords='offset points',
                 ha='right',
                 va='bottom')
"""
plt.show()
plt.savefig('./fig.png')

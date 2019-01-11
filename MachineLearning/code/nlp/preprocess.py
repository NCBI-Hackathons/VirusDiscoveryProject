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
import csv

def doc2vec_method(sentences):
    tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[i]) for i, _d in enumerate(sentences)]

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
    return model

#input_file = "../../../../data/total_metadata.csv"
input_file = "../../../../data/SRA.all_SRR.csv"
sentences = []
labels = []
with open(input_file, 'r') as f:
    csvreader = csv.reader(f, delimiter=',', quotechar='"')
    for l in csvreader:
        labels.append(l[9])
        sentences.append(' '.join(l[0:9] + l[10:]))
labels.pop(0)
sentences.pop(0)

hgm_labels = []
for l in labels:
    if "human gut metagenome" in l:
        hgm_labels.append(0)
    elif "NA" in l or "None" in l:
        hgm_labels.append(1)
    else:
        hgm_labels.append(2)
#print(sentences)
print(hgm_labels)

model = doc2vec_method(sentences)

vecs = []
for label in hgm_labels:
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
    
plt.figure(figsize=(8, 8)) 
colors = ['red', 'blue', 'orange']
colorlabels = ['human gut microbiome', 'NA', 'Other']
for i in range(len(x)):
    plt.scatter(x[i],y[i], color=colors[hgm_labels[i]])

plt.legend(colorlabels)
plt.title("t-SNE of metadata transformed by doc2vec")
plt.show()
plt.savefig('./fig1.png')

#Remove NA's
hgm_labels = []
new_sentences = []
for i, l in enumerate(labels):
    if "human gut metagenome" in l:
        hgm_labels.append(1)
        new_sentences.append(sentences[i])
    elif "NA" in l or "None" in l:
        continue
    else:
        hgm_labels.append(0)
        new_sentences.append(sentences[i])
model = doc2vec_method(new_sentences)
vecs = []
for label in hgm_labels:
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

plt.figure(figsize=(8, 8))
colors = ['red', 'blue']
colorlabels = ['Other', 'Human Gut Microbiome']
for i in range(len(x)):
    plt.scatter(x[i],y[i], color=colors[hgm_labels[i]])

plt.legend(colorlabels)
plt.title("t-SNE of metadata transformed by doc2vec with NA's removed")
plt.show()
plt.savefig('./fig2.png')

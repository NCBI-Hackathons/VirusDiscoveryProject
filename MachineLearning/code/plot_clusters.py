import json
import matplotlib.pyplot as plt
import numpy as np

with open('wordFreq2MASHgroups.json') as f:
    data = json.load(f)

name = 'X6'
blacklist = ['both', 'can', 'using','be', 'been', 'fmt', 'stec', 'd', 'of', 'the', 'with', 'and', 'in', 'a', 'an', 'to', 'from', 'for', 'we', 'on', 'that', 'is', 'by', 'are', 'were', 'as']
fig = plt.figure(figsize=(16, 12))
axes = fig.subplots(4, 1, sharex=False, sharey=False)

for i, cluster in enumerate(data['X6']):
    ax = axes[i]
    words = data['X6'][cluster]['words']
    vals = data['X6'][cluster]['cummulative_frequency']
    #print(vals)
    #print(words)
    top_vals = []
    top_words = []
    count = 0
    for j, word in enumerate(words):
        if word not in blacklist:
            top_words.append(word)
            top_vals.append(float(vals[j]))
            count += 1
        if count == 10:
            break
    print(top_words)
    index = np.arange(10)
    ax.bar(top_words, top_vals)
    if i == 0:
        ax.set_title("Cumulative Frequencies of words found in metadata across MASH clusters")
    ax.set_ylabel("Cumulative Frequencies")
    if i == 3:
        ax.set_xlabel("Words")
    #ax.set_xticks(index, top_words)
plt.savefig('./clusters.pdf')

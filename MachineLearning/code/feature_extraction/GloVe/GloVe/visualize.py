#!/usr/bin/env python
# encoding: utf-8


import numpy as np
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

name = 'SNEDE0000EPH'

def cooc():
    X = np.load('../data/%s_6gram_2stride_cooccurrence.npy' % name)
    print 'cooccurrence loaded...'
    X = X[2:, 2:] # except 'none'
    print X.shape
    f = plt.figure(figsize=(6.2, 5.6))
    ax = f.add_axes([0.06, 0.07, 0.8, 0.8])
    axcolor = f.add_axes([0.87, 0.07, 0.04, 0.8])
    im = ax.matshow(X, norm=LogNorm())
    t = [0.1, 1, 10, 100, 1000]
    f.colorbar(im, cax=axcolor, ticks=t, format='$%.1f$')
    f.savefig('./cooc.pdf')
    print 'cooccurrence pdf saved...'

def vocab():
    f = open('../data/%s_6gram_2stride_vocab.txt' % name, 'r')
    lines = f.readlines()
    V = [int(x[:-1].split()[1]) for x in lines]
    V = V[1:] # except 'none'
    print 'vocabulary loaded...'
    print len(V)
    plt.figure()
    plt.plot(V)
    plt.xlabel('Vocabulary (frequency ordered)')
    plt.ylabel('Frequency')
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
    plt.savefig('./vocab.pdf')
    print 'vocabulary pdf saved...'

def tsne():
    try:
        vecs_2d = np.load('../data/%s_6gram_2stride_vectors_2d.npy' % name)
    except:
        from sklearn.manifold import TSNE
        f = open('../data/%s_6gram_2stride_vectors.txt' % name, 'r')
        lines = f.readlines()
        vecs = []
        for line in lines[1:]:
            vecs.append([float(x) for x in line[:-1].split()[1:] ])
        vecs = np.array(vecs)
        print vecs, vecs.shape
        model = TSNE(n_components=2, random_state=0)
        vecs_2d = model.fit_transform(vecs)
        np.save('../data/%s_6gram_2stride_vectors_2d' % name, vecs_2d)
    print vecs_2d
    xs = vecs_2d[:, 0]
    ys = vecs_2d[:, 1]
    print xs, ys
    plt.figure()
    plt.scatter(xs, ys, '.')
    plt.savefig('./vectors_2d.pdf')


def vectors():
    f = open('../data/%s_6gram_2stride_vectors.txt' % name, 'r')
    lines = f.readlines()
    vecs = []
    for line in lines[1:]:
        vecs.append([float(x) for x in line[:-1].split()[1:] ])
    vecs = np.array(vecs)
    print 'vectors loaded...'
    print vecs.shape
    f = plt.figure(figsize=(13,5))
    ax = f.add_axes([0.02,0.07,0.92,0.85])
    ax_color = f.add_axes([.92,0.07,0.03,0.85])
    im = ax.matshow(vecs.T, aspect=16)
    f.colorbar(im, cax=ax_color)
    ax.set_xlabel('Vocabulary (frequency ordered)')
    ax.set_ylabel('Vector dimension')
    f.savefig('./vectors.pdf')
    print 'vectors pdf saved...'

def histos():
    auroc_i_t = [0.8830, 0.88178, 0.9249, 0.9031]
    auprc_i_t = [0.8774, 0.87418, 0.91948, 0.9008]
    auroc_i_n = [0.86799, 0.85392, .88562, .88226]
    auprc_i_n = [.86138, .84374, .8796, .8819]
    auroc_n = [.86049, .85581, .8997, .87199]
    auprc_n =[.85091, .84381, .89078, .86475]

    N = 4
    ind = np.arange(N)
    width = 0.14
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, auroc_i_t, width, color='r', linewidth=0.8)
    rects2 = ax.bar(ind+width, auroc_i_n, width, color='r', hatch='//', linewidth=0.8)
    rects3 = ax.bar(ind+2*width, auroc_n, width, color='r', hatch='\\\\', linewidth=0.8)
    rects4 = ax.bar(ind+3*width, auprc_i_t, width, color='b', linewidth=0.8)
    rects5 = ax.bar(ind+4*width, auprc_i_n, width, color='b', hatch='//', linewidth=0.8)
    rects6 = ax.bar(ind+5*width, auprc_n, width, color='b', hatch='\\\\', linewidth=0.8)

    ax.set_ylim((0.7,1.0))
    ax.set_xlim((-0.2, 4.2-(1-6*width)))
    ax.set_ylabel('auc scores')
    ax.set_xticks(ind+3*width)
    ax.set_xticklabels(('GM12878', 'K562', 'MCF-7', 'HeLa-S3'))
    ax.legend((rects1[0], rects2[0], rects3[0], rects4[0], rects5[0], rects6[0]),
              ('auROC -init -train', 'auROC -init -notrain', 'auROC -noinit',
               'auPRC -init -train', 'auPRC -init -notrain', 'auPRC -noinit'),
              loc=0)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%.3f' % height,
                    ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('./histo.pdf', dpi=50)

if __name__ == '__main__':
    # cooc()
    # vocab()
    # tsne()
    # vectors()
    histos()


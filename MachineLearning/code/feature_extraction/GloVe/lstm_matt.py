#!/usr/bin/env python
# encoding: utf-8

import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Bidirectional
from keras.layers import Convolution1D, MaxPooling1D
from keras.layers.embeddings import Embedding
from keras.callbacks import ModelCheckpoint, EarlyStopping

from sklearn import metrics
np.random.seed(12345)

import argparse

def get_args():
    parser = argparse.ArgumentParser(description='embedconvlstm training')
    parser.add_argument('-gpu', dest='gpu', type=int, default=5, help='using which gpu')
    parser.add_argument('-k', dest='k', type=int, default=6, help='length of kmer')
    parser.add_argument('-s', dest='s', type=int, default=2, help='stride of splitting')
    parser.add_argument('-batchsize', dest='batchsize', type=int, default=2000, help='size of one batch')
    parser.add_argument('-init', dest='init', action='store_true', default=True, help='initialize vector')
    parser.add_argument('-noinit', dest='init', action='store_false', help='no initialize')
    parser.add_argument('-trainable', dest='trainable', action='store_true', default=True, help='embedding vectors trainable')
    parser.add_argument('-notrainable', dest='trainable', action='store_false', help='not trainable')
    parser.add_argument('-test', dest='test', action='store_true', default=False, help='only test step')
    parser.add_argument('-combined', dest='combined', action='store_true', default=False, help='whether to use the pos+neg combined vector file')
    parser.add_argument('-total', dest='total', action='store_true', default=False, help='whether the traing data is for total')
    parser.add_argument('-iteration', type=int, dest='iteration', default=1, help='which fold')
    parser.add_argument('-indir', dest='in_dir', help='directory where pos and neg are stored')
    parser.add_argument('-pospath', dest='pos_path', help='path to positive kmer/step file')
    parser.add_argument('-negpath', dest='neg_path', help='path to negative kmer/step file')
    parser.add_argument('-window', dest='window', type=int, default=-1, help='size of window for glove')
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    run_everything(**args.__dict__)

def load_data(pos_path, neg_path, NB_WORDS, MAX_LEN, k, s, in_dir):
    print('Loading seq data from {} and {}'.format(pos_path, neg_path))
    pos_seqs = [line[:-2] for line in open('%s' % pos_path) if len(line.split())>15]
    neg_seqs = [line[:-2] for line in open('%s' % neg_path) if len(line.split())>15]
    seqs = pos_seqs + neg_seqs
    lens = [len(line.split()) for line in seqs]
    n_seqs = len(lens)
    print('there are %d sequences' % n_seqs)
    print('  containing %d-mers statistics:' % k)
    print('  max ', np.max(lens))
    print('  min ', np.min(lens))
    print('  mean ', np.mean(lens))
    print('  25% ', np.percentile(lens, 25))
    print('  50% ', np.median(lens))
    print('  75% ', np.percentile(lens, 75))
    y = np.array([1] * len(pos_seqs) + [0] * len(neg_seqs))

    print('Tokenizing seqs...')
    #tokenizer = Tokenizer(nb_words=NB_WORDS)
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(seqs)
    sequences = tokenizer.texts_to_sequences(seqs)
    X = pad_sequences(sequences, maxlen=MAX_LEN)

    kmer_index = tokenizer.word_index
    print('Found %s unique tokens.' % len(kmer_index))

    print('Spliting train, valid, test parts...')
    indices = np.arange(n_seqs)
    np.random.shuffle(indices)
    X = X[indices]
    y = y[indices]
    return X, y, kmer_index, n_seqs

def run_everything(gpu, k, s, batchsize, init, trainable, test, combined, total, iteration, in_dir, pos_path, neg_path, window):
    NB_WORDS = 20000
    MAX_LEN = 3000
    file_type = ""
    """ 
    vector_name = ''
    if total and combined:
        vector_name = 'gv_PBSIM_total.fastq'
    elif total and not combined:
        vector_name = 'girus_PBSIM_total.fastq'
    elif not total and combined:
        vector_name = 'gv_PBSIM_train.fastq'
    elif not total and not combined:
        vector_name = 'girus_PBSIM_train.fastq'
    print('vector name = {}'.format(vector_name))
    """
    X_train, y_train, kmer_index_train, n_seqs_train = load_data(pos_path, neg_path, NB_WORDS, MAX_LEN, k, s)
    print("kmer_index_train len = {}".format(len(kmer_index_train)))
    n_tr = int(n_seqs_train * 0.90)
    n_va = n_seqs_train - n_tr
    print("n_tr = {}\tn_va = {}".format(n_tr, n_va))
    X_valid = X_train[-n_va:]
    y_valid = y_train[-n_va:]
    X_train = X_train[:n_tr]
    y_train = y_train[:n_tr]
    """
    n_tr = int(n_seqs_train * 0.85)
    n_va = int(n_seqs_train * 0.05)
    n_te = n_seqs_train - n_tr - n_va
    X_valid = X_train[n_tr:n_tr+n_va]
    y_valid = y_train[n_tr:n_tr+n_va]
    X_test = X_train[-n_te:]
    y_test = y_train[-n_te:]
    X_train = X_train[:n_tr]
    y_train = y_train[:n_tr]
    """
    print("y_train len = {}\ty_valid len = {}".format(len(y_train), len(y_valid)))
    pos_name_test = '{}_test_{}.fasta'.format(pos_name, iteration)
    neg_name_test = '{}_test_{}.fasta'.format(neg_name, iteration)
    X_test, y_test, kmer_index_test, n_seqs_test = load_data(pos_name_test, neg_name_test, NB_WORDS, MAX_LEN, k, s, in_dir)
    embedding_vector_length = 100
    #nb_words = min(NB_WORDS, len(kmer_index_train)) # kmer_index starting from 1
    nb_words = len(kmer_index_train)
    print('Building model...')
    model = Sequential()
    if init:
        print('initialize embedding layer with glove vectors from %s/%s_%dgram_%dstride_vectors.txt' % (in_dir, pos_name_train, k, s))
        kmer2vec={}
        if window is -1:
            f = open('%s_vectors.txt' % (in_dir, pos_name_train, k, s))
        else:
            f = open('%s_%dwindow_vectors.txt' % (in_dir, pos_name_train, k, s, window))
        for line in f:
            values = line.split()
            try:
                kmer = values[0]
                coefs = np.asarray(values[1:], dtype='float32')
                kmer2vec[kmer] = coefs
            except:pass
        f.close()
        embedding_matrix = np.zeros((nb_words+1, embedding_vector_length))
        for kmer, i in kmer_index_train.items():
            #if i > NB_WORDS:
            #    continue
            vector = kmer2vec.get(kmer)
            if vector is not None:
                embedding_matrix[i] = vector

        print('embedding layers trainable %s' % trainable)
        model.add(Embedding(nb_words+1,
                            embedding_vector_length,
                            weights=[embedding_matrix],
                            input_length=MAX_LEN,
                            trainable=trainable))
    else:
        model.add(Embedding(nb_words+1,
                            embedding_vector_length,
                            input_length=MAX_LEN))
    model.add(Dropout(0.2))
    model.add(Convolution1D(100, 10, activation='relu'))
    model.add(MaxPooling1D(4, 4))
    model.add(Dropout(0.2))
    model.add(Convolution1D(100, 8, activation='relu'))
    model.add(MaxPooling1D(2, 2))
    model.add(Dropout(0.2))
    model.add(Convolution1D(80, 8, activation='relu'))
    model.add(MaxPooling1D(2, 2))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(80)))
    model.add(Dropout(0.2))
    model.add(Dense(20, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    print(model.summary())

    if not test:
        checkpointer = ModelCheckpoint(filepath="./model/%s_bestmodel_%dgram_%dstride_%sinit_%strainable_%stotal_%scombined_%dwindow.hdf5"
                                       % (pos_name_train, k, s, init, trainable, total, combined, window), verbose=1, save_best_only=True)
        earlystopper = EarlyStopping(monitor='val_loss', patience=6, verbose=1)

        print('Training model...')
        model.fit(X_train, y_train, nb_epoch=60, batch_size=batchsize, shuffle=True,
                  validation_data=(X_valid, y_valid),
                  callbacks=[checkpointer,earlystopper],
                  verbose=1)

    print('Testing model...')
    model.load_weights('./model/%s_bestmodel_%dgram_%dstride_%sinit_%strainable_%stotal_%scombined_%dwindow.hdf5'
                       % (pos_name_train, k, s, init, trainable, total, combined, window))
    tresults = model.evaluate(X_test, y_test)
    print(tresults)
    y_pred = model.predict(X_test, batch_size=batchsize, verbose=1)
    y = y_test
    print('Calculating AUC...')
    auroc = metrics.roc_auc_score(y, y_pred)
    auprc = metrics.average_precision_score(y, y_pred)
    print(auroc, auprc)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# encoding: utf-8

import numpy as np
from preprocess import *
import argparse
import os
import sys

def get_args():
    parser = argparse.ArgumentParser(description='Generate k-mers and GloVe vectors')
    parser.add_argument('-k', dest='k', type=int, default=6, help='length of kmer')
    parser.add_argument('-s', dest='s', type=int, default=2, help='stride of splitting')
    parser.add_argument('-infile', dest='in_file', help='path to fasta file containing sequences to k-merize')
    parser.add_argument('-glove', dest='glove', help='whether to generate the 1-line corpus for GloVe') 
    parser.add_argument('-w', dest='work_dir', help='path to working (in and out) directory')
    args = parser.parse_args()
    return args

def main():
    args = get_args()
    out_name = os.path.splitext(args.in_file)[0]
    seq2kmer('%s' % args.in_file, args.k, args.s, '%s_%dkmer_%dstep' % (out_name, args.k, args.s))
    corpus('%s_%dkmer_%dstep' % (out_name, args.k, args.s),
                 '%s_%dkmer_%dstep_oneline' % (out_name, args.k, args.s))

def seq2kmer(seqs, k, s, dest):
    with open(seqs, 'r') as f:
        out = open(dest, 'w')
        for num, line in enumerate(f):
            if num % 1000 == 0:
                print('%d lines to kmers' % num)
            if num % 2 == 0:
                continue
            line = line[:-1]
            l = len(line) # length of line
            for i in range(0, l-k+1, s):
                out_line = "%s " % ''.join(line[i:i+k])
                out.write(out_line)
            out.write('\n')
    out.close()

def corpus(f, dest):
    f = open(f)
    with open(dest, 'w') as out:
        for num, line in enumerate(f):
            if num % 1000 == 0:
                print('%d lines saved' % num)
            out.write(line[:-1])
            out.write('none ' * 5)
    f.close()


if __name__ == "__main__":
    main()

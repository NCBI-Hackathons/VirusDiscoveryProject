#!/usr/bin/env python3
#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description  TETS ERR1874157.realign
#  -------------------------------------------------------------------------------


import io
import os
import sys
import subprocess
import math

class FastaReader:

  class Sequence:

    def __init__(self, header=None):
      self.header = header
      self.seq = ''
      self.shannon = 0.0
      self.charfreqs = {}

    def get_shannon(self):
      for i in self.charfreqs:
        self.shannon += self.charfreqs[i] * math.log2(self.charfreqs[i])
      return abs(self.shannon)

    def add_seq(self, seq):
      for i in seq:
        if i not in self.charfreqs:
          self.charfreqs[i] = 0
        self.charfreqs[i] += 1
      self.seq += seq

    def dump_fasta(self):
      return ">{}\n{}".format(self.header, self.seq)

  def __init__(self):
    self.min_seqlen = 1000
    self.min_shannon_metric = 0.7

  def read(self):
    s = None
    for i in sys.stdin:
      if i[0] == '>':
        if not s:
          s = FastaReader.Sequence(i[1:].rstrip())
        else:
          if len(s.seq) >= self.min_seqlen:
            print(s.dump_fasta())
          s = FastaReader.Sequence(i[1:].rstrip())
      else:
        s.add_seq(i.strip())
    if (len(s.seq) >= self.min_seqlen) and (s.get_shannon() >= self.min_shannon_metric):
      print(s.dump_fasta())

def main():
  fr = FastaReader()
  fr.read()
  return 0

if __name__ == '__main__':
  main()

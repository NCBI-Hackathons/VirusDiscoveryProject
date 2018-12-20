#!/usr/bin/env python3
#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------


import io
import os
import sys
import argparse

import itree
import interval

class LineSplitter:

  class Columns:

    def __init__(self, query, db, subject, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore):
      self.query = query
      self.db = db
      self.subject = subject
      self.pident = pident
      self.length = length
      self.mismatch = mismatch
      self.gapopen = gapopen
      self.qstart = qstart
      self.qend = qend
      self.sstart = sstart
      self.send = send
      self.evalue = evalue
      self.bitscore = bitscore

  def __init__(self, sep):
    self.sep = sep

  def split(self, line):
    raise NotImplementedError("Help! Need implementation")


class RpstblastnSplitter(LineSplitter):

  def __init__(self, sep='\t'):
    super().__init__(sep)

  def split(self, line):
    cols = line.split(self.sep)
    db, subject = cols[1].split(':')
    return self.Columns(cols[0], db, subject, cols[2], cols[3], cols[4],
                        cols[5], cols[6], cols[7], cols[8], cols[9], cols[10],
                        cols[11])

class Contig:

  def __init__(self, name, srr):
    self.name = name
    self.srr = srr
    self.itree = itree.IntervalTree()

  def add_interval(self, interval):
    self.itree.collect_interval(interval)

  def build_itree(self):
    self.itree.build()

  def score(self):
    for i in self.itree.nodes:
      print(self.srr, self.name, self.itree.nodes[i].id, self.itree.nodes[i].beg, self.itree.nodes[i].end, len(self.itree.nodes[i].intervals))

def make_dot(contigs, srr):
  print("graph \"\"\n{")
  print("label=\"{}\"".format(srr))
  ctg_count = 0
  for i in contigs:
    ctg = i.name.replace(':', '_').replace('.', '_')
    print("subgraph cluster{0}".format(ctg_count))
    print("{")
    print("label=\"{}\"".format(ctg))
    for j in i.itree.nodes:
      print("{0}{1} [label=\"id: {1}\lival: {2}-{3}\lmedian: {4}\lroot: {5}\l\"] ;".format(ctg_count, i.itree.nodes[j].id, i.itree.nodes[j].beg,i.itree.nodes[j].end, i.itree.nodes[j].median, i.itree.nodes[j].root.id))
      if i.itree.nodes[j].left:
        print("{0}{1} -- {0}{2}".format(ctg_count, i.itree.nodes[j].id, i.itree.nodes[j].left.id))
      if i.itree.nodes[j].right:
        print("{0}{1} -- {0}{2}".format(ctg_count, i.itree.nodes[j].id, i.itree.nodes[j].right.id))
    print("}")
    ctg_count += 1
  print("}")

def set_splitter(blast_typ):
  if blast_typ == 'rpstblastn':
    return RpstblastnSplitter()

def main():
  ap = argparse.ArgumentParser(description='Read BLAST[?] flat files fof novel analysis')
  ap.add_argument('-s',
                  '--sep',
                  type=str,
                  help='Field separator')
  ap.add_argument('--srr',
                  type=str,
                  required=True,
                  help='SRR accession')
  ap.add_argument('-b',
                  '--blast',
                  type=str,
                  required=True,
                  help='Blast type: {t}blast{n,x}, rpstblastn')
  args = ap.parse_args()

  s = set_splitter(args.blast)
  contigs = []
  for i in sys.stdin:
    cols = s.split(i.rstrip())
    if not contigs:
      contigs.append(Contig(cols.query, args.srr))
    if cols.query != contigs[-1].name:
      contigs[-1].build_itree()
      contigs.append(Contig(cols.query, args.srr))
    contigs[-1].add_interval(interval.Interval(cols))
  contigs[-1].build_itree()
  #make_dot(contigs, args.srr) SRR918250
  for i in contigs:
    i.score()
  return 0


if __name__ == '__main__':
  main()

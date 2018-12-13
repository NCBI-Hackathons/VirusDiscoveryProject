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

sys.path.insert(1, os.path.join(sys.path[0], '../../include/entrezpy/src'))
import wally.wally

class CddExplainer:

  class CddResult:

    def __init__(self, contig, db, hit):
      self.srr = None
      self.contig = contig
      self.db = db
      self.hit = hit

  def __init__(self, email):
    self.contigs = {}
    self.hits = {}
    self.email = email

  def parse_result(self):
    for i in sys.stdin:
      cols = i.split()
      db, hit = cols[1].split(':')
      if cols[0] not in self.contigs:
        self.contigs[cols[0]] = self.CddResult(cols[0], db, hit)
      if db not in self.hits:
        self.hits[db] = {}
      self.hits[db][hit] = 0

  def summarize_hits(self):
    header = ['db', 'uid', 'accession', 'database', 'organism', 'title', 'subtitle']
    w = wally.wally.Wally(self.email)
    for i in self.hits:
      pl = w.new_pipeline()
      qid = pl.add_summary({'db':i, 'id': [x for x in self.hits[i]]})
      a = w.run(pl)
      print('\t'.join(x for x in header[1:]))
      for i in a.result.summaries:
        print('\t'.join(a.result.summaries[i][x] for x in header[1:]))

def main():
  ap = argparse.ArgumentParser(description='Novel result summarizer')
  ap.add_argument('-e','--email', type=str, help='Email required by Edirect')
  args = ap.parse_args()
  c = CddExplainer(args.email)
  c.parse_result()
  c.summarize_hits()
  return 0


if __name__ == '__main__':
  main()

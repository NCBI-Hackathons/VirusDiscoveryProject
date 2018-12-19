#!/usr/bin/env python3
#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------


import io
import os
import sys

import itree
import interval

class Contig:

  def __init__(self, name, srr):
    self.name = name
    self.srr = srr
    self.itree = itree.IntervalTree()
    self.intervals = 0

  def add_interval(self, interval):
    self.itree.collect_interval(interval)
    self.intervals += 1

  def build_itree(self):
    self.itree.build()

def main():
  contig = None
  srr = "SRR918250"
  for i in sys.stdin:
    cols = i.split()
    if not contig:
      contig = Contig(cols[0], srr)
    if cols[0] != contig.name:
      print(contig.name)
      contig.build_itree()
      print("==============")
      contig = Contig(cols[0], srr)
      contig.add_interval(interval.Interval(cols[0], cols[1], cols[6], cols[7]))
    else:
      contig.add_interval(interval.Interval(cols[0], cols[1], cols[6], cols[7]))
  print(contig.name)
  contig.build_itree()
  return 0


if __name__ == '__main__':
  main()

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

def main():
  t = itree.IntervalTree()
  for i in sys.stdin:
    cols = i.split()
    t.collect_interval(interval.Interval(cols[0], cols[1], cols[6], cols[7]))
  t.build()
  return 0


if __name__ == '__main__':
  main()

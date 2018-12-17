#!/usr/bin/env python3
#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------


import io
import os
import sys
import math

class IntervalTree:

  class Node:

    def __init__(self, median):
      self.median = median
      self.intervals = []
      self.left = []
      self.right = []

  def __init__(self):
    self.ivals = []
    self.end_coords = set()

  def collect_interval(self, interval):
    self.ivals.append(interval)
    self.end_coords.add(interval.end)

  def build(self):
    self.ivals.sort(key=lambda x:x.end)
    sorted_ivals = sorted(self.end_coords)
    median_idx = math.floor(len(sorted_ivals)/2) - 1
    print(sorted_ivals[median_idx])
    self.add_node(self.ivals)

  def calc_median(self, ivals):
    prev_val = 0
    uniq = []
    for i in ivals:
      if i.end != prev_val:
        uniq.append(i)
      prev_val = i.end
    return uniq[math.floor(len(uniq)/2)-1].end

  def add_node(self, ivals):
    if not ivals:
      return None
    n = self.Node(self.calc_median(ivals))
    for i in ivals:
      if i.beg <= n.median and i.end >= n.median:
        n.intervals.append(i)
      elif i.end < n.median:
        n.left.append(i)
      elif i.beg > n.median:
        n.right.append(i)
      else:
        sys.exit("Should never happen")

    print("left")
    for i in n.left:
      print(i.dump())
    print("center")
    for i in n.intervals:
      print(i.dump())
    print("right")
    for i in n.right:
      print(i.dump())

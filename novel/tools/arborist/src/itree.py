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
import uuid

class IntervalTree:

  class Node:

    def __init__(self, median, root):
      self.id = None
      self.uuid = str(uuid.uuid4())
      self.root = root
      self.median = median
      self.beg = median
      self.end = 0
      self.intervals = []
      self.left = []
      self.right = []

    def dump(self):
      return {'median':self.median, 'left':self.left, 'right': self.right}

  def __init__(self):
    self.ivals = []
    self.end_coords = set()
    self.node_count = 0
    self.nodes = []

  def collect_interval(self, interval):
    self.ivals.append(interval)
    self.end_coords.add(interval.end)

  def build(self):
    self.ivals.sort(key=lambda x:x.end)
    n = self.add_node(self.ivals)
    if not n:
      print("Done")
    else:
      print(n, n.median)
    #while root:
      #print(nd.median)
      #for i in nd.right:
        #print(i.dump())
      #root =


  def calc_median(self, ivals):
    prev_val = 0
    uniq = []
    for i in ivals:
      if i.end != prev_val:
        uniq.append(i)
      prev_val = i.end
    return uniq[math.floor(len(uniq)/2)-1].end

  def add_node(self, ivals, root=None):
    if not ivals:
      return None
    n = self.Node(self.calc_median(ivals), root)
    n.id = self.node_count
    for i in ivals:
      if i.beg <= n.median and i.end >= n.median:
        if i.beg < n.beg:
          n.beg = i.beg
        if i.end > n.end:
          n.end = i.end
        n.intervals.append(i)
      elif i.end < n.median:
        n.left.append(i)
      elif i.beg > n.median:
        n.right.append(i)
      else:
        sys.exit("Should never happen")
    print("Node", n, n.id, n.median, n.root, n.beg, n.end, len(n.intervals))
    self.nodes.append(n)
    self.node_count += 1
    self.add_node(n.left, n)
    self.add_node(n.right, n)
    return n

    #print(n.median)
    #print("left")
    #for i in n.left:
      #print(i.dump())
    #print("center")
    #for i in n.intervals:
      #print(i.dump())
    #print("right")
    #for i in n.right:
      #print(i.dump())
    #return n

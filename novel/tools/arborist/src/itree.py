#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#-------------------------------------------------------------------------------

import sys
import math

class IntervalTree:

  class Node:

    node_count = 0

    def __init__(self, median, root):
      self.id = IntervalTree.Node.node_count
      self.root = self if not root else root
      self.median = median
      self.beg = median
      self.end = 0
      self.intervals = []
      self.left = None
      self.right = None
      IntervalTree.Node.node_count += 1

    def dump(self):
      return {'id':self.id, 'self':self, 'median':self.median, 'root': self.root.id, 'ivals':self.intervals,
              'left':self.left, 'right': self.right}

  def __init__(self):
    self.ivals = []
    self.nodes = {}
    self.Node.node_count = 0

  def collect_interval(self, interval):
    self.ivals.append(interval)

  def build(self):
    self.ivals.sort(key=lambda x:x.end)
    return self.add_node(self.ivals)

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
    self.nodes[n.id] = n
    left = []
    right = []
    for i in ivals:
      if i.beg <= n.median and i.end >= n.median:
        if i.beg < n.beg:
          n.beg = i.beg
        if i.end > n.end:
          n.end = i.end
        n.intervals.append(i)
      elif i.end < n.median:
        left.append(i)
      elif i.beg > n.median:
        right.append(i)
      else:
        sys.exit("Should never happen")
    self.nodes[n.id].left = self.add_node(left, n)
    self.nodes[n.id].right = self.add_node(right, n)
    #print(n.dump())
    return n

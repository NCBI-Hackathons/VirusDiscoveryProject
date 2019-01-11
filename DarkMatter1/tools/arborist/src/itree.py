#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#-------------------------------------------------------------------------------

import sys
import math

"""
In interval tree to store and acore results from SRR contig screens. Each hit
in a database search produces an interval (the hit). Intervals are sorted
with increasing end position of the hit on the contig.

The median of unique end positions is selected as root. All intervals containing
the end are stored in this node. All intervals with end coordinates lower than
the median are stored as left while intervals with start coordinates bigger than
the median are stored on the right.

Each node is visited recursivly and subdied as described as above.

Currently, no fancy stuff like overlap meging etc. is performed.

An selection of some interval trees can be found in the doc direcotry.
"""
class IntervalTree:

  """
    Node implementation for the interval tree.
    A node has a median and holds all intervals containing this median.
    left and right point to the nodes with lower and higher median,
    respecitvely.
  """
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
    """
    Start building the interval tree. Sort intervals here avoids to
    sort at every step.
    :return: root node of interval tree
    :rtype: Node()
    """
    self.ivals.sort(key=lambda x:x.end)
    return self.add_node(self.ivals)

  def calc_median(self, ivals):
    """
    Calculate end position of median interval from list of current intervals.
    :param ivals: list of interval.Interval()
    :return: end coordinate of median interval
    :rtype: int
    """
    prev_val = 0
    uniq = []
    for i in ivals:
      if i.end != prev_val:
        uniq.append(i)
      prev_val = i.end
    return uniq[math.floor(len(uniq)/2)-1].end

  def add_node(self, ivals, root=None):
    """
    Recursively add nodes with intervals to the interval tree.
    :param ivals: list of intervals at this point
    :param root: ancestor node
    :return: node with median and intervals containing the median
    :rtype: Node()
    """
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

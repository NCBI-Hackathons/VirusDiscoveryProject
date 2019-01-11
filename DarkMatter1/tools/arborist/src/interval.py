#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  -------------------------------------------------------------------------------

"""
Interval class to store values from blast results. They can be accessed later
from nodes and scored based on their attributes.
"""
class Interval:

  def __init__(self, cols):
    self.hit = cols.subject
    self.db = cols.db
    self.pident = cols.pident
    self.length = cols.length
    self.mismatch = cols.mismatch
    self.gapopen = cols.gapopen
    self.evalue = cols.evalue
    self.bitscore = cols.bitscore
    self.beg = int(cols.qstart)
    self.end = int(cols.qend)
    if int(cols.qstart) > int(cols.qend):
      self.beg = int(cols.qend)
      self.end = int(cols.qstart)

  def dump(self):
    return {'beg': self.beg, 'end': self.end, 'hit':self.hit, 'db':self.db}

class VigoInterval:

  def __init__(self, cols):
    self.contig = cols.contig
    self.proteinid = cols.proteinid
    self.descr = cols.descr
    self.sources = {}
    self.beg = int(cols.beg)
    self.end = int(cols.end)
    if int(cols.beg) > int(cols.end):
      self.beg = int(cols.beg)
      self.end = int(cols.end)

  def add_source(self, source):
    self.sources[source.name] = source

  def dump(self):
    return {'beg': self.beg, 'end': self.end, 'hit':self.hit, 'db':self.db}

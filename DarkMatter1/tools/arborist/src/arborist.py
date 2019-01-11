#!/usr/bin/env python3
#-------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#-------------------------------------------------------------------------------

import sys
import argparse

import itree
import interval

"""
Base class to handle different Blast results and types.
split() needs to be implemented to create an uniform approach for Intervals
"""
class LineSplitter:


  class Columns:
    """
    Store the columns/fields ina flat file blast result as struct
    """
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

  class VigoSource:

    def __init__(self, name, percid, perccov, evalue):
      self.name = name
      self.percid = percid
      self.perccov = perccov
      self.evalue = evalue

  class VigoColumns:
    """
    Store the columns/fields ina flat file blast result as struct
    """
    def __init__(self, contig, proteinid, start, stop, descr):
      self.contig = contig
      self.proteinid = proteinid
      self.descr = descr
      self.beg = int(start)
      self.end = int(stop)

  def __init__(self, sep):
    self.sep = sep

  """
  Virtual method to accomodate quirks and weird formatting issues encountered in
  Blast results.
  :param: result line
  :return: Column()
  """
  def split(self, line):
    raise NotImplementedError("Help! Need implementation")

class RpstblastnSplitter(LineSplitter):
  """
  Class to handle rpstblastn -outfmt 6 result files
  :param sep: field separator
  """
  def __init__(self, sep='\t'):
    super().__init__(sep)

  """
  Implemented virtual split method to extratc CDD accession form blast results.
  """
  def split(self, line):
    cols = line.split(self.sep)
    db, subject = cols[1].split(':')
    return interval.Interval(self.Columns(cols[0], db, subject, cols[2], cols[3], cols[4],
                        cols[5], cols[6], cols[7], cols[8], cols[9], cols[10],
                        cols[11]))

class VigoSplitter(LineSplitter):
  """
  Class to handle rpstblastn -outfmt 6 result files
  :param sep: field separator
  """
  def __init__(self, sep='\t'):
    super().__init__(sep)

  """
  Implemented virtual split method to extratc CDD accession form blast results.
  """
  def split(self, line):
    cols = line.split(self.sep)
    ival = interval.VigoInterval(self.VigoColumns(cols[0], cols[1], cols[2], cols[3], cols[9]))
    if cols[10] != "NA":
      ival.add_source(self.VigoSource(cols[10], cols[11], cols[12], cols[13]))
    if cols[15] != "NO":
      ival.add_source(self.VigoSource(cols[15], cols[16], cols[17], cols[18]))
    return ival

class Contig:
  """
  Class to handle individual contings from a SRR.contigs file and corresponding
  interval tree.
  :param name: contig name
  :param srr: SRR accession
  """
  def __init__(self, name, srr):
    self.name = name
    self.srr = srr
    self.itree = itree.IntervalTree()

  """
  Add interval to interval tree
  :param interval: Interval()
  """
  def add_interval(self, interval):
    self.itree.collect_interval(interval)

  """
  Build interval tree after parsing all hits for one contig
  """
  def build_itree(self):
    self.itree.build()

  """
  Scoring function for contig. Currently more proof of concept.
  """
  def score(self):
    for i in self.itree.nodes:
      print(self.srr, self.name, self.itree.nodes[i].id, self.itree.nodes[i].beg, self.itree.nodes[i].end, len(self.itree.nodes[i].intervals))

"""
Quick and dirty function to dump intervals in dot to pot with graphviz, e.g.
dot -Tpdf.
It makes sens eot limit the number of contigs since this will blow up if a whole
SRR is plotted.
head -n 100 unk_test_rpstbln_fullCD_eval3.tab | arborist/src/arborist.py -b rpstblastn --srr SRR918250 | dot -Tpdf > SRR918250.itree.pdf
"""
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
      print("{0}{1} [label=\"id: {1}\lival: {2}-{3}\lmedian: {4}\lroot: {5}\l\"] ;".format(ctg, i.itree.nodes[j].id, i.itree.nodes[j].beg,i.itree.nodes[j].end, i.itree.nodes[j].median, i.itree.nodes[j].root.id))
      if i.itree.nodes[j].left:
        print("{0}{1} -- {0}{2}".format(ctg, i.itree.nodes[j].id, i.itree.nodes[j].left.id))
      if i.itree.nodes[j].right:
        print("{0}{1} -- {0}{2}".format(ctg, i.itree.nodes[j].id, i.itree.nodes[j].right.id))
    print("}")
    ctg_count += 1
  print("}")

"""
Set splitter. Only rpstblastn so far.
"""
def set_splitter(blast_typ):
  if blast_typ == 'rpstblastn':
    return RpstblastnSplitter()
  if blast_typ == 'vigo':
    return VigoSplitter()

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
  ap.add_argument('--plot',
                  action='store_true',
                  help='Plot interval trees in dot to stdout')
  args = ap.parse_args()

  s = set_splitter(args.blast)
  contigs = []
  for i in sys.stdin:
    ival = s.split(i.rstrip())
    if not contigs:
      contigs.append(Contig(ival.contig, args.srr))
    if ival.contig != contigs[-1].name:
      contigs[-1].build_itree()
      contigs.append(Contig(ival.contig, args.srr))
    contigs[-1].add_interval(ival)
  contigs[-1].build_itree()
  if args.plot:
    make_dot(contigs, args.srr) #SRR918250
    return 0
  for i in contigs:
    i.score()
  return 0

if __name__ == '__main__':
  main()

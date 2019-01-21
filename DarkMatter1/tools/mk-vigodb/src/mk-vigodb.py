#!/usr/bin/env python3
#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------

import io
import os
import sys
import sqlite3
import argparse

class VigoDbMaker:

  class Source:

    def __init__(self, source, similarity, coverage, evalue):
      self.source = source
      self.similarity = float(similarity)
      self.coverage = float(coverage)
      self.evalue = float(evalue)

    def dump_list(self):
      return [self.source, self.similarity, self.coverage, self.evalue]

  class Row:

    def __init__(self, contig, proteinid, start, stop, strand, description, orflen, srr, vquot):
      self.contig = contig
      self.proteinid = proteinid
      self.start = int(start)
      self.stop = int(stop)
      self.strand = int(strand)
      self.viral_quot = 0 if vquot == 'NA' else float(vquot)
      self.orflen = int(orflen)
      self.srr = srr
      self.description = None
      self.organism = None
      self.sources = []
      self.split_description(description)
      self.hitscore = self.viral_quot

    def split_description(self, description):
      parts = description.split('[')
      if len(parts) > 1:
        self.description = parts[0]
        self.organism = parts[1][:-1]
      else:
        self.description = parts[0]

    def calc_hitscore(self):
      for i in self.sources:
        self.hitscore += ((i.similarity + i.coverage) / 200 ) - i.evalue
      self.hitscore /= (len(self.sources) + 1)
      return self.hitscore

    def add_source(self, source='NA', similarity=0.0, coverage=0.0, evalue=0.0):
      self.sources.append(VigoDbMaker.Source(source, similarity, coverage, evalue))

    def get_sources(self):
      s = []
      for i in self.sources:
        s += i.dump_list()
      return s

    def dump_sql(self):
      entry = [self.srr, self.contig, self.proteinid, self.start, self.stop, self.strand, self.description, self.organism]
      entry += self.get_sources()
      entry += [self.viral_quot, self.orflen, self.calc_hitscore()]
      return entry

  def __init__(self):
    self.path = 'viga.db'
    self.conn = sqlite3.connect(self.path)
    self.conn.row_factory = sqlite3.Row
    self.name = 'viga'
    self.commit_size = 100000
    self.data = []

  def init_db(self):
    stmt = """CREATE TABLE IF NOT EXISTS {0}
              (
                srr           TEXT,               -- srr
                contig        TEXT,               -- contig in srr
                proteinid     TEXT,               -- predicted protein on contig
                start         INT,                -- start position of proteinid [nt]
                stop          INT,                -- stop position of proteinid  [nt]
                strand        INT,                -- strand where proteinid was predicted
                descr         TEXT,               -- description text of prtein used for prediction
                orgn          TEXT,               -- organism given in descr
                source        TEXT  DEFAULT NULL,  -- source database of hit
                src_percid    FLOAT DEFAULT NULL,  -- similarity between protein template and predicted sequence
                src_perccov   FLOAT DEFAULT NULL,  -- coverage of predicted protein by source protein
                src_evalue    FLOAT DEFAULT NULL,  -- evalue for predicted protein
                pvog          TEXT  DEFAULT NULL,  -- has a pVOG hit
                pvog_percid   FLOAT DEFAULT NULL,  -- similarity between pVOG template and predicted sequence
                pvog_perccov  FLOAT DEFAULT NULL,  -- coverage of pVOG protein by source protein
                pvog_evalue   FLOAT DEFAULT NULL,  -- evalue for predicted protein based on pVOG
                viral_quot    FLOAT DEFAULT NULL,  -- viral quotient by Cody Glickman
                orflen        INT,                  -- length of predicted ORF [nt]
                hitscore      FLOAT DEFAULT NULL,  -- hackathon hit score
                PRIMARY KEY (srr, contig, proteinid)
              )"""
    c = self.conn.cursor()
    c.execute(stmt.format(self.name))

  def insert(self):
    c = self.conn.cursor()
    c.executemany("""INSERT INTO {} VALUES  (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""".format(self.name), self.data)
    self.conn.commit()
    self.data = []

  def add_remaining_entries(self):
    if self.data:
      self.insert()

  def line_to_row(self, cols):
    r = VigoDbMaker.Row(cols[0], cols[1],  cols[2],  cols[3],  cols[4], cols[9], cols[-2], cols[-1], cols[-3])
    if cols[10] != 'NO_HIT':
      r.add_source(cols[10], cols[11], cols[12], cols[13])
    else:
      r.add_source()
    if cols[15] != 'NO':
      r.add_source(cols[15], cols[16], cols[17], cols[18])
    else:
      r.add_source()
    return r

  def parse_vigo(self, infile, delimiter):
    fh = open(infile, 'r')
    entries = 0
    isFirstLine = True
    for i in fh:
      if not isFirstLine:
        row = self.line_to_row(i.strip().split(delimiter))
        self.data.append(row.dump_sql())
        entries += 1
      isFirstLine = False
    fh.close()
    if entries % self.commit_size == 0:
      self.insert()

  def make_orftable(self):
    c = self.conn.cursor()
    prev_contig = None
    prev_srr = None
    beg = 0
    end = 0
    cov = 0
    for i in c.execute("SELECT srr, contig, start, stop FROM {} GROUP BY srr, contig ORDER BY start".format(self.name)):
      print(list(i))
      if i['srr'] == prev_srr and i['contig'] == prev_contig:
        if i['start'] < beg:
          end = i['stop']
        else:
          cov += end - beg + 1
        beg = i['start']
        end = i['stop']
      prev_srr = i['srr']
      print(cov)


#select srr||'_'||contig AS srr_contigname, start||'-'||stop FROM viga GROUP BY srr, contig, proteinid ORDER BY start;

def main():
  ap =  argparse.ArgumentParser(description='Create SQLite database from tabular VIGA output')
  ap.add_argument('-b', '--build',
                  type=str,
                  help='Build database on cwd from VIGA tab output files in directory given with -b')
  ap.add_argument('-d', '--delimiter',
                  type=str,
                  default='\t',
                  help='field delimiter of VIGA result. Default: tab')

  args = ap.parse_args()
  v = VigoDbMaker()
  if args.build:
    v.init_db()
    for i in os.scandir(args.build):
      if i.name.endswith('.csv') and i.is_file():
        print("Processing {}".format(i.name), file=sys.stderr)
        v.parse_vigo(i, args.delimiter)
    v.add_remaining_entries()
    return 0
  elif sys.argv[1] == '-t':
    v.make_orftable()
    return 0
  else:
    return 0

if __name__ == '__main__':
  main()

#new
#real    0m3.612s
#user    0m0.268s
#sys     0m0.057s

# old
#real    1m38.490s
#user    0m0.664s
#sys     0m0.682s

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
import json
import argparse

class Exporter:

  def __init__(self, vigadb):
    self.db = vigadb
    self.skipmap = {'source', 'src_percid', 'src_perccov', 'src_evalue', 'pvog', 'pvog_percid', 'pvog_perccov', 'pvog_evalue'}

  def add_source(self):
    pass

  def export(self):
    c = self.db.conn.cursor()
    rows = {}
    for i in c.execute(""" SELECT * FROM viga"""):
      if i['srr'] not in rows:
        rows[i['srr']] = []
      entry = {'Sources':{}}
      for j in i.keys():
        if j not in self.skipmap:
          entry[self.db.colmap.get(j, j)] = i[j]
        if j == 'source' and i[j] != 'NA':
          entry['Sources'].update({i[j] : {self.db.colmap.get('src_percid') : i['src_percid'],
                                           self.db.colmap.get('src_perccov') : i['src_perccov'],
                                           self.db.colmap.get('src_evalue') : i['src_evalue']}})
        if j == 'pvog' and i[j] != 'NA':
          entry['Sources'].update({i[j] : {self.db.colmap.get('pvog_percid') :  i['pvog_percid'],
                                           self.db.colmap.get('pvog_perccov') : i['pvog_perccov'],
                                           self.db.colmap.get('pvog_evalue') :  i['pvog_evalue']}})

      rows[i['srr']].append({i['proteinid']: entry})
    print(json.dumps(rows))

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

    def __init__(self, cols):
      self.contig = cols[0]
      self.proteinid = cols[1]
      self.start = int(cols[2])
      self.stop = int(cols[3])
      self.strand = int(cols[4])
      self.size_aa = int(cols[5])
      self.orflen = self.size_aa * 3
      self.pI = float(cols[6])
      self.mw = float(cols[7])
      self.inst_idx = float(cols[8])
      self.description = None
      self.organism = None
      self.srr = cols[-1]
      self.split_description(cols[9])
      self.viral_quot = 0 if cols[-3] == 'NA' else float(cols[-3])
      self.hitscore = self.viral_quot
      self.sources = []

    def split_description(self, description):
      parts = description.split('[')
      if len(parts) > 1:
        self.description = parts[0].rstrip()
        self.organism = parts[1][:-1].rstrip()
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
      return [self.srr,
              self.contig,
              self.proteinid,
              self.start,
              self.stop,
              self.strand,
              self.size_aa,
              self.pI,
              self.mw,
              self.inst_idx,
              self.description,
              self.organism] + self.get_sources() + [self.viral_quot, self.orflen, self.calc_hitscore()]

  def __init__(self):
    self.path = None
    self.conn = None
    self.name = 'viga'
    self.commit_size = 100000
    self.data = []
    self.colmap = {'srr' : 'SRR', 'contig' : 'Contig', 'proteinid': 'Protein_id',
                   'start' : 'Start', 'stop' : 'Stop', 'strand' : 'Strand',
                   'descr' : 'Description', 'orgn' : 'Organism',
                   'size_aa': 'Length_aa', 'molweight':'Molecular_weight',
                   'inst_idx' : 'Instability_index', 'src_percid': 'Similarity',
                   'src_perccov' : 'Coverage', 'src_evalue' : 'Evalue',
                   'pvog_percid' : 'Similarity', 'pvog_perccov' : 'Coverage',
                   'pvog_evalue' : 'Evalue', 'viral_quot' : 'Virus_quotient',
                   'hitscore' : 'Hitscore', 'orflen' : 'Orflength'}
  def connect(self, dbpath):
    self.path = dbpath
    self.conn = sqlite3.connect(self.path)
    self.conn.row_factory = sqlite3.Row

  def init_db(self):
    stmt = """CREATE TABLE IF NOT EXISTS {0}
              (
                srr           TEXT,               -- srr
                contig        TEXT,               -- contig in srr
                proteinid     TEXT,               -- predicted protein on contig
                start         INT,                -- start position of proteinid [nt]
                stop          INT,                -- stop position of proteinid  [nt]
                strand        INT,                -- strand where proteinid was predicted
                size_aa       INT,                -- length of predicted ORF [aa]
                pI            FLOAT,              -- Estimated isolectric point
                molweight     FLOAT,              -- Molecular weight [kDa]
                inst_idx      FLOAT,              -- Estimated insatility index
                descr         TEXT,               -- description text of prtein used for prediction
                orgn          TEXT,               -- organism given in descr
                source        TEXT  DEFAULT NULL, -- source database of hit
                src_percid    FLOAT DEFAULT NULL, -- similarity between protein template and predicted sequence
                src_perccov   FLOAT DEFAULT NULL, -- coverage of predicted protein by source protein
                src_evalue    FLOAT DEFAULT NULL, -- evalue for predicted protein
                pvog          TEXT  DEFAULT NULL, -- has a pVOG hit
                pvog_percid   FLOAT DEFAULT NULL, -- similarity between pVOG template and predicted sequence
                pvog_perccov  FLOAT DEFAULT NULL, -- coverage of pVOG protein by source protein
                pvog_evalue   FLOAT DEFAULT NULL, -- evalue for predicted protein based on pVOG
                viral_quot    FLOAT DEFAULT NULL, -- viral quotient by Cody Glickman
                orflen        INT,                -- length of predicted ORF [nt]
                hitscore      FLOAT DEFAULT NULL, -- hackathon hit score
                PRIMARY KEY (srr, contig, proteinid)
              )"""
    c = self.conn.cursor()
    c.execute(stmt.format(self.name))

  def get_output_column_name(self, sqlcolname):
    return self.colmap.get(sqlcolname)

  def insert(self):
    c = self.conn.cursor()
    c.executemany("""INSERT OR IGNORE INTO  {} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""".format(self.name), self.data)
    self.conn.commit()
    self.data = []

  def add_remaining_entries(self):
    if self.data:
      self.insert()

  def line_to_row(self, cols):
    r = VigoDbMaker.Row(cols)
    if cols[10] != 'NO_HIT':
      r.add_source(cols[10], cols[11], cols[12], cols[13])
    else:
      r.add_source()
    if cols[15] != 'NO':
      r.add_source(cols[15], cols[16], cols[17], cols[18])
    else:
      r.add_source()
    return r

  def parse_viga(self, infile, delimiter):
    fh = open(infile, 'r')
    isFirstLine = True
    for i in fh:
      if not isFirstLine:
        row = self.line_to_row(i.strip().split(delimiter))
        self.data.append(row.dump_sql())
        if len(self.data) % self.commit_size == 0:
          self.insert()
      isFirstLine = False
    fh.close()

def main():
  ap =  argparse.ArgumentParser(description='Create SQLite database from tabular VIGA output')
  ap.add_argument('-db', '--database',
                  type=str,
                  default=os.path.join(os.getcwd(), 'vigares.db'),
                  help='Database path')
  ap.add_argument('-b', '--build',
                  type=str,
                  help='Build database on cwd from VIGA tab output files in directory given with -b')
  ap.add_argument('-e', '--export',
                  action='store_true',
                  help='Export database in JSON')
  ap.add_argument('-d', '--delimiter',
                  type=str,
                  default='\t',
                  help='field delimiter of VIGA result. Default: tab')

  args = ap.parse_args()
  v = VigoDbMaker()
  v.connect(args.database)
  if args.build:
    v.init_db()
    for i in os.scandir(args.build):
      if i.name.endswith('.csv') and i.is_file():
        print("Processing {}".format(i.name), file=sys.stderr)
        v.parse_viga(i, args.delimiter)
    v.add_remaining_entries()
    return 0
  if args.export:
    e = Exporter(v)
    e.export()
    return 0
  return 0

if __name__ == '__main__':
  main()

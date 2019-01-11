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

class VigoDbMaker:

  def __init__(self):
    self.path = 'viga.db'
    self.conn = sqlite3.connect(self.path)
    self.conn.row_factory = sqlite3.Row
    self.name = 'viga'

  def init_db(self):
    stmt = """CREATE TABLE IF NOT EXISTS {0}
              (
                srr     TEXT, -- sequence id
                contig  TEXT, -- function id
                proteinid TEXT,
                start INT,
                stop INT,
                strand INT,
                descr TEXT,
                source TEXT,
                src_percid FLOAT,
                src_perccov FLOAT,
                src_evalue FLOAT,
                pvog TEXT,
                pvog_percid FLOAT,
                pvog_perccov FLOAT,
                pvog_evalue FLOAT
                -- viral_quot FLOAT,
                -- orflen INT,
                --PRIMARY KEY (srr, contig, proteinid)
              )"""
    c = self.conn.cursor()
    c.execute(stmt.format(self.name))

  def parse_vigo(self, srr, infile):
    fh = open(infile, 'r')
    data = []
    isFirstLine = True
    for i in fh:
      if not isFirstLine:
        cols = i.strip().split('\t')
        line = (srr,      cols[0],  cols[1],  cols[2],  cols[3],  cols[4],
                cols[9],  cols[10], cols[11], cols[12], cols[13],
                #cols[14], cols[16], cols[17], cols[18], cols[19], cols[20])
                cols[14], cols[16], cols[17], cols[18])
        data.append(line)
      isFirstLine = False
    c = self.conn.cursor()
    #c.executemany("""INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""".format(self.name), data)
    c.executemany("""INSERT INTO {} VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""".format(self.name), data)
    self.conn.commit()

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
  v = VigoDbMaker()
  if sys.argv[1] == '-b':
    v.init_db()
    for i in os.scandir(os.getcwd()):
      if i.name.endswith('.csv') and i.is_file():
        print(i.name)
        srr = i.name.split('/')[-1].split('.')[0]
        v.parse_vigo(srr, i)
    return 0
  elif sys.argv[1] == '-t':
    v.make_orftable()
    return 0
  else:
    return 0
if __name__ == '__main__':
  main()

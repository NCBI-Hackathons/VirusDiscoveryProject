#!/usr/bin/env python3
#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2019 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------


import io
import os
import sys
import subprocess

class Orf:

  def __init__(self, name, start=0, length=0, frame=1):
    self.name = name
    self.start = int(start)
    self.frame = int(frame)
    self.end = int(start) + int(length)

class OrfmWrapper:

  def __init__(self, path='/usr/local/bin/orfm'):
    self.path = path
    self.orfs = []

  def run(self, contigfile, outdir=os.getcwd()):
    srr = contigfile.split('/')[-1].split('.')[0]
    print(srr)
    cmd = [self.path, '-t', os.path.join(outdir, srr+'.orfs.nt'), contigfile]
    print(cmd)
    ph = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    fh = open(os.path.join(outdir, srr+'.orfs.na'), 'w')
    for i in ph.stdout.readlines():
      fh.write(i)
      if i[0] == '>':
        self.orfs.append(Orf(i[1:].strip(),
                             start=i[1:].strip().split('_')[-3],
                             frame=i[1:].strip().split('_')[-2]))
      else:
        self.orfs[-1].end = self.orfs[-1].start + len(i.strip()*3)
    fh.close()

    for i in self.orfs:
      print(i.name, i.start, i.end, i.frame)

def main():
  o = OrfmWrapper()
  o.run(sys.argv[1])
  return 0

if __name__ == '__main__':
  main()

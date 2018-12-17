#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------

class Interval:

  def __init__(self, contig, hit, beg, end):
    self.contig = contig
    self.beg = int(beg)
    self.end = int(end)
    if int(beg) > int(end):
      self.beg = int(end)
      self.end = int(beg)

  def dump(self):
    return {'contig':self.contig, 'beg': self.beg, 'end': self.end}

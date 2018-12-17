#  -------------------------------------------------------------------------------
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \description
#  -------------------------------------------------------------------------------

import io
import os
import sys

class Node:

  def __init__(self, med, ivals):
    self.med = med
    self.left = []
    self.right = []

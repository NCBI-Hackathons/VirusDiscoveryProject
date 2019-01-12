##script to accept segment files (200k lines each), extract contig IDs, parse matching fa.gz file and extract contigs to put into new fasta file##

import sys 
import csv
import gzip
from Bio import SeqIO
import time 
import os


foldername = sys.argv[1] + '_results'
SRRlist = set()
os.makedirs(foldername)

#parse segmentfile csv and pull unique SRRs to read into memory later
with open(sys.argv[1]) as segmentfile:
    csv_reader = csv.reader(segmentfile, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        else:
            line_count += 1
            SRRlist.add(row[0])

SRRlist = list(SRRlist)
#print the list of unique SRR IDs
print ('list is \n ')
print (SRRlist) 
print ('\n')

#open each unique SRR's corresponding .fa.gz file with SecIO
for j in  range(len(SRRlist)):
  fastaforlist = list()
  tempfilename = '/home/vpeddu/fastas/' + SRRlist[j] + '.realign.local.fa.gz' 
  with gzip.open (tempfilename, "rt") as tempfile:
   with open(sys.argv[1]) as segmentfile:
    print (tempfilename  + ' opened')
    csv_reader = csv.reader(segmentfile, delimiter=',')
    line_count = 0
    temp = list()
#makes list of contig IDs from segment file
    for row in csv_reader:
     temp.append(row[1])
#reads fasta file in as a dictionary using SeqIO.to_dict()
#keys are fasta header, values are sequence
    record_dict = SeqIO.to_dict(SeqIO.parse(tempfile,"fasta"))
    [key.split(':')[0] for key in record_dict.keys()]
#create new dictionary with keys trimmed to everything before ":"
    trimmed_dict = {}
    for key in record_dict.keys():
     new_key = key.split(':')[0]
     trimmed_dict[new_key] = record_dict[key]
    for contig in temp:
#match contig to key ID
     if contig in trimmed_dict:
#only keep match if sequence length >999bp
      if len(trimmed_dict[contig].seq)>999:
       fastaforlist.append(trimmed_dict[contig])

#write fasta file
  tempfastafilename = foldername + '/' + SRRlist[j] + '.fasta'
  with open (tempfastafilename, "w") as output_handle: 
     SeqIO.write(fastaforlist, output_handle, "fasta")    



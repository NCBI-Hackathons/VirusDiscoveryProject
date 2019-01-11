#!/usr/bin/python
#print each CDS feature from a genbank file

from Bio import SeqIO
import re
import sys

filehandle = str(sys.argv[1])
s=filehandle.split(".")
output=open(str(filehandle[:-4])+".protein.faa", "w")

source = ""
for record in SeqIO.parse(open(filehandle, "r"), "genbank"):
	for seq_feature in record.features:
		if seq_feature.type == "CDS":
			output.write(">%s\n%s\n" % (seq_feature.qualifiers['locus_tag'][0], seq_feature.qualifiers['translation'][0]))



				
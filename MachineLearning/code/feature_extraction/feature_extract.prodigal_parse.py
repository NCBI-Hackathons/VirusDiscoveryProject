import pandas as pd
from Bio import SeqIO
from Bio import Seq
from Bio.SeqUtils import CodonUsage as CU
from Bio.Alphabet import generic_dna
import seaborn as sns
import numpy as np
import scipy as sp
import math 

CodonsDict = { 
       'TTT': 0, 'TTC': 0, 'TTA': 0, 'TTG': 0, 'CTT': 0, 
       'CTC': 0, 'CTA': 0, 'CTG': 0, 'ATT': 0, 'ATC': 0, 
       'ATA': 0, 'ATG': 0, 'GTT': 0, 'GTC': 0, 'GTA': 0, 
       'GTG': 0, 'TAT': 0, 'TAC': 0, 'TAA': 0, 'TAG': 0, 
       'CAT': 0, 'CAC': 0, 'CAA': 0, 'CAG': 0, 'AAT': 0, 
       'AAC': 0, 'AAA': 0, 'AAG': 0, 'GAT': 0, 'GAC': 0, 
       'GAA': 0, 'GAG': 0, 'TCT': 0, 'TCC': 0, 'TCA': 0, 
       'TCG': 0, 'CCT': 0, 'CCC': 0, 'CCA': 0, 'CCG': 0, 
       'ACT': 0, 'ACC': 0, 'ACA': 0, 'ACG': 0, 'GCT': 0, 
       'GCC': 0, 'GCA': 0, 'GCG': 0, 'TGT': 0, 'TGC': 0, 
       'TGA': 0, 'TGG': 0, 'CGT': 0, 'CGC': 0, 'CGA': 0, 
       'CGG': 0, 'AGT': 0, 'AGC': 0, 'AGA': 0, 'AGG': 0, 
       'GGT': 0, 'GGC': 0, 'GGA': 0, 'GGG': 0} 
    
    
   # this dictionary shows which codons encode the same AA 
   SynonymousCodons = { 
       'CYS': ['TGT', 'TGC'], 
       'ASP': ['GAT', 'GAC'], 
       'SER': ['TCT', 'TCG', 'TCA', 'TCC', 'AGC', 'AGT'], 
       'GLN': ['CAA', 'CAG'], 
       'MET': ['ATG'], 
       'ASN': ['AAC', 'AAT'], 
       'PRO': ['CCT', 'CCG', 'CCA', 'CCC'], 
       'LYS': ['AAG', 'AAA'], 
       'STOP': ['TAG', 'TGA', 'TAA'], 
       'THR': ['ACC', 'ACA', 'ACG', 'ACT'], 
       'PHE': ['TTT', 'TTC'], 
       'ALA': ['GCA', 'GCC', 'GCG', 'GCT'], 
       'GLY': ['GGT', 'GGG', 'GGA', 'GGC'], 
       'ILE': ['ATC', 'ATA', 'ATT'], 
       'LEU': ['TTA', 'TTG', 'CTC', 'CTT', 'CTG', 'CTA'], 
       'HIS': ['CAT', 'CAC'], 
       'ARG': ['CGA', 'CGC', 'CGG', 'CGT', 'AGG', 'AGA'], 
       'TRP': ['TGG'], 
       'VAL': ['GTA', 'GTC', 'GTG', 'GTT'], 
       'GLU': ['GAG', 'GAA'], 
       'TYR': ['TAT', 'TAC']}



#################################
#################################
# core functions

# Frequency Calculations
def CAI(f,idx):
	idx = CU.CodonAdaptationIndex() ### I think this is a bacterial index from "SharpEcoliIndex?"
	return idx.generate_index(f)


# from Bio.SeqUtils.CodonUsage-pysrc.html#CodonAdaptationIndex
def count_codons_aa(self, fasta_file): 
	with open(fasta_file, 'r') as handle: 
		# make the codon dictionary  
		codon_count = CodonsDict.copy() 
		# make the aa dictionary 
		aa_count = {aa:0 for aa in codon_count.keys()}

		# iterate over sequence and count all the codons in the FastaFile. 
		for cur_record in SeqIO.parse(handle, "fasta"): 
			# make sure the sequence is lower case 
			if str(cur_record.seq).islower(): 
				dna_sequence = str(cur_record.seq).upper() 
			else: 
				dna_sequence = str(cur_record.seq)

			# count codons
			for i in range(0, len(dna_sequence), 3): 
				codon = dna_sequence[i:i + 3] 
				if codon in codon_count: 
					codon_count[codon] += 1 
				else: 
					raise TypeError("illegal codon %s in gene: %s" % (codon, cur_record.id)) 
			# count aa
			aa_sequence = dna_sequence.translate()
			for i in range(0, len(aa_sequence)):
				aa = aa_sequence[i]
				aa_count[aa] += 1
	return codon_count,aa_count

##################################
##################################

# def fasta_in(f):
# 	# load CAI

# 	with open(f, "rU") as handle:
# 		for record in SeqIO.parse(handle, "fasta"):
# 			# get codon frequency 

# 			# get CAI
# 			codonF = CAI(record,idx)


# #### main
# def main(contigs):
# 	fa = SeqIO.read(f,'fasta')
# 	# iterate over contigs
# 	for cont in contigs:
# 		f = fasta_in(cont+'nucl.fa')
		

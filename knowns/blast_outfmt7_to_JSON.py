# Simple script that parses tabular blast results files into JSON format
# requires blast output to be formated as -outfmt "7 qseqid sacc staxids stitle pident evalue bitscore length" 
# also requires the name of the input file to be the SRR number followed by a period. (SRRXXXXX.anything.can.go.here.txt.output.example)
# the queries are also assumed to be in the form contig_name:1.contig_length 

# Ryan Shean 

import argparse
import sys

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Converts tabular output from #knowns into JSON format for the #scaling team')
	parser.add_argument('blast_out', help='Input tabular blast file. Generated with  -outfmt "7 qseqid sacc staxids stitle pident evalue bitscore length"')

	try: 
		args = parser.parse_args()
	except:
		parser.print_help()
		sys.exit(0)

	blast_out = args.blast_out
	SRR = blast_out.split('.')[0]

	output_file = open(SRR + '.JSON', 'w')
	output_file.write('[')

	g = open(blast_out)

	# go through data once and only split lines that actually need to go into the JSON
	for line in g:
		if line[0] != '#':
			if read_one:
				line_list = line.split('\t')
				cnl = line_list[0].split(':')
				contig = cnl[0]
				length = cnl[1].split('.')[1]
				hit_accession = line_list[1]
				hit_taxid = line_list[2]
				evalue = line_list[5]
				percent_ident = line_list[4]
				bitscore = line_list[6]

				output_file.write('\n{\n\t"SRR": "' + SRR + '",\n\t"contig":"' + contig + '",\n\t"hit_accession":"' + hit_accession + '",\n\t"hit_taxid":' + hit_taxid + ',\n\t"evalue":' + evalue + ',\n\t"length":' + length + ',\n\t"percent_ident":' + percent_ident + ',\n\t"bitscore":' + bitscore + '\n}')
			read_one = False
		else:
			read_one = True


			

	output_file.write('\n]')
	output_file.close()
	g.close()

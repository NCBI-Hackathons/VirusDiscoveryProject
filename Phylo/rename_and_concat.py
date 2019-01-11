"""
THIS WILL ONLY WORK WITH FASTA FILES THAT HAVE THE SEQUENCE ON A SINGLE LINE - it's a hackathon, what did you expect?

Contact: kylemlevi@gmail.com
USAGE:  python3 rename_and_concat.py -i path/to/my_fastas/ -o all_seqs.fasta -c

This script will read in a directory of files, ignoring any non .fasta files
and it will write all sequences from every file in the directory to a single .fasta file
It will ignore:
    * entries that have "NC_" in the name (if -c is used)
    * entries that have a duplicate header

It will rename according to:
    '>' + SRR000000 + '_' + contig1.234.123


THIS WILL ONLY WORK WITH FASTA FILES THAT HAVE THE SEQUENCE ON A SINGLE LINE - it's a hackathon, what did you expect?
"""


import sys
import os
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input File', required=True)
    parser.add_argument('-o', '--output', help='Output File', required=True)
    parser.add_argument('-c', help='Ignore any FASTA entries that have NC_, like NC_001345', action='store_true')


    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    with open(args.output, 'w') as outfile:
        seen_names = set()
        for fname in os.listdir(args.input):
            if not fname.endswith('.fasta'):
                continue
            with open(os.path.join(args.input, fname), 'r') as infile:
                save_seq = False
                for line in infile:
                    line = line.replace('\n', '')
                    if line.startswith('>'):
                        newheader = '>' + fname.split('.')[0] + '_' + line[1:]
                        if args.c and "NC_" in newheader:  # Ignoring contigs from reference guided assembly
                            continue
                        if newheader in seen_names:
                            save_seq = False
                            continue
                        else:   # this is the header of a fasta file we haven't seen
                            seen_names.add(newheader)
                            outfile.write(newheader + '\n')
                            save_seq = True
                    else:  # only sequences should make it to this statement
                        if save_seq:
                            outfile.write(line + '\n')
                            save_seq = False
                        else:
                            pass  # its a sequence and we dont need to save it
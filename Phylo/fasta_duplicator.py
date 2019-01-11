"""
USAGE:
python3 fasta_duplicator.py -i example_files/test_contigs.fasta -o example_files/dup_contigs.fasta -n 3
    -n is the number of duplications for each entry

contact:kylemlevi@gmail.com
"""

import sys
import os
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input fasta File', required=True)
    parser.add_argument('-o', '--output', help='output File', required=True)

    parser.add_argument('-n', help='number of duplicates you want', type=int)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

#     fasta_file = 'example_files/test_contigs.fasta'
#     new_fasta = 'example_files/big.fasta'
#     duplicates = 3
    new_fasta = args.output
    fasta_file = args.input
    duplicates = args.n



    with open(new_fasta, 'w') as outfile:
        for i in range(duplicates):
            with open(fasta_file, 'r') as infile:
                for line in infile:
                    if line.startswith('>'):
                        line = ">" + str(i) + line[1:]
                    outfile.write(line)
                try:
                    if not line.endswith('\n'):
                        outfile.write('\n')
                except:
                    continue
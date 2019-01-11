"""
USAGE:

python3 blast_pairs.py -i example_files/knowns.blastn -o example_files/example_blast_paris.tsv

contact: kylemlevi@gmail.com

"""

import sys
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input File', required=True)
    parser.add_argument('-o', '--output', help='Some Number')


    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)

    with open(args.output, 'w') as outfile:
        with open(args.input, 'r') as infile:
            newresult = True
            for line in infile:
                if line.startswith("#"):
                    newresult = True
                elif newresult:
                    line = line.replace('\n', '').split('\t')
                    if line[0] != line[1]:
                        outfile.write('\t'.join([line[0], line[1], line[-1], '\n']))
                        newresult = False




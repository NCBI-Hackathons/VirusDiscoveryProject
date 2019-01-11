import sys
import os
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', help='Input File', required=True)
    parser.add_argument('-n', help='Some Number', type=int)
    parser.add_argument('-a', help='Verbose', action='store_true')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)


    clusters = {}
    with open('example_files/example_clusters.tsv', 'r') as infile:
        for line in infile:
            line = line.strip().split('\t')
            clusters[line[0]] = clusters.get(line[0], 0) + 1

    for k in sorted(clusters, key=clusters.get):
        print(k, clusters[k])
    print(len(clusters))
    print(len([x for x in clusters.keys() if clusters[x] > 9]))

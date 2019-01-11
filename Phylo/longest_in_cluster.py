"""
USAGE: python3 longest_in_cluster.py -f example_files/test_contigs.fasta -c example_files/test_clusters.fasta -o example_files/newclusters.tsv

contact: kylemlevi@gmail.com
"""

import sys
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--fasta', help='Input File', required=True)
    parser.add_argument('-c', '--clusters', help='Input File', required=True)
    parser.add_argument('-o', '--output', help='Input File', required=True)


    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)


    # fasta_file = 'example_files/test_contigs.fasta'
    # cluster_file = 'example_files/new_clusters.tsv'
    # outf = 'example_files/exampleout.tsv'
    fasta_file = args.fasta
    cluster_file = args.cluster
    outf = args.output

    #count all genome lengths:
    genome_lens = {}
    with open(fasta_file, 'r') as infile:
        count = 0
        header = None
        for line in infile:
            line = line.replace('\n', '')
            if line.startswith('>'):
                if header:
                    genome_lens[header[1:]] = count
                    count = 0
                header = line
            else:
                count += len(line)
        genome_lens[header[1:]] = count

    # read all clusters
    clusters = {}
    with open(cluster_file, 'r') as infile:
        for line in infile:
            line = line.replace('\n', '').split('\t')
            clusters[line[0]] = clusters.get(line[0], []) + [line[1]]
    print(clusters)

    # define new clusters
    newclusters = {}
    for k,v in clusters.items():
        sizes = [genome_lens[x] for x in v]
        biggest = v[sizes.index(max(sizes))]
        newclusters[biggest] = v

    # write new file
    with open(outf, 'w') as outfile:
        for k,v in newclusters.items():
            for child in v:
                outfile.write(k + '\t' + child + '\n')





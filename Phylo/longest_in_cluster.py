"""
USAGE
This command will read in a fasta file (of all sequences clustered) and a cluster file (from mmseqs) and output a new cluster file with the longest sequence as the 'representative' of the cluster
    python3 longest_in_cluster.py -f example_files/test_contigs.fasta -c example_files/test_clusters.tsv -o example_files/newclusters.tsv

This command will extract only the longest sequence from each cluster, using the same files as above. It writes a new FASTA file
    python3 longest_in_cluster.py -f example_files/test_contigs.fasta -c example_files/test_clusters.tsv -o example_files/newclusters.tsv -e


contact: kylemlevi@gmail.com
"""

import sys
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--fasta', help='Input File', required=True)
    parser.add_argument('-c', '--cluster', help='Input File', required=True)
    parser.add_argument('-o', '--output', help='Input File', required=True)
    parser.add_argument('-e', '--extractlongest', help='instead of remaking the clusters around the longest, extract the longest fasta to a new file', action='store_true')


    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(1)


    # fasta_file = 'example_files/test_contigs.fasta'
    # cluster_file = 'example_files/test_clusters.tsv'
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
            try:
                clusters[line[0]] = clusters.get(line[0], []) + [line[1]]
            except:
                sys.stderr.write('something went wrong with line:\n{}\n'.format(line))


    # define new clusters
    newclusters = {}
    for k,v in clusters.items():
        sizes = [genome_lens.get(x, 0) for x in v]
        biggest = v[sizes.index(max(sizes))]
        newclusters[biggest] = v
    if not args.extractlongest:
        # write new file
        with open(outf, 'w') as outfile:
            for k,v in newclusters.items():
                for child in v:
                    outfile.write(k + '\t' + child + '\n')

    else:
        longests = set(newclusters.keys())
        with open(outf, 'w') as outfile:
            with open(fasta_file, 'r') as infile:
                keeper = False
                for line in infile:
                    if line.startswith('>'):
                        if line[1:].strip() in longests:
                            keeper = True
                            outfile.write(line)
                        else:
                            keeper = False
                    else:
                        if keeper:
                            outfile.write(line)



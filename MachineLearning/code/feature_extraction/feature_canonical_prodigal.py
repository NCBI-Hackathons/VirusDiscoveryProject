import argparse
import sys
from Bio import SeqIO 

# --------------------------------------------------
def get_args():
    """get args"""
    parser = argparse.ArgumentParser(
        description='get canonical features from prodigal output',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--imp', help='imput file',
                        metavar='imp', type=str)
    parser.add_argument('-o', '--out', help='output file',
                        metavar='out', type=str)
    return parser.parse_args()

# --------------------------------------------------


def main():
    args = get_args()
    my_in=args.imp
    my_out=args.out

    #features
    nb_genes=1
    av_gene_length=0
    sum_gene_length=0
    av_GC=0
    sum_GC=0

    f= open(my_out,"w+")
    #parsing fasta
    with open(my_in, "rU") as handle:
        contig_name=""
        header=True
        for record in SeqIO.parse(handle, "fasta"):
            contig, gene_ID=record.id.rsplit('_', 1)
            
            if int(gene_ID) == 1:
                #print summary previous contig
                if header:
                    f.write("contig_id,nb_genes,av_gene_length,av_GC\n")
                    header=False
                else:
                    f.write(contig_name+","+str(nb_genes)+","+str(av_gene_length)+","+str(av_GC)+"\n")

                #reinitialize features
                contig_name=contig
                av_gene_length=0
                sum_gene_length=0
                av_GC=0
                sum_GC=0

            #read metrics
            name, start, stop, strand, metrics=record.description.split('#')
            ID_r,partial_r,st_type_r,rbs_r,space_r,gc_r=metrics.split(';')

            nb_genes=int(gene_ID)
            name, partial=partial_r.split("=")

            if partial == "00":
                length=len(record.seq)
            else:
                length=0
            
            sum_gene_length += int(length)
            av_gene_length=sum_gene_length/int(nb_genes)

            
            name,gc=gc_r.split("=")
            sum_GC+=float(gc)
            av_GC=sum_GC/int(nb_genes)
                


    f.close()
if __name__ == '__main__':
    main()

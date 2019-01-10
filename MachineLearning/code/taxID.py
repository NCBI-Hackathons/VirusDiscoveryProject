from Bio import Entrez
import argparse
import sys

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
    taxids_filename=args.imp
    my_out=args.out
 
    f= open(my_out,"w+")

    with open(taxids_filename) as f:
        tax_ids = f.read().split('\n')

        #Entrez.email = 'user@example.org'  # Put your email here
        handle = Entrez.efetch('taxonomy', id=tax_ids, rettype='xml')
        response = Entrez.read(handle)

        for entry in response:
            sci_name = entry.get('ScientificName')
            lineage_taxa = entry.get('Lineage').split(';')
            print(sci_name, ' > '.join(lineage_taxa))
            order=lineage_taxa[2]
            print(order)
            family=lineage_taxa[3]

            #f.write("")

    f.close()
if __name__ == '__main__':
    main()


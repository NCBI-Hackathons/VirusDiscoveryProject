#!/usr/bin/python3

#Read in JSON file data to python; write to csv file

#JSON schema: [({"hit_id":<int>, "contig":<str>, "method":<str>,
#"parameters":<str>, "accession":<str>, "simil":<float>},]

import sys,json

if len(sys.argv) < 3:
    print("Usage: python3 " + sys.argv[0] + " <json input file> <csv output file>")
    sys.exit()

with open(sys.argv[1], "r") as infile:
    with open(sys.argv[2], "w") as outfile:

        data = json.load(infile)

        for key in data[0]:
            outfile.write(str(key) + ',')
        outfile.write('\n')
                
        for dict in data:
            for key in dict:
                outfile.write(str(dict[key]) + ',')
            outfile.write('\n')

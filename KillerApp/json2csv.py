#!/usr/bin/python3

#Read in JSON file data to python; write to csv file

#JSON schema: [({"hit_id":<int>, "contig":<str>, "method":<str>,
#"parameters":<str>, "accession":<str>, "simil":<float>},]

import json

with open("testfile.json", "r") as infile:
    with open("output.csv", "w") as outfile:

        data = json.load(infile)

        for key in data[0]:
            outfile.write(str(key) + ',')
        outfile.write('\n')
                
        for dict in data:
            for key in dict:
                outfile.write(str(dict[key]) + ',')
            outfile.write('\n')

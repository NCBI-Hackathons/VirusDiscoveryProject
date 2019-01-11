#!/usr/bin/env python
## Input requires three arguments
### First path of VIGA output table
### Second path of ViralQuotient.txt
### Third output file name and path
## ./app_vq [path/VIGA_Output] [path/ViralQuotient.txt] [path/Output]
#!/usr/bin/env python
import pandas as pd
import sys
import os
df = pd.read_table(sys.argv[2], index_col=0, header=None)
df2 = df.to_dict('index')

with open(sys.argv[1], "r") as csv:
    with open(sys.argv[3], "w") as outfile:
        if os.stat(sys.argv[1]).st_size == 0:
            print("Empty File") 
            exit()
        csv_lines = csv.readlines() 
        header = csv_lines[0].strip()
        header = header.strip('"')
        outfile.write(header + '\t' + 'Viral_Quotient' + '\t' + 'ORF_Length'+ '\t'+ "accession"+ '\n')
        
        
        for i in range(1, len(csv_lines)):   
            header = csv_lines[i].strip()
            header = header.strip('"')
            my_list = header.split("\t")
            VOG_id = my_list[15]
            orfl = str(int(my_list[3]) - int(my_list[2]))
            sr = str(sys.argv[1])
            srr = sr.split(".")[0]
            i +=1 
            x = df2.get(VOG_id)
            if x is not None:
                my_list.append(str(list(df2.get(VOG_id).values())[0]))
                my_list.append(orfl)
                my_list.append(srr)
            else:
                my_list.append("NA")
                my_list.append(orfl)
                my_list.append(srr)
            new_header = "\t".join(my_list)
            outfile.write(new_header + '\n')
          

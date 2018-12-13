#!/usr/bin bash

IN_FILE="/home/joan.marti.carreras/RVDB/SRR918250.realign.local.unknowns.RVDB.tblout"

IN_FOLDER="/novel/databases/RVDB/annot/"




grep -v "#" ${IN_FILE} | while read i;
	do
		MODEL=$(echo ${i} | sed 's/  */ /g'| cut -f1 -d " " | sed 's/FAM//g'| sed 's/^0*//g')
		LCA=$(cat ${IN_FOLDER}${MODEL}.txt | awk 'NR == 2 {first = $1; $1 = ""; print $0; }')
		echo ${i} | sed "s/^/${LCA}\t/g"
	done >> /home/joan.marti.carreras/RVDB/SRR918250.realign.local.unknowns.RVDB.tblout.LCA


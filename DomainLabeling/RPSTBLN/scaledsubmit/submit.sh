#/bin/bash
#script assumes we have 10 nodes (so total fasta gets split in 10).

mkdir DB
cd DB
gsutil -m cp -r dir gs://novel_blast/hd2/CDD_DB ./
cd ..
mkdir fasta
cd fasta
gsutil -m cp -r dir gs://novel_blast/hd2/SCALESET1/*fasta ./
ls | grep fasta > ../fastanames.txt
cd ..
split -l 213 fastanames.txt
cd fasta

while read line;do sed "s/line\.size\.fa/$line/g" ../cmd | sed "s/line/$line/g">> splitRPS1.sh;done < ../$1
while read line;do sed "s/line\.size\.fa/$line/g" ../cmd | sed "s/line/$line/g">> splitRPS2.sh;done < ../$2
while read line;do sed "s/line\.size\.fa/$line/g" ../cmd | sed "s/line/$line/g">> splitRPS3.sh;done < ../$3
chmod u+x+ splitRPS1.sh
chmod u+x+ splitRPS2.sh
chmod u+x+ splitRPS3.sh

#/bin/bash
DBHOME=/home/ward.deboutte/newdb
cd $DBHOME
wget ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/cdd.tar.gz
tar -xvzf cdd.tar.gz
mkdir profs
mv *smp profs
rm *pn
a=($(ls profs | wc -l))
b=$((a / 32))
ls profs > profnam.txt
split -l $b profnam.txt
mkdir SPLITDB
cd SPLITDB
ls ../ | grep x* > dbnames.txt
mv ../x* ../profs
while read line;do makeprofiledb -in ../profs/$line -dbtype rps -scale 1.0;done < dbnames.txt

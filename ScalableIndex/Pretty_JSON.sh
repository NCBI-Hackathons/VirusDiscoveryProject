echo "Pretty-JSONing the file $1"

perl -p -i -e 's/{/\n{\n/g' $1
perl -p -i -e 's/",/",\n/g' $1
perl -p -i -e 's/(},?)/\n$1/g' $1

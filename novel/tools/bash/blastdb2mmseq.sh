db_in=$1
db_gzip=$1.gz
host_dbdir=/mmseqdbs

docker run --rm -v /blast/blastdb:/blast/blastdb:ro  ncbi/blast blastdbcmd -entry all -db /blast/blastdb/$1| gzip >$db_gzip
docker run --rm -v ${PWD}:${PWD}  -v ${host_dbdir}:${host_dbdir} mmseqs2 mmseqs createdb ${PWD}/$db_gzip  $host_dbdir/$1

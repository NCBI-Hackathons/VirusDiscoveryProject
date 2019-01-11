#!/usr/bin/env perl -w
use strict;
use DBI;
use DBD::Pg;
use Getopt::Long;
use Data::Dumper qw(Dumper);
use Benchmark 'timethis';

my $bench = 1000000;
GetOptions("b=s" => \$bench) or die ("No dice with options: $!");

my $dbname = 'benchmarks_mil';
my $host = 'localhost';
my $port = 5433;
my $username = 'postgrr';
my $password = 'grrr9_@_1S';

my $dbh = DBI -> connect("dbi:Pg:dbname=$dbname;host=$host;port=$port",
			 $username,
			 $password,
			 {AutoCommit => 0, RaiseError => 1}
    ) or die $DBI::errstr;

my $stmt = qq(select * from sample_knowns where sacc = 'NC_019915' and accession in (select accession from metadata where lower(center) = LOWER('UNIVERSITY OF OXFORD') and accession in (select accession from contigs where length > 100)););
my $sth = $dbh->prepare( $stmt );
timethis($bench, sub { 
    my $rv = $sth->execute() or die $DBI::errstr;
    $sth->finish();
 });

#if($rv < 0) {
#    print $DBI::errstr;
#}
#while(my @rows = $sth->fetchrow_array()) {
#    foreach my $row (@rows){
#	print "$row \n";
#    }
#}

$dbh->disconnect();
print "Yay all done\n";

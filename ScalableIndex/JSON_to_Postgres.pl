#!/usr/bin/env perl -w
use strict;
use DBI;
use DBD::Pg;
use Getopt::Long;
use Data::Dumper qw(Dumper);
use Benchmark 'timethis';

my $output = "test.out";
my $input = "knowns.json";
my $tablename = "sample_knowns";

GetOptions("i=s" => \$input, "t=s" => \$tablename) or die ("No dice with options: $!");

print "opening $input\n";

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

open (my $fh, '<', $input) or die "Error, cannot open file $input: $!";
#open (my $out, '>', $output) or print "Could not open file $output: $!";

my $keys = "";
my $vals = "";
my $count = 0;
while (<$fh>){
    my $line = $_; #chomp();
    if ($line =~ m/^\s*{\s*$/){
	#print "found opening $line\n";
	$keys = "";
	$vals = "";
    }
    elsif( $line =~ m/^\s*"([^"]+)"\s*:\s*"([^"]+)",?\s*$/){
	my $key = $1;
	my $val = $2;
	if ($val =~ m/'/){
	    print "found a quote mark\n";
	    $val =~ s/'/''/g;
	    print "$val\n";
	}
	#print "found $1 : $2 \n";
	$keys .= "$key, ";
	$vals .= "'$val', ";
    }
    elsif ($line =~ m/^\s*}[,\]]?\s*$/){
	#print "found closing $line\n";
	$count++;
	$keys =~ s/, $//;
	$vals =~ s/, $//;
	my $sql = "INSERT INTO $tablename ($keys) values ($vals);";
	#print "command: $sql\n";
	my $result = $dbh->do($sql) or die $DBI::errstr;
	#print "result: $result\n";
    }
}
print "Count is $count\n";
$dbh->commit();
$dbh->disconnect();
print "Yay all done\n";

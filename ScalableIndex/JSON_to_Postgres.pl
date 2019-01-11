#!/usr/bin/env perl -w
use strict;
use DBI;
use DBD::Pg;
use Getopt::Long;
use Data::Dumper qw(Dumper);

my $output = "test.out";
my $input = "knowns.json";
GetOptions("i=s" => \$input) or die ("No dice with options: $!");

print "opening $input\n";

my $dbname = 'benchmarks';
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

my %hash;
my $keys = "";
my $vals = "";

while (<$fh>){
    my $line = $_; #chomp();
    if ($line =~ m/^\s*{\s*$/){
	print "found opening $line\n";
	undef %hash;
	$keys = "";
	$vals = "";

    }
    elsif( $line =~ m/^\s*"([^"]+)"\s*:\s*"([^"]+)",?\s*$/){
	print "found $1 : $2 \n";
	$hash{$1} = $2;
	$keys .= "$1, ";
	$vals .= "'$2', ";
    }
    elsif ($line =~ m/^\s*},\s*$/){
	print "found closing $line\n";
	#print Dumper %hash;
	$keys =~ s/, $//;
	$vals =~ s/, $//;
	my $sql = "INSERT INTO sample_knowns ($keys) values ($vals);";
	print "command: $sql\n";
	#my $sth = $dbh->prepare( $sql );
	#my $result = $sth->execute() or die $DBI::errstr;
	my $result = $dbh->do($sql) or die $DBI::errstr;
	print "result: $result\n";

	last;
    }
}


my $stmt = qq(SELECT * from sample_knowns;);
my $sth = $dbh->prepare( $stmt );
my $rv = $sth->execute() or die $DBI::errstr;
if($rv < 0) {
    print $DBI::errstr;
}
while(my @rows = $sth->fetchrow_array()) {
    foreach my $row (@rows){
	print "$row \n";
    }
}

$dbh->commit();
$dbh->disconnect();
print "Yay all done\n";

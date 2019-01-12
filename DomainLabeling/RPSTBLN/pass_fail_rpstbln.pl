#!/usr/bin/env perl
# Sam Shepard - 2018.01

use Data::Dumper qw(Dumper);
use File::Basename;

if ( scalar(@ARGV) != 5 ) {
	die("Usage:\n\tperl <ref1> ... <ref4> <jsons|grep>\n");
}


%taxonByAccession = ();
foreach $file (@ARGV[0..3]) {
	open(IN,'<',$file) or die("Cannot open file $file\n");
	$filename = basename($file);
	$filename =~ s/_models\.txt//;
	$taxon = $filename;
	print STDERR "Loading $file with $taxon\n";
	while($line=<IN>) {
		chomp($line);
		$taxonByAccession{$line} = $taxon;
	}
	close(IN);
}


%counts = ();
@T = ("virus","eukaryota","bacteria",'archaea','unknown');
open(IN,'<',$ARGV[4]) or die("Cannot open $ARGV[4]: $!\n");
while($line=<IN>) {
	chomp($line);
	if ( $line =~ /query_title".+?"(.+?)"/ ) {
		$currentQuery = $1;
		if ( !defined($counts{$currentQuery}{'unknown'}) ) { $counts{$currentQuery}{'unknown'} = 0; }
		if ( !defined($counts{$currentQuery}{'eukaryota'}) ) { $counts{$currentQuery}{'eukaryota'} = 0; }
		if ( !defined($counts{$currentQuery}{'archaea'}) ) { $counts{$currentQuery}{'archaea'} = 0; }
		if ( !defined($counts{$currentQuery}{'virus'}) ) { $counts{$currentQuery}{'virus'} = 0; }
		if ( !defined($counts{$currentQuery}{'bacteria'}) ) { $counts{$currentQuery}{'bacteria'} = 0; }
		#archaea_models.txt  bacteria_models.txt  eukaryota_models.txt  virus_models.txt
	} elsif ( $line =~ /accession".+?"(.+?)"/ ) {
		$accession = $1;
		$taxon = defined($taxonByAccession{$accession}) ? $taxonByAccession{$accession} : 'unknown';
		$counts{$currentQuery}{$taxon}++;
	}
}
close(IN);

foreach $query ( sort(keys(%counts)) ) {
	$pass = 'PASS';
	if ( $counts{$query}{'eukaryota'} > 3 ) { $pass = 'FAIL'; }
	if ( $counts{$query}{'bacteria'} > 3 && $counts{$query}{'virus'} == 0 ) { $pass = 'FAIL'; }
	
	$sum = 0; $type = ''; $line = '';
	foreach $t ( @T ) {
		if ( $counts{$query}{$t} > 0 ) {
			$sum += $counts{$query}{$t};
			$type .= $type eq '' ? $t : ','.$t;
		}

		if ( $line eq '' ) {
			$line = "$t:".$counts{$query}{$t};
		} else {
			$line .= " $t:".$counts{$query}{$t};
		}
	}

	if ( $sum == 0 ) {
		$type = 'dark';
	}
	print $pass,"\t",$query,"\t",$sum,"\t",$type,"\t",$line,"\n";
}

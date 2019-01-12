#!/usr/bin/env perl
# filterByLength - Sam Shepard - 2018.01

use strict;
use warnings;

my ($maxLength,$minLength,$message,$verbose);
use Getopt::Long;
GetOptions( 
		'max-length|X=i' => \$maxLength,
		'min-length|M=i' => \$minLength,
		'verbose|V' => \$verbose
	);

if ( -t STDIN && ! scalar(@ARGV) ) {
	$message = "Usage:\n\tperl $0 <fasta> [options]\n";
	$message .= "\t\t-X|--max-length\t\tFilter by maximum length. Default: no max\n";
	$message .= "\t\t-M|--min-length\t\tFilter by minimum length. Default: no min\n";
	$message .= "\t\t-V|--verbose\t\tPrint to STDERR filtered headers and reason filtered.\n";
	die($message."\n");
}


# Trim function.
# # Removes whitespace from the start and end of the string
sub trim($) {
 	my $string = defined($_[0]) ? $_[0] : '';
	$string =~ /^\s*(.*?)\s*$/;
 	return $1;
}

$/ = '>';
$verbose = defined($verbose) ? 1 : 0;
my $doMax = defined($maxLength) ? 1 : 0;
my $doMin = defined($minLength) ? 1 : 0;
my @lines = ();
my ($length,$record,$header,$sequence);
while( $record = <> ) {
	chomp($record);
	@lines = split(/\r\n|\n|\r/, $record);
	$header = trim(shift(@lines));
	$sequence = uc(join('',@lines));
	$sequence =~ tr/ //d;
	$length = length($sequence);

	if ( $length == 0 ) {
		next;
	}

	if ( $doMin && $length < $minLength ) {
		if ( $verbose ) { print STDERR "MIN\t$minLength\t$length\t$header\n"; }
		next;
	}

	if ( $doMax && $length > $maxLength ) {
		if ( $verbose ) { print STDERR "MAX\t$maxLength\t$length\t$header\n"; }
		next;
	}

	print STDOUT '>',$header,"\n",$sequence,"\n";
}

exit(0);

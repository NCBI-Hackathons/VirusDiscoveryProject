#!/usr/bin/perl -w

use strict 'subs';

if (scalar(@ARGV)!=3)
{
	die "Usage: $0 fastafile contigfile outputfile\n";
}

$fastafile=shift @ARGV;
$contigfile=shift @ARGV;
$outputfile=shift @ARGV;

open (OUT, ">$outputfile") or die "Error - cannot open file for writing '$outputfile' : $!\n";

open (FILE, "<$contigfile") or die "Error - cannot open file '$contigfile' : $!\n";
while (<FILE>)
{
	next unless /^>/;
	chomp;
	s/^>//;
	s/ .*//;
	push @contigs, $_;
}
close FILE;

open (FILE, "<$fastafile") or die "Error - cannot open file '$fastafile' : $!\n";
while (<FILE>)
{
	if (/^>LOC_(\d+)/)
	{
		my $index=$1;
		if (!defined($contigs[$index-1])) { die "Error - invalid match between contigs and fastafile files on line:\n\t$_\n"; }
		s/LOC_$index/$contigs[$index-1]/g;
		print OUT $_;
	}
	else
	{
		print OUT $_;
	}
}
close FILE;
close OUT;


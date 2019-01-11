#!/usr/bin/perl -w

use strict 'subs';

if (scalar(@ARGV)!=3)
{
	die "Usage: $0 annotationfile contigfile outputfile\n";
}

$annotationfile=shift @ARGV;
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

open (FILE, "<$annotationfile") or die "Error - cannot open file '$annotationfile' : $!\n";
$header=<FILE>;
print OUT $header;
while (<FILE>)
{
	if (!/LOC_(\d+)/)
	{
		die "Error - improper file format of $annotationfile on line:\n\t$_\n";
	}
	my $index=$1;
	#my $newindex=$origindex;
	if (!defined($contigs[$index-1])) { die "Error - invalid match between contigs and annotation files on line:\n\t$_\n"; }
	s/LOC_$index/$contigs[$index-1]/g;
	print OUT $_;
}
close FILE;
close OUT;


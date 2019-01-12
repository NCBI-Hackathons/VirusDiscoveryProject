#!/usr/bin/perl -w

use strict 'subs';

if (scalar(@ARGV)!=6)
{
	die "Usage: $0 contigfile_notmapped contigfile_mapped annotationfile outputannotationfile proteinseqsfile_mapped outputproteinseqsfile
Input files: #1, #2, #3 & #5.
Output files: #4 & #6
This program reads the first two input files and creates a mapping b/t the re-named contigs (of format LOC_xyz) and the original names (CONTIG_blah). Then it reads the annotation and proteinseqs files and for each, replaces the re-named ids with their original names.
";
}

$in_contigfile1=shift @ARGV;
$in_contigfile2=shift @ARGV;
$in_annotationfile=shift @ARGV;
$out_annotationfile=shift @ARGV;
$in_protseqsfile=shift @ARGV;
$out_protseqsfile=shift @ARGV;

# Read first input file - save original contig names
open (FILE, "<$in_contigfile1") or die "Error - cannot open file '$in_contigfile1' : $!\n";
while (<FILE>)
{
	next unless /^>/;
	chomp;
	s/^>//;
	s/ .*//;
	push @contigs1, $_;
}
close FILE;

# Read second input file - save mapped contig names (LOC_xyz)
open (FILE, "<$in_contigfile2") or die "Error - cannot open file '$in_contigfile2' : $!\n";
while (<FILE>)
{
	next unless /^>/;
	chomp;
	s/^>//;
	s/ .*//;
	push @contigs2, $_;
}
close FILE;

# Create mapping b/t renamed contig names to original names
if (scalar(@contigs1)!=scalar(@contigs2)) { die "Error - contigs files have unequal number of items! $in_contigfile1 vs. $in_contigfile2\n"; }
for (my $i=0; $i<scalar(@contigs2); $i++)
{
	$contigmapping{$contigs2[$i]}=$contigs1[$i];
}

# Read third input file - as it is read, modify each line to replace new contig names with original names
open (FILE, "<$in_annotationfile") or die "Error - cannot open file '$in_annotationfile' : $!\n";
open (OUT, ">$out_annotationfile") or die "Error - cannot open file for writing '$out_annotationfile' : $!\n";
$header=<FILE>;
print OUT $header;
while (<FILE>)
{
	if (!/(LOC_\d+)/)
	{
		die "Error - improper file format of $in_annotationfile on line:\n\t$_\n";
	}

	my $name=$1;
	if (!defined($contigmapping{$name})) { die "Error - invalid match between contigs and annotation files on line:\n\t$_\n"; }
	#replace first column, then second column - safer than a global match that could do more than desired
	s/$name/$contigmapping{$name}/;
	s/$name/$contigmapping{$name}/;
	print OUT $_;
}
close FILE;
close OUT;

# Read first input file - save original contig names
open (FILE, "<$in_protseqsfile") or die "Error - cannot open file '$in_protseqsfile' : $!\n";
open (OUT, ">$out_protseqsfile") or die "Error - cannot open file for writing '$out_protseqsfile' : $!\n";
while (<FILE>)
{
	chomp;
	if (/^>(LOC_\d+)/)
	{
		my $name=$1;
		if (!defined($contigmapping{$name})) { die "Error - invalid match between contigs and protseqs files on line:\n\t$_\n"; }
		s/$name/$contigmapping{$name}/;
	}
	print OUT "$_\n";
}
close FILE;
close OUT;

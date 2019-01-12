#/usr/bin/env perl
# blast overlaps - Sam Shepard - 2018.01
# Writen to detect overlaps in subject matches per query.
# May be useful in chimera detection.

use strict;
use warnings;

my ($nonoverlap_threshold,$overlap_threshold,$allow_self,$allow_multiple,$no_redundant,$message);
use Data::Dumper qw(Dumper);
use Getopt::Long;
GetOptions( 	'nonoverlap-threshold|N=f' => \$nonoverlap_threshold,
		'overlap-threshold|O=f' => \$overlap_threshold,
		'allow-self|S' => \$allow_self,
		'allow-multiples|M' => \$allow_multiple,
		'no-redundant|R' => \$no_redundant
	);
use constant {QID => 0, SID => 1, PID => 3, LEN => 3, MM => 4, GO => 5, QS => 6, QE => 7, SS => 8, SE => 9, EVALUE => 10, BITSCORE => 11};

if ( -t STDIN && ! scalar(@ARGV) ) {
	$message = "Usage:\n\tperl $0 <blastFMT6> [options]\n";
	$message .= "\t\t-N|--nonoverlap-threshold <#>\t\tFloat in [0,1]. Nonoverlap is less than threshold. Default = 1\n";
	$message .= "\t\t-O|--overlap-threshold <#>\t\tFloat in [0,1]. Min overlap for merging like pairs. Default = 1\n";
	$message .= "\t\t-S|--allow-self\t\t\t\tAllow query to match subject.\n";
	$message .= "\t\t-M|--allow-multiples\t\t\tAllow multiple hits per subject.\n";
	$message .= "\t\t-R|--no-redundant\t\t\tReduce output for multiple to make roughly sequential..\n";
	die($message."\n");
}

$no_redundant = defined($no_redundant) ? 1 : 0;
$allow_multiple = defined($allow_multiple) ? 1 : 0;
my $not_self = defined($allow_self) ? 0 : 1;
if ( !defined($nonoverlap_threshold) ) { $nonoverlap_threshold = 1; }
if ( !defined($overlap_threshold) ) { $overlap_threshold = 1; }

print STDERR "NONOVERLAP THRESHOLD\t(i < thresh)\t$nonoverlap_threshold\n";
print STDERR "OVERLAP THRESHOLD\t(i >= thresh)\t$overlap_threshold\n";
print STDERR "Q_id\tS1_id\tS2_id\tOverlap_coeff\tS1_start\tS1_end\tBitscore1\tS2_start\tS2_end\tBitscore2\n";

sub inferior_overlapping($$$) {
	my $h = $_[0];
	my ($s1,$s2) = ($_[1],$_[2]);

    	my $L1 = abs($h->{$s1}->[1] - $h->{$s1}->[0])+1;
    	my $L2 = abs($h->{$s2}->[1] - $h->{$s2}->[0])+1;
	my $b1 = $h->{$s1}->[2];
	my $b2 = $h->{$s2}->[2];

	if ( $b1 == $b2 ) {
		if ( $L1 < $L2 ) {
			return $s1;
		} else {
			return $s2;
		}
	} elsif ( $b1 < $b2 ) {
		return $s1;
	} else {
		return $s2;
	}
}

sub overlap_coefficient($$$$) {
	my ($a,$b,$x,$y) = (@_);
	my ($t,$intersection,$Lmin);
	# simplify by swapping
	if ( $a > $b ) { $t = $a; $a = $b; $b = $t; }
	if ( $x > $y ) { $t = $x; $x = $y; $y = $t; }

	# set the lengths and find the min
    	my $L1 = $b - $a+1;
	my $L2 = $y - $x+1;
	if ( $L1 < $L2 ) {
		$Lmin = $L1;
	} else {
		$Lmin = $L2;
	}

	#  No intersection
	if ( $b < $x || $y < $a ) {
		$intersection = 0;
	# Some intersection
	} else {
		my $E = $y >= $b ? $b : $y;
		my $S = $x <= $a ? $a : $x;
		$intersection = $E - $S + 1;
	}

	return ($intersection / $Lmin);
}

sub calculate_query_group($$) {
	my $coords = $_[0];
	my $currentQ = $_[1];
	my @subjects = keys(%{$coords});
	my $isect = '';
	my %intersections = ();
	my %subjects_to_remove = ();
	if ( scalar(@subjects) > 1 ) {
		foreach my $i ( 0 .. $#subjects ) {
			foreach my $j ( ($i+1) .. $#subjects ) {
				my ($s1,$s2) = ($subjects[$i],$subjects[$j]);

				$isect = overlap_coefficient(	$coords->{$s1}->[0],$coords->{$s1}->[1],
								$coords->{$s2}->[0],$coords->{$s2}->[1] );
				$intersections{$s1}{$s2} = $isect; $intersections{$s2}{$s1} = $isect;		
				if ( $isect >= $overlap_threshold ) {
					$subjects_to_remove{inferior_overlapping($coords,$s1,$s2)} = 1;
				}
			}
		}

		@subjects = sort(grep { ! defined($subjects_to_remove{$_}) } @subjects);
		my %redundant = ();
		if ( scalar(@subjects) > 1 ) {
			foreach my $i ( 0 .. $#subjects ) {
				foreach my $j ( ($i+1) .. $#subjects ) {
					my ($s1,$s2) = ($subjects[$i],$subjects[$j]);
					my ($ps1,$ps2) = ($s1,$s2);
					if ( $allow_multiple ) {
						$ps1 =~ s/\/.+?$//;
						$ps2 =~ s/\/.+?$//;
						if ( $ps1 eq $ps2 ) {
							if ( $no_redundant && defined($redundant{$s1}) ) {
								next;
							} else {
								$redundant{$s1} = 1;
							}
						}
					}
					if ( $intersections{$s1}{$s2} < $nonoverlap_threshold ) {
						if ( $not_self && ($ps1 eq $currentQ || $ps2 eq $currentQ ) ) { next; } 
						print STDOUT $currentQ,"\t",$ps1,"\t",$ps2,"\t",
							sprintf("%1.4f",$intersections{$s1}{$s2}),
							"\t",join("\t",@{$coords->{$s1}}),"\t",join("\t",@{$coords->{$s2}}),"\n";
					}
				}
			}
		}
	}
}

# assumes ordered query
my ($previousQ,$currentQ) = ('','');
my %coords = ();
my $sid = '';
while(my $line=<>) {
	chomp($line);
	my @f = split("\t",$line);
	$currentQ = $f[QID];
	if ( $previousQ ne $currentQ ) {
		# DO overlap tests
		if ( $previousQ ne '' ) { 
			calculate_query_group(\%coords,$previousQ);
		}
		$previousQ = $currentQ;
		%coords = ();
	}
	$sid = $allow_multiple ? $f[SID].'/'.$f[QS].'-'.$f[QE] : $f[SID];
	$coords{$sid} = [ ($f[QS], $f[QE], $f[BITSCORE]) ];

}
calculate_query_group(\%coords,$currentQ);

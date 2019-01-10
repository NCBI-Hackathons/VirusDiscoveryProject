#/usr/bin/env perl
# blast overlaps - Sam Shepard - 2018.01
# Writen to detect overlaps in subject matches per query.
# May be useful in chimera detection.

use strict;
use warnings;

my ($nonoverlap_threshold,$overlap_threshold,$allow_self);
use Getopt::Long;
GetOptions( 	'nonoverlap-threshold|N=f' => \$nonoverlap_threshold,
		'overlap-threshold|O=f' => \$overlap_threshold,
		'allow-self|S' => \$allow_self
	);
use constant {QID => 0, SID => 1, PID => 3, LEN => 3, MM => 4, GO => 5, QS => 6, QE => 7, SS => 8, SE => 9, EVALUE => 10, BITSCORE => 11};

my $not_self = defined($allow_self) ? 0 : 1;
if ( !defined($nonoverlap_threshold) ) { $nonoverlap_threshold = 1; }
if ( !defined($overlap_threshold) ) { $overlap_threshold = 0; }

print STDERR "NONOVERLAP THRESHOLD: $nonoverlap_threshold\n";
print STDERR "OVERLAP THRESHOLD: $overlap_threshold\n";
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

# assumes ordered query
my ($previousQ,$currentQ) = ('','');
my %coords = ();
my %intersections = ();
my $isect = 0;
my %subjects_to_remove = ();
while(my $line=<>) {
	chomp($line);
	my @f = split("\t",$line);
	$currentQ = $f[QID];

	if ( $previousQ ne $currentQ ) {
		# DO overlap tests
		my @subjects = keys(%coords);
		my %intersections = ();
		if ( scalar(@subjects) > 1 ) {
			foreach my $i ( 0 .. $#subjects ) {
				foreach my $j ( ($i+1) .. $#subjects ) {
					my ($s1,$s2) = ($subjects[$i],$subjects[$j]);

					$isect = overlap_coefficient(	$coords{$s1}->[0],$coords{$s1}->[1],
									$coords{$s2}->[0],$coords{$s2}->[1] );

					$intersections{$s1}{$s2} = $isect; $intersections{$s2}{$s1} = $isect;		
					if ( $isect <= $nonoverlap_threshold ) {
						if ( $isect <= $overlap_threshold ) {
							$subjects_to_remove{inferior_overlapping(\%coords,$s1,$s2)} = 1;
						}
					}
				}
			}

			@subjects = sort(grep { ! defined($subjects_to_remove{$_}) } @subjects);
			if ( scalar(@subjects) > 1 ) {
				foreach my $i ( 0 .. $#subjects ) {
					foreach my $j ( ($i+1) .. $#subjects ) {
						my ($s1,$s2) = ($subjects[$i],$subjects[$j]);
						if ( $intersections{$s1}{$s2} <= $nonoverlap_threshold ) {
							if ( $not_self && ($s1 eq $currentQ || $s2 eq $currentQ) ) { next; } 
							print STDOUT $currentQ,"\t",$s1,"\t",$s2,"\t",
								sprintf("%1.4f",$intersections{$s1}{$s2}),
								"\t",join("\t",@{$coords{$s1}}),"\t",join("\t",@{$coords{$s2}}),"\n";
						}
					}
				}
			}
		}
		$previousQ = $currentQ;
		%coords = ();
	}

	$coords{$f[SID]} = [ ($f[QS], $f[QE], $f[BITSCORE]) ];
}

if ( scalar(keys(%coords)) > 1 ) {
	my @subjects = keys(%coords);
	foreach my $i ( 0 .. $#subjects ) {
		foreach my $j ( ($i+1) .. $#subjects ) {
			my ($s1,$s2) = ($subjects[$i],$subjects[$j]);
			$isect = overlap_coefficient(	$coords{$s1}->[0],$coords{$s1}->[1],
							$coords{$s2}->[0],$coords{$s2}->[1] );
			
			$intersections{$s1}{$s2} = $isect; $intersections{$s2}{$s1} = $isect;		
			if ( $isect <= $nonoverlap_threshold ) {
				if ( $isect <= $overlap_threshold ) {
					$subjects_to_remove{inferior_overlapping(\%coords,$s1,$s2)} = 1;
				}
			}
		}
	}

	@subjects = sort( grep { ! defined($subjects_to_remove{$_}) } @subjects );
	if ( scalar(@subjects) > 1 ) {
		foreach my $i ( 0 .. $#subjects ) {
			foreach my $j ( ($i+1) .. $#subjects ) {
				my ($s1,$s2) = ($subjects[$i],$subjects[$j]);
				if ( $intersections{$s1}{$s2} <= $nonoverlap_threshold ) {
					if ( $not_self && ($s1 eq $currentQ || $s2 eq $currentQ) ) { next; }
					print STDOUT $currentQ,"\t",$s1,"\t",$s2,"\t",
						sprintf("%1.4f",$intersections{$s1}{$s2}),
						"\t",join("\t",@{$coords{$s1}}),"\t",join("\t",@{$coords{$s2}}),"\n";
				}
			}
		}
	}
}

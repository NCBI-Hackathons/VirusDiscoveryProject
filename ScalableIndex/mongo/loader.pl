#!/usr/bin/env perl

use strict;
use autodie;
use feature 'say';
use Data::Dump 'dump';
use Getopt::Long;
use JSON 'decode_json';
use MongoDB;
use Perl6::Slurp 'slurp';
use Pod::Usage;
use Readonly;

$MongoDB::BSON::looks_like_number = 1;

main();

# --------------------------------------------------
sub main {
    my %args = get_args();

    if ($args{'help'} || $args{'man_page'}) {
        pod2usage({
            -exitval => 0,
            -verbose => $args{'man_page'} ? 2 : 1
        });
    }; 

    my $collection = $args{'collection'} or pod2usage('Missing --collection');
    my $file       = $args{'file'}       or pod2usage('Missing --file'); 
    my $db         = $args{'db'}         || 'hackathon';
    my $limit      = $args{'limit'}      || 0;
    my %valid_coll = (
        contig       => \&insert_contig,
        metadata     => \&insert_metadata,
        known_sample => \&insert_known_sample,
    );

    my $insert = $valid_coll{$collection} or pod2usage(
        sprintf("Invalid collection (%s) choose from: %s\n", 
        $collection, join ', ', keys %valid_coll)
    );

    printf "Loading '%s' into '%s/%s'\n", $file, $db, $collection;

    my $json = decode_json(slurp($file));
    unless (ref $json eq 'ARRAY') {
        die "Not a JSON array";
    }

    printf "Found %s records\n", scalar(@$json);

    my $mongo = MongoDB::MongoClient->new(
        host     => 'localhost',
        port     => 27017,
        user     => 'loader',
        password => 'ilikecake',
    );

    my $mdb  = $mongo->get_database('hackathon');
    my $coll = $mdb->get_collection($collection);
    $coll->drop();

    my $i = 0;
    for my $rec (@$json) {
        printf "%-78s\r", sprintf("%3d", ++$i);
        #$coll->insert_one($rec);

        $insert->($coll, $rec); 

        last if $limit > 0 && $i >= $limit;
    }

    say "\nDone.";
}

# --------------------------------------------------
sub insert_contig {
    my ($coll, $rec) = @_;

    for my $fld (qw{covered_length perc50 length}) {
        $rec->{$fld} += 0;
    }

    $coll->insert_one($rec);
}

# --------------------------------------------------
sub insert_metadata {
    my ($coll, $rec) = @_;

    my @num_flds = qw[insert_size run_bases run_spots run_bytes];

    for my $fld (@num_flds) {
        $rec->{$fld} += 0;
    }

    $coll->insert_one($rec);
}

# --------------------------------------------------
sub insert_known_sample {
    my ($coll, $rec) = @_;

    my @num_flds = qw[pident evalue bitscore hit_len];

    for my $fld (@num_flds) {
        $rec->{$fld} += 0;
    }

    $coll->insert_one($rec);
}

# --------------------------------------------------
sub get_args {
    my %args;
    GetOptions(
        \%args,
        'db|d=s',
        'collection|c=s',
        'file|f=s',
        'limit|l=i',
        'help',
        'man',
    ) or pod2usage(2);

    return %args;
}

__END__

# --------------------------------------------------

=pod

=head1 NAME

loader.pl - a script

=head1 SYNOPSIS

  loader.pl 

Options:

  --help   Show brief help and exit
  --man    Show full documentation

=head1 DESCRIPTION

Describe what the script does, what input it expects, what output it
creates, etc.

=head1 SEE ALSO

perl.

=head1 AUTHOR

kyclark E<lt>kyclark@email.arizona.eduE<gt>.

=head1 COPYRIGHT

Copyright (c) 2019 kyclark

This module is free software; you can redistribute it and/or
modify it under the terms of the GPL (either version 1, or at
your option, any later version) or the Artistic License 2.0.
Refer to LICENSE for the full license text and to DISCLAIMER for
additional warranty disclaimers.

=cut

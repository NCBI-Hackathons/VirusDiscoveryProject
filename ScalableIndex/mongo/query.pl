#!/usr/bin/env perl

use strict;
use autodie;
use feature 'say';
use Benchmark 'timethis';
use Data::Dump 'dump';
use Getopt::Long;
use MongoDB;
use Pod::Usage;
use Readonly;

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

    my $mongo = MongoDB::MongoClient->new(
        host     => 'localhost',
        port     => 27017,
        user     => 'loader',
        password => 'ilikecake',
    );

    my $mdb   = $mongo->get_database('hackathon');
    my $query = $mdb->get_collection('query');

    my %cmp_op = (
        '='    => '$eq',
        '>'    => '$gt',
        '>='   => '$gte',
        '<'    => '$lt',
        '<='   => '$lte',
    );

    my %params;
    for my $fld (qw[length meta__center sample__sacc]) {
        my $val = $args{ $fld };
        next unless defined $val && $val ne '';

        if ($val =~ /^(\=|>|>=|<|<=)?(\d+)$/) {
            my $cmp = $1 || '=';
            my $num = $2;
            my $op  = $cmp_op{ $cmp };
            $params{ $fld } = { $op => $num };
        }
        else {
            $params{ $fld } = $val;
        }
    }

    say dump(\%params);

    if (my $bench = $args{'bench'}) {
        say "Benchmarking $bench iterations...";
        timethis($bench, sub { $query->find(\%params) });
    }
    else {
        my @data = $query->find(\%params)->all;

        printf "Found %s contigs\n", scalar(@data);
        say join "\n", map { " " . $_->{'contig'} } @data;

        if ($args{'dump'}) {
            say dump(\@data);
        }
    }
}

# --------------------------------------------------
sub get_args {
    my %args;
    GetOptions(
        \%args,
        'bench|b=i',
        'length|l=s',
        'meta__center|c=s',
        'sample__sacc|a=s',
        'dump|d',
        'help',
        'man',
    ) or pod2usage(2);

    return %args;
}

__END__

# --------------------------------------------------

=pod

=head1 NAME

query.pl - query mongodb

=head1 SYNOPSIS

  query.pl -l '>=100' -c 'UNIVERSITY OF OXFORD' -s 'NC_005856'

Options:

  --length|-l         contig.length (e.g., 100, <100, >=100)
  --meta__center|-c   contig.meta__center
  --sample__sacc|-s   contig.sample__sacc
  --dump|-d           Show data dump

  --help              Show brief help and exit
  --man               Show full documentation

=head1 DESCRIPTION

Query Mongo.

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

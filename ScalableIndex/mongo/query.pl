#!/usr/bin/env perl

use strict;
use autodie;
use feature 'say';
use Benchmark 'timethis';
use Data::Dump 'dump';
use JSON 'to_json';
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

    my $db = $args{'db'} || 'hackathon';

    say "Connecting to database '$db'";

    my $mongo = MongoDB::MongoClient->new(
        host     => 'localhost',
        port     => 27017,
        user     => 'loader',
        password => 'ilikecake',
    );

    my $mdb   = $mongo->get_database($db);
    my $query = $mdb->get_collection('query');

    my %cmp_op = (
        '='    => '$eq',
        '>'    => '$gt',
        '>='   => '$gte',
        '<'    => '$lt',
        '<='   => '$lte',
    );

    my %params;

    my %flds = @{ $args{'f'} };
    while (my ($key, $val) = each %flds) {
        next unless defined $val && $val ne '';

        if ($val =~ /^(\=|>|>=|<|<=)(\d+)$/) {
            my $cmp = $1 || '=';
            my $num = $2;
            my $op  = $cmp_op{ $cmp };
            $params{ $key } = { $op => $num };
        }
        else {
            $params{ $key } = "$val";
        }
    }

    say dump(\%params);

    if (my $bench = $args{'bench'}) {
        say "Benchmarking $bench iterations...";
        timethis($bench, sub { $query->find(\%params) });
    }
    else {
        my @data = map { delete $_->{'_id'}; $_ } 
                   $query->find(\%params)->all;

        printf STDERR "Found %s contigs\n", scalar(@data);

        if ($args{'json'}) {
            say to_json(\@data, { pretty => 1 });
        }
    }
}

# --------------------------------------------------
sub get_args {
    my %args;
    GetOptions(
        \%args,
        'db|d=s',
        'bench|b=i',
        'f=s@{0,}',
        'json|j',
        'help',
        'man',
    ) or pod2usage(2);

    #'length|l=s',
    #'meta__center|c=s',
    #'sample__sacc|a=s',

    return %args;
}

__END__

# --------------------------------------------------

=pod

=head1 NAME

query.pl - query mongodb

=head1 SYNOPSIS

  ./query.pl -f contig__length '>=100' \
    -f meta__center 'UNIVERSITY OF OXFORD' \
    -f sample__sacc 'NC_005856' 

Options:

  -f          field_name/value to search
  --db|-d     Database name
  --json|-j   Show JSON

  --help      Show brief help and exit
  --man       Show full documentation

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

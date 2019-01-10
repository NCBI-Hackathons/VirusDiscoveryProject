#!/usr/bin/env perl

use strict;
use autodie;
use feature 'say';
use Data::Dump 'dump';
use Getopt::Long;
use JSON 'decode_json';
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

    my $db    = $args{'db'} || 'hackathon';
    my $mongo = MongoDB::MongoClient->new(
        host     => 'localhost',
        port     => 27017,
        user     => 'loader',
        password => 'ilikecake',
    );

    say "Connecting to database '$db'";
    my $mdb         = $mongo->get_database($db);
    my $contig_coll = $mdb->get_collection('contig');
    my $meta_coll   = $mdb->get_collection('metadata');
    my $sample_coll = $mdb->get_collection('known_sample');
    my $query_coll  = $mdb->get_collection('query');

    $query_coll->drop();

    my $i = 0;
    for my $contig ($contig_coll->find()->all()) {
        my $meta   = $meta_coll->find_one({contig => $contig->{'contig'}})
                     or next;
        my $sample = $sample_coll->find_one({contig => $contig->{'contig'}})
                     or next;

        while (my ($key, $val) = each %$meta) {
            $contig->{'meta__' . $key} = $val;
        }

        while (my ($key, $val) = each %$sample) {
            $contig->{'sample__' . $key} = $val;
        }

        #say "contig = ", dump($contig);
        #say "meta = ", dump($meta);
        #say "sample = ", dump($sample);

        printf "%3d: %s\n", ++$i, $contig->{'contig'};
        $query_coll->insert_one($contig);
    }

    say "Done.";
}

# --------------------------------------------------
sub get_args {
    my %args;
    GetOptions(
        \%args,
        'db|d=s',
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

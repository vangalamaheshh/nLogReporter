#!/usr/bin/env perl

use strict;
use warnings;

my @array = ();
while( my $line = <STDIN> ) {
    chomp $line;
   # if( $line =~ /\sERROR\s/ ) {
        print $line, "\n";
    #}
}



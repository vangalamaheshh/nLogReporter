#!/usr/bin/perl

use strict;
use warnings;
use Getopt::Long;

my $options = parse_options();
my $info = {};
my @all_sys = ();

foreach my $cur_file( @{ $$options{ 'file' } } ) {
    open( FH, "<$cur_file" ) or die "Error in opening the file, $cur_file, $!\n";
    my $system = undef;
    while( my $line = <FH>) {
        chomp $line;
        my( $time_diff, $code ) = split( "\t", $line );
        $system = $cur_file;
        $system =~ s/.txt//g;
        $$info{ $code }{ $system }++;
    }
    push @all_sys, $system;
    close FH or die "Error closing the file, $cur_file, $!\n";
}

my @temp_codes = ( "'00102", "'00056", "'01471", "'01474", "'01460", "'01461", "'03222", 
               "'01462", "'02015", "'01510" );

my @sys = @all_sys;
print join(",",("", @sys)),"\n";
foreach my $code( @temp_codes ) {
    my @token = ();
    foreach my $cur_sys( @sys) {
        push @token, $$info{$code}{$cur_sys} || 0;
    }
    print join(",",($code,@token)),"\n";
}


sub parse_options {
    my $options = {};
    GetOptions( $options, 'file|f=s@', 'help|h' );
    unless( $$options{ 'file' } ) {
        print STDERR "Usage: $0 <--file|-f> [--file|-f]\n";
        exit 1;
    }
    return $options;
}

#!/usr/bin/env python

import sys
from datetime import datetime,timedelta

token = False
prev_time = 0
prev_saved_time = 0

#error_codes = ["'02000", "'02005", "'02010", "'02020", "'02025", "'02030",
#    "'02055", "'02095", "'02098", "'02099", "'02101", "'03004", "'03005",
#    "'03084", "'03218", "'03220", "'04056"]

error_codes = ["'01454", "'01478", "'01285", "'01294", "'01419", "'01471", "'01425", "'01427", "'01428", "'01474",
                "'01476", "'02055", "'02076", "'03188", "'01285", "'01294", "'01419", "'01425", "'01427", "'01428", "'01454",
                "'02000", "'02005", "'02010", "'02015", "'02020", "'02025", "'02030", "'02055", "'02076", "'02086", "'02095",
                "'02098", "'02099", "'02101", "'03004", "'03084", "'03088", "'03218", "'03220", "'03222", "'04056", "'04068"]
#with open(sys.argv[1],"r") as fh:
for line in sys.stdin:
    line = line.strip()
    if not line:
        next
    l = line.split("\t")
    time_diff = 0
    if not token:
        #token = True
        prev_time = datetime.strptime(l[1], '%Y-%m-%d %H:%M:%S.%f')
        prev_saved_time = datetime.strptime(l[1], '%Y-%m-%d %H:%M:%S.%f')
        if l[0] not in error_codes:
            token = True
            print( "\t".join([str(time_diff)] + l))
    else:
        cur_time = datetime.strptime(l[1], '%Y-%m-%d %H:%M:%S.%f')
        time_diff = int((cur_time - prev_time).total_seconds()/60)
        prev_time = cur_time
    if time_diff > 2 and l[0] not in error_codes:
        cur_time = datetime.strptime(l[1], '%Y-%m-%d %H:%M:%S.%f')
        actual_time_diff = int((cur_time - prev_saved_time).total_seconds()/60)
        print( "\t".join([str(actual_time_diff)] + l))
        prev_saved_time = datetime.strptime(l[1], '%Y-%m-%d %H:%M:%S.%f')

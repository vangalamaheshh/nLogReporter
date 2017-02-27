#!/usr/bin/env python3

import sys
import re
import itertools
from datetime import datetime,timedelta
from collections import OrderedDict

reObj = re.compile(r"""to #make sure it's to emergency; not emergency to
                    \s+emergency""", re.X | re.I)

time_info = OrderedDict()
input_list = []

for line in sys.stdin:
    line = line.strip()
    if not line:
        next
    l = line.split("\t")
    if reObj.search(line):
        time_stamp = datetime.strptime(l[2], '%Y-%m-%d %H:%M:%S.%f')
        time_info[time_stamp] = 1
    else:
        input_list.append(line)

time_filter = datetime.strptime("2000-03-07 13:08:28.240", '%Y-%m-%d %H:%M:%S.%f')
total = len(time_info.keys())
counter = 1
(time_goal,val) = time_info.popitem(last=False)
for line in input_list[1:]:
    l = line.split("\t")
    if l[1][0:5] == 'ERROR':
        time_stamp = datetime.strptime(l[2], '%Y-%m-%d %H:%M:%S.%f')
        if counter < total and time_stamp > time_filter and (time_goal - time_stamp).total_seconds() <= 60:
            sys.stdout.write(line + "\n")
            time_filter = time_goal
            (time_goal,val) = time_info.popitem(last=False)
            counter += 1
        else:    
            sys.stderr.write(line + "\n")
        
             
        
        

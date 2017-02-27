#!/usr/bin/env python3

import sys
import re
from datetime import datetime,timedelta
from collections import OrderedDict

rlu_info = OrderedDict()
reObj = re.compile(r"""_(?P<month>\d\d)_(?P<date>\d\d)_(?P<year>\d\d\d\d)_(?P<hour>\d\d)_(?P<min>\d\d)_(?P<sec>\d\d)\.txt""")
reObj1 = re.compile(r"""_(?P<month>\d\d)_(?P<date>\d\d)_(?P<year>\d\d\d\d)_(?P<hour>\d\d)_(?P<min>\d\d)_(?P<sec>\d\d)_(?P<fsec>\d+)\.txt""")
 
for rlu_log in sys.stdin:
    rlu_log = rlu_log.strip()
    matchObj = reObj.search(rlu_log)
    matchObj1 = reObj1.search(rlu_log)
    time_stamp = None
    if not matchObj1 and matchObj:
        time_stamp = datetime.strptime(str(matchObj.group('year')) +
                                        str(matchObj.group('month')) + 
                                        str(matchObj.group('date')) +
                                        str(matchObj.group('hour')) +
                                        str(matchObj.group('min')) +
                                        str(matchObj.group('sec')), '%Y%m%d%H%M%S')
    elif matchObj1:
        time_stamp = datetime.strptime(str(matchObj1.group('year')) +
                                        str(matchObj1.group('month')) +
                                        str(matchObj1.group('date')) +
                                        str(matchObj1.group('hour')) +
                                        str(matchObj1.group('min')) +
                                        str(matchObj1.group('sec')) +
                                        str(matchObj1.group('fsec')), '%Y%m%d%H%M%S%f')
    if time_stamp and time_stamp in rlu_info:
        rlu_info[time_stamp] += 1
    elif time_stamp:
        rlu_info[time_stamp] = 1

time_list = list(rlu_info.keys())
time_list.sort()
index = 0
counter = 0

with open(sys.argv[1], "r") as fh:
    for line in fh:
        line = line.strip()
        l = line.split("\t")
        cur_stamp = datetime.strptime(l[2], '%Y-%m-%d %H:%M:%S.%f')
        for cur_index in range(index,len(time_list)):
            if cur_stamp > time_list[cur_index]:
                counter += rlu_info[time_list[cur_index]]
            else:
                index = cur_index
                break
        list1 = [str(counter)]
        list1.extend(l)
        print("\t".join(list1))
        counter = 0

#!/usr/bin/env python

import sys
import re

with open(sys.argv[1],"r") as fh:
    matchObj = re.search("_(Super\w+?)_",sys.argv[1])
    for line in fh:
        l = line.split("\t")
        if len(l) > 1 and l[1] == "ERROR":
            print(l[0], l[2], l[5], matchObj.group(1), sep="\t")

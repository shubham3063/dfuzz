#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 12:36:22 2015

@author: hduser
"""
import sys

# only filtering output
for line in sys.stdin:
    line = line.strip()
    line = line.split('\t')
#    print line
    if len(line) != 2:
#        print "rejecting this"
        continue
    if len(line) == 2 and len(line[0]) != 6:
#        print "rejecting this"
        continue
    prog_id,inp = line
    
    sys.stdout.write(b"{0}\t{1}\n".format(prog_id,inp))

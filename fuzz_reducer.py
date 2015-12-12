#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: hduser
"""
import sys
n_args = 3
n_id   = 6
# only filtering output
for line in sys.stdin:
    line = line.strip()
    line = line.split('\t')
#    print line
    if len(line) != n_args:
#        print "rejecting this"
        continue
    if len(line) == n_args and len(line[0]) != n_id:
#        print "rejecting this"
        continue
#    prog_id,inp_id,inp = line
    prog_id,inp = line
    
#    sys.stdout.write(b"{0}\t{1}\t{2}\n".format(prog_id,inp_id,inp))
    sys.stdout.write(b"{0}\t{2}\n".format(prog_id,inp))

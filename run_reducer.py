#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 15:36:40 2015

@author: hduser
"""

import sys

prev = ''
exit_codes = []

for line in sys.stdin:

    line = line.strip()
    
    prog_id, exit_code = line.split('\t')   
    
    if prev and prog_id != prev:
        print "%s" % prev
        for ec in exit_codes:        
            print "\t%s" % (ec)
        exit_codes = []
        
    exit_code = int(exit_code)
    if exit_code not in exit_codes:
        exit_codes.append(exit_code)

    prev = prog_id

print prog_id
for ec in exit_codes:
    print "\t%s" % ec

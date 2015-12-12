#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author: hduser
"""
import sys
import random
import subprocess

fuzzer     = ' zzuf '
seed_flag  = ' -s '
ratio_flag = r" -r 0.2 -P '\\n ' "
cat_util   = ' cat '
seed_file  = '/tmp/seedinp.txt'
mut_file   = '/tmp/mutinp.txt'
list_mut_inp = []

# input is file id and input
for line in sys.stdin:
    
    # strip the record of leading and trailing whitespaces and newlines
    # and split it over tab
    line = line.strip()
    prog_id,inp = line.split('\t')

    # print original/seed input
#    print "%s\t%s" % (prog_id,inp)
    list_mut_inp.append(inp)
    # write input to temp file. so that fuzzer can capture it with 'cat' utility
    with open(seed_file,'wb') as finp:
        finp.writelines(inp.encode('latin-1'))
    
    # generate multiple inputs for each file id using a mutation fuzzer zzuf
    # Parameters
    seed = random.randint(1,100000)
    n_inputs = 5
    i = 1
    while i <= n_inputs:
        f = open(mut_file,'wb')
        fuzz_args = fuzzer + seed_flag + str(seed) + ratio_flag + cat_util + seed_file + ' > ' + mut_file
        fuzz_status = subprocess.call(fuzz_args,shell=True)
        if fuzz_status == 0:
            with open(mut_file,'rb') as fmutinp:
                mut_inp = fmutinp.readlines()
                mut_inp_striped = '\\n'.join([line.strip() for line in mut_inp])
                list_mut_inp.append(mut_inp_striped)
#                sys.stdout.write(b"{0}\t{1}\t{2}\n".format(prog_id,i,mut_inp_striped))
                sys.stdout.write(b"{0}\t{1}\n".format(prog_id,mut_inp_striped))
        
        i += 1
        
        # update seed value
        seed += 1
    
#    # print all the testcases in the output       
#    for m_inp in list_mut_inp:
#        sys.stdout.write(b"{0}\t{1}\n".format(prog_id,m_inp))
    list_mut_inp = []
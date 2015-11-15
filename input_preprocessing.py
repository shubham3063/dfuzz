# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 12:14:57 2015

@author: hduser
"""

import os, inspect

# set current working directory of the code
cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/'

# set language specific variables
lang = 'C' 
extn = '.c'

# set path for all the downloaded codes.
inpath_codes = cwd + 'downloaded_codes/' + lang + '/'

# set the file to storing data/records
fdata = open('data_C_1.txt','wb')

# open the file containing paths of directories containing the programs
with open('C_codes_with_inputs_1.txt','rb') as fi:
    
    # read all paths in a list
    filepaths = fi.readlines()
    
    # for each path split it over forward slash (/) and create accurate
    # path for the programs
    for fp in filepaths:
        fp = fp.strip().split('/')
        filepath = inpath_codes + fp[-1] + '/' + fp[-1]
        
        # open the program in read only byte stream
        with open(filepath + extn,'rb') as fprog:
            # read all lines of code in a list
            prog = fprog.readlines()

            # strip leading and trailing whitespaces and newlines 
            # and join all the lines of code with special custom 
            # delimiter (\\N). 
            # This delimiter will be used later on in mapper to 
            # reconstruct the code correctly.
            progstriped = '\\N'.join([line.strip() for line in prog])
            
        # open the input file in read only byte stream 
        with open(filepath + '_i','rb') as finp:
            # read all lines of input in a list
            inp = finp.readlines()
            
            # strip leading and trailing whitespaces and newlines 
            # and join all the lines of input with special custom 
            # delimiter (\\n). 
            # This delimiter will be used later on in mapper to 
            # reconstruct the input correctly.            
            inpstriped = '\\n'.join([line.strip() for line in inp])
        
        # write the modified input and program as a single line record 
        # in the data file
        fdata.write(inpstriped + '\t' + progstriped + '\n')
        
# close the data file    
fdata.close()

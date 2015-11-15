# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 13:07:36 2015

@author: hduser
"""
# import system and subprocess module from standard python library
import sys,subprocess

# set the compiler 
compiler = 'gcc-5 '+'-lm '+'-pthread ' + '-g '

# set the program file and input file
progfile = '/tmp/tmpprog.c'
inpfile  = '/tmp/tmpinput.txt'

i=0 # temp counter for verification
for line in sys.stdin:
    print i # temp
    i+=1    # temp
    
    # strip the record of leading and trailing whitespaces and newlines
    line = line.strip()
    
    # split the record over tab. 
    linesplit = line.split('\t')
    
    # set the input split
    inp = linesplit[0]
    
    # set the program split as the remaining record
    prog = ''.join(linesplit[1:])
    
    # convert the double escaped newlines (\\n) to newline character (\n)
    inp = inp.replace('\\n','\n')
    
    # convert the double escaped custom newlines specifier in program (\\N)
    # to valid newlines in the program
    prog = prog.replace('\\N','\n')

    # write the reconstructed input to the input file in the /tmp directory
    with open(inpfile,'wb') as finp:
        finp.writelines(inp)
    
    # write the reconstructed program to the program file in the /tmp directory
    with open(progfile,'wb') as fprog:
        fprog.writelines(prog)
    
    # compile the program file
    # set the language specific compilation arguments
    compilation_args = compiler + progfile
    
    # set the standard output and error redirection files
    stdoutput = open('/tmp/tmpstdout.txt','wb')
    stderror  = open('/tmp/tmpstderr.txt','wb')
    
    # call the compiler gcc as a subprocess and run it in shell,
    # with output and error redirected to respective directories
    status = subprocess.call(compilation_args,stdout = stdoutput, stderr = stderror, shell=True)
    
    # close the output and error files
    stdoutput.close()
    stderror.close()
    
    # check the status of the compilation and proceed accordingly
    if status == 0:
        # run the executable on the input and catch the output
        pass
    else:
        # compilation was unsuccessful. continue with next record
        continue
    
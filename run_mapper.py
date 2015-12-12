#!/usr/bin/python

# -*- coding: utf-8 -*-
"""
@author: hduser
"""
# import system and subprocess module from standard python library
import sys,subprocess,threading,os

from pymongo import MongoClient

# set the compiler 
compiler = 'gcc-5 '+'-lm '+'-pthread ' + '-g '

# set the program file and input file
progfile = '/tmp/tmpprog.c'
inpfile  = '/tmp/tmpinput.txt'
opfile   = '/tmp/tmpoutput.txt'

# keep track of file ids, if already present then dont download
list_file_ids = []

# create temp directory for stored program list. These programs will be local
# to the datanode, and will be fetched from the mongodb only once.
tmp_progs_dir = '/tmp/progs'
if not os.path.exists(tmp_progs_dir):
    os.makedirs(tmp_progs_dir)

# set up class for shell program execution with timeout
class Command(object):
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout):
        def target():
#            print 'Thread started'
            # run the executable on the input and catch the output
            execstdoutput = open('/tmp/exectmpstdout.txt','wb')
            execstderror = open('/tmp/exectmpstderr.txt','wb')    
            
            self.process = subprocess.Popen(self.cmd,stdout=execstdoutput,stderr=execstderror, shell=True)
            self.process.communicate()

            execstdoutput.close()
            execstderror.close()            
            
#            print 'Thread finished'

        thread = threading.Thread(target=target)
        thread.start()
        
        thread.join(timeout)
        if thread.is_alive():
#            print 'Terminating process'
            self.process.terminate()
            thread.join()
#        print self.process.returncode
        return self.process.returncode


n_args = 2
n_id = 6
# begin reading standard input line by line
# each input is in the format : [file id, input]
for line in sys.stdin:
    
    # strip the record of leading and trailing whitespaces and newlines
    line = line.strip()
    
    # split the record over tab. 
    linesplit = line.split('\t')

    # malformed line 
    if len(linesplit) != n_args or len(linesplit[0]) != n_id:
        continue
        
    
    # set program id
    prog_id = linesplit[0]
#    print prog_id
#    print list_file_ids

    # set the input split
#    inp_id = linesplit[1]
    inp = linesplit[1]
    
    # convert the double escaped newlines (\\n) to newline character (\n)
    inp = inp.replace('\\n','\n')    
    
#    print inp

    # write the reconstructed input to the temp input file in the /tmp directory
    with open(inpfile,'wb') as finp:
#        finp.writelines(inp.decode('utf-8').encode('utf-8'))
        finp.writelines(inp.decode('latin-1').encode('latin-1'))
        
    # set the program split as the remaining record
    # prog = ''.join(linesplit[1:])

    # first check if the program is available in the temp location
#    if prog_id in list_file_ids:
#        print "Fetching from local"

    # if program is not available in the list, then get it from mongodb client
    if prog_id not in list_file_ids:
#        print "Fetching from Mongo"
        client = MongoClient()
        db = client.mydb
        programs = db.programs
        try:
            prog = programs.find_one({'_id':prog_id})['code']
        except:
            continue

        # convert the double escaped custom newlines specifier in program (\\N)
        # to valid newlines in the program
        prog = prog.replace('\\N','\n')
        
        # write this newly fetched program and input to the tmp directory        
        with open('/tmp/progs/' + prog_id + '.c','wb') as fprog:
            fprog.writelines(prog.encode('utf-8'))

        # write the reconstructed program to the temp program file in the /tmp directory
        with open(progfile,'wb') as fprog:
            fprog.writelines(prog.encode('utf-8'))

        # if there is no error in fetching and writing, then add this program
        # to the list_prog_ids, so that we can fetch it leter directly 
        list_file_ids.append(prog_id)
        
    
    # compile the program file
    # set the language specific compilation arguments
    compilation_args = compiler + progfile + ' -o ' + '/tmp/a.out'
    
    # set the standard output and error redirection files
    stdoutput = open('/tmp/tmpstdout.txt','wb')
    stderror  = open('/tmp/tmpstderr.txt','wb')
    
    # call the compiler gcc as a subprocess and run it in shell,
    # with output and error redirected to respective directories
    status = subprocess.call(compilation_args,stdout = stdoutput, stderr = stderror, shell=True)
#    print "status : {0}".format(status)
    # close the output and error files
    stdoutput.close()
    stderror.close()
    
    # check the status of the compilation and proceed accordingly
    if status == 0:

#        # run the executable on the input and catch the output
#        execstdoutput = open('/tmp/exectmpstdout.txt','wb')
#        execstderror = open('/tmp/exectmpstderr.txt','wb')

#        execstatus = subprocess.call('/tmp/a.out < /tmp/tmpinput.txt > /tmp/tmpoutput.txt',stdout=execstdoutput,stderr=execstderror,shell=True)
        exec_command = Command("/tmp/a.out < /tmp/tmpinput.txt > /tmp/tmpoutput.txt")
        execstatus = exec_command.run(timeout=1)
#        print "{0}\t{1}\t{2}".format(prog_id, inp_id,execstatus)
        print "{0}\t{1}".format(prog_id, execstatus)

#        execstdoutput.close()
#        execstderror.close()
        
    else:
        # compilation was unsuccessful. continue with next record
        continue
    
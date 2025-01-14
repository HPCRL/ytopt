import os, sys, subprocess, random, uuid

class Plopper:
    def __init__(self,sourcefile,outputdir):

        # Initializing global variables
        self.sourcefile = sourcefile
        self.outputdir = outputdir+"/tmp_files"

        if not os.path.exists(self.outputdir):
            os.makedirs(self.outputdir)

    #Creating a dictionary using parameter label and value
    def createDict(self, x, params):
        dictVal = {}
        for p, v in zip(params, x):
            dictVal[p] = v
        return(dictVal)
    
    # Function to find the execution time of the interim file, and return the execution time as cost to the search module
    def findRuntime(self, x, params):
        interimfile = ""
        exetime = 1
        
        # Generate intermediate file
        dictVal = self.createDict(x, params)

        #compile and find the execution time
        tmpbinary = self.outputdir + '/tmp_'+str(uuid.uuid4())+'.bin'
        kernel_idx = self.sourcefile.rfind('/')
        kernel_dir = self.sourcefile[:kernel_idx]
        gcc_cmd = 'gcc ' + kernel_dir +'/test.c '
        gcc_cmd += ' -D{0}={1}'.format('FILL_ME', dictVal['FILL_ME'])
        gcc_cmd += ' -o ' + tmpbinary
        run_cmd = kernel_dir + "/exe.pl " + tmpbinary
        print (gcc_cmd)
        print(run_cmd)
        print("#####")
        #Find the compilation status using subprocess
        compilation_status = subprocess.run(gcc_cmd, shell=True, stderr=subprocess.PIPE)

        #Find the execution time only when the compilation return code is zero, else return infinity
        if compilation_status.returncode == 0 :
            execution_status = subprocess.run(run_cmd, shell=True, stdout=subprocess.PIPE);
            exetime = float(execution_status.stdout.decode('utf-8'))
            if exetime == 0:
                exetime = 1
        else:
            print(compilation_status.stderr)
            print("compile failed")
        return exetime #return execution time as cost


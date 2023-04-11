import os, sys, subprocess, random, uuid
import fileinput
from subprocess import *

class Plopper:
    def __init__(self,sourcefile,outputdir, bookkeeping):
        self.autotuner_function_to_target = bookkeeping['autotuner_function_to_target']
        self.autotuner_lowlevel_td_spec_file = bookkeeping['autotuner_lowlevel_td_spec_file']
        self.autotuner_input = bookkeeping['autotuner_input']
        self.autotuner_payload_ir_file = bookkeeping['autotuner_payload_ir_file']

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
        sourcefile_dir = os.path.dirname(os.path.realpath(self.sourcefile))
        #compile and find the execution time
        tmpvmfb = self.outputdir + '/tmp_'+str(uuid.uuid4())+'.vmfb'
        tmpoutput = self.outputdir + '/out_'+str(uuid.uuid4())+'.txt'
        payload_ir_file = sourcefile_dir + "/" + self.autotuner_payload_ir_file
        # This always assumes the low level TD file is in build/ folder.
        lowlevel_transform_ir_file = sourcefile_dir + "/build/" + self.autotuner_lowlevel_td_spec_file

        # Go in the htd-codegen/build folder.
        os.chdir(sourcefile_dir + "/build")
        ireelogfile = self.outputdir + "/../ireelogytopt.log"
        #################BUILD        
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        build_cmd =  "cmake -DCMAKE_CXX_FLAGS=\"-DAUTO_TUNER "
        # Replace values dynamically.
        for key, value in dictVal.items() :
            build_cmd += "-D{0}={1} ".format(key, value)
        build_cmd += "\" .. &>>" + ireelogfile + " && make &>>" + ireelogfile + " && ./codegen"

        #################COMPILE            
        compile_cmd = 'iree-compile {0} --iree-hal-target-backends=cuda --iree-opt-const-expr-hoisting=false --iree-opt-const-eval=false --iree-codegen-llvmgpu-enable-transform-dialect-jit=false --iree-codegen-llvmgpu-use-transform-dialect={1} &> {2}'.format(payload_ir_file, lowlevel_transform_ir_file, tmpvmfb)
        #########RUN Command ###############
        run_cmd = self.outputdir + '/../exe.pl' + ' \"iree-run-module --function={} --device=cuda '.format(self.autotuner_function_to_target)
        # Loop through the input values in autotuner_input and add them to the run_cmd string
        for input_value in self.autotuner_input:
            input_shape = input_value['shape']
            input_value = input_value['value']
            input_str = '{}={}'.format(input_shape, input_value)
            run_cmd += ' --input=\"{}\"'.format(input_str)
        run_cmd += ' --module=\"{0}\" --output= \"'.format(tmpvmfb)

        #old_run_cmd = self.outputdir + '/../exe.pl' + ' \"iree-run-module --function=linalg_matmul --device=cuda --input=\"1024x128xf32=1\" --input=\"128x2048xf32=1\" --input=\"1024x2048xf32=0\" --module=\"{0}\" --output= \"'.format(tmpvmfb)

        #######################################################################
        # Logger

        # Execute the command in a subshell using os.system
        return_value = os.system(build_cmd)
        if return_value == 0:
            compile_return_value = os.system(compile_cmd)
            if compile_return_value == 0:
                execution_status = subprocess.run(run_cmd, shell=True, stdout=subprocess.PIPE, encoding= 'utf-8')
                if execution_status.returncode == 0:
                    exetime = float(execution_status.stdout)
                    if exetime == 0:
                        exetime = 1
                else:
                    print("Run command failed with exit status:")
                    print (execution_status.returncode)
                    with open(ireelogfile, "a") as myfile:
                        myfile.write("###########################")
                        myfile.write(compile_cmd)
                        myfile.write("-----------------")
                        myfile.write(build_cmd)
                        myfile.write("-----------------")
                        myfile.write(run_cmd) 
                        myfile.write("-----------------")
                        output = execution_status.stdout.read()
                        myfile.write(output)
                    raise Exception("Error in commands")
            else:
                print("Compile Command failed with exit status:", os.WEXITSTATUS(compile_return_value))
                with open(ireelogfile, "a") as myfile:
                    myfile.write("###########################")
                    myfile.write(compile_cmd)
                    myfile.write("-----------------")
                    myfile.write(build_cmd)
                    myfile.write("-----------------")
                    myfile.write(run_cmd)
                    myfile.write("-----------------")
                    myfile.write(os.system(compile_cmd))
                raise Exception("Error in compile commands")
        else:
            print("Build Command failed with exit status:", os.WEXITSTATUS(return_value))
            raise Exception("Error in Build commands")
        #######################################################################
        return exetime

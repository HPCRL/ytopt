import os, sys, subprocess, random, uuid
import fileinput
from subprocess import *

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
        sourcefile_dir = output_dir_path = os.path.dirname(os.path.realpath(self.sourcefile))
        #compile and find the execution time
        tmpvmfb = self.outputdir + '/tmp_'+str(uuid.uuid4())+'.vmfb'
        tmpoutput = self.outputdir + '/out_'+str(uuid.uuid4())+'.txt'
        payload_ir_file = sourcefile_dir + "/matmul.mlir"
        lowlevel_transform_ir_file = sourcefile_dir + "/build/" + "hi_spec.mlir"

        # Go in the htd-codegen/build folder.
        os.chdir(sourcefile_dir + "/build")
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        #################Dynamic        
        build_cmd =  "cmake -DCMAKE_CXX_FLAGS=\"-DAUTO_TUNER "
        # Replace values dynamically.
        for key, value in dictVal.items() :
            build_cmd += "-D{0}={1} ".format(key, value)
        build_cmd += "\" .. > /dev/null && make > /dev/null && ./codegen"
        #################            
        compile_cmd = 'iree-compile {0} --iree-hal-target-backends=cuda --iree-opt-const-expr-hoisting=false --iree-opt-const-eval=false --iree-codegen-llvmgpu-enable-transform-dialect-jit=false --iree-codegen-llvmgpu-use-transform-dialect={1} &> {2}'.format(payload_ir_file, lowlevel_transform_ir_file, tmpvmfb)
        run_cmd = self.outputdir + '/../exe.pl' + ' \"iree-run-module --function=linalg_matmul --device=cuda --input=\"1024x128xf32=1\" --input=\"128x2048xf32=1\" --input=\"1024x2048xf32=0\" --module=\"{0}\" --output= \"'.format(tmpvmfb)

        #######################################################################
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
                    raise Exception("Error in commands")
            else:
                print("Compile Command failed with exit status:", os.WEXITSTATUS(compile_return_value))
                raise Exception("Error in compile commands")
        else:
            print("Build Command failed with exit status:", os.WEXITSTATUS(return_value))
            raise Exception("Error in Build commands")
        #######################################################################
        return exetime

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
        #run_return_value = 1

        # Generate intermediate file
        dictVal = self.createDict(x, params)
        sourcefile_dir = output_dir_path = os.path.dirname(os.path.realpath(self.sourcefile))
        #compile and find the execution time
        tmpvmfb = self.outputdir + '/tmp_'+str(uuid.uuid4())+'.vmfb'
        tmpoutput = self.outputdir + '/out_'+str(uuid.uuid4())+'.txt'
        payload_ir_file = sourcefile_dir + "/matmul.mlir"
        lowlevel_transform_ir_file = sourcefile_dir + "/build/" + "hi_spec.mlir"

#        kernel_idx = self.sourcefile.rfind('/')
#        kernel_dir = self.sourcefile[:kernel_idx]
        # TODO: Change the file to work on and even command to compile
        ##compile_cmd = 'gcc ' + kernel_dir +'/reduction_codegen_spec.mlir '
        #compile_cmd += ' -D{0}={1}'.format('FILL_ME', dictVal['FILL_ME'])
        #compile_cmd += ' -o ' + tmpvmfb
        #run_cmd = kernel_dir + "/exe.pl " + tmpvmfb

        # Go in the htd-codegen/build folder.
        os.chdir(sourcefile_dir + "/build")


#
#        compile_cmd = "cd /uufs/chpc.utah.edu/common/home/u1418973/other/llvm_stuff/IREE/htd-codegen/build &&"
#        compile_cmd = "cmake -DCMAKE_CXX_FLAGS=\"-DAUTO_TUNER -DBX={0} -DBY={1} -DTY={2} -DTX={3}\" ..".format(dictVal['BX'], dictVal['BY'], dictVal['TX'], dictVal['TY'])
#        compile_cmd += " && make && ./codegen "
#        compile_cmd +=" && iree-compile " + payload_ir_file + " --iree-hal-target-backends=cuda --iree-opt-const-expr-hoisting=false --iree-opt-const-eval=false --iree-codegen-llvmgpu-enable-transform-dialect-jit=false --iree-codegen-llvmgpu-use-transform-dialect=" + lowlevel_transform_ir_file + " &> " + tmpvmfb
#        run_cmd = 'iree-run-module --function=linalg_matmul --device=cuda --input=\"1024x128xf32=1\" --input=\"128x2048xf32=1\" --input=\"1024x2048xf32=0\" --module=' + tmpvmfb        #+ tmpoutput
        #print("ENV = " + os.environ['CUDA_VISIBLE_DEVICES'])
        os.environ['CUDA_VISIBLE_DEVICES'] = '0'
        build_cmd = "cmake -DCMAKE_CXX_FLAGS=\"-DAUTO_TUNER -DBX={0} -DBY={1} -DTY={2} -DTX={3}\" .. > /dev/null && make > /dev/null && ./codegen".format(dictVal['BX'], dictVal['BY'], dictVal['TX'], dictVal['TY'])
        compile_cmd = 'iree-compile {0} --iree-hal-target-backends=cuda --iree-opt-const-expr-hoisting=false --iree-opt-const-eval=false --iree-codegen-llvmgpu-enable-transform-dialect-jit=false --iree-codegen-llvmgpu-use-transform-dialect={1} &> {2}'.format(payload_ir_file, lowlevel_transform_ir_file, tmpvmfb)
        run_cmd = self.outputdir + '/../exe.pl' + ' \"iree-run-module --function=linalg_matmul --device=cuda --input=\"1024x128xf32=1\" --input=\"128x2048xf32=1\" --input=\"1024x2048xf32=0\" --module=\"{0}\" --output= \"'.format(tmpvmfb)
        print(run_cmd)

#######################################################################

## Execute the compile command
#        build_process = subprocess.run(build_cmd, shell=True)
#        build_output, build_error = build_process.communicate()
#        if build_process.returncode != 0:
#            # build failed
#            print("Build failed with error:")
#            print(build_error.decode())
#        else:
#            # build succeeded, execute the compile command
#            print ("BUILD_SUCCESS")
#            compile_process = subprocess.run(compile_cmd, shell=True)
#            compile_output, compile_error = compile_process.communicate()
#            if compile_process.returncode != 0:
#                # Compilation failed
#                print("Compile command failed with error:")
#                print(compile_error.decode())
#            else:
#                print ("COMPILE_SUCCESS")
#                # compile success now run.
#                run_process = subprocess.Popen(run_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#                run_output, run_error = run_process.communicate()
#                if run_process.returncode != 0:
#                    # Run failed
#                    print("Run failed with error:")
#                    print(run_error.decode())
#                else:
#                    # Run succeeded, print the output
#                    print(run_output.decode())
#        return exetime
######################################################################33
# os.system

# Execute the command in a subshell using os.system
       # print (build_cmd)
       # print (compile_cmd)
       # print (run_cmd)
        return_value = os.system(build_cmd)
        if return_value == 0:
            #print("Build Command executed successfully")
            compile_return_value = os.system(compile_cmd)
            if compile_return_value == 0:
                #print("Compile Command executed successfully")
#                run_return_value = os.system(run_cmd)
#                if run_return_value == 0:
#                    #print("Run Command executed successfully")
#                    run_return_value = 1
#                else:
#                    print("Run Command failed with exit status:", os.WEXITSTATUS(run_return_value))

                execution_status = subprocess.run(run_cmd, shell=True, stdout=subprocess.PIPE, encoding= 'utf-8')
                if execution_status.returncode == 0:
                    exetime = float(execution_status.stdout)
                    if exetime == 0:
                        exetime = 1
                else:
                    print("RUN ERROR")
                    print (execution_status.returncode)
                    raise Exception("Error in commands")
            else:
                print("Compile Command failed with exit status:", os.WEXITSTATUS(compile_return_value))
        else:
            print("Build Command failed with exit status:", os.WEXITSTATUS(return_value))
#        return run_return_value 
        return exetime
######################################################################33

#        #Find the compilation status using subprocess
#        compilation_status = subprocess.run(compile_cmd, shell=True, stderr=subprocess.PIPE)
#
#        #Find the execution time only when the compilation return code is zero, else return infinity
#        if compilation_status.returncode == 0 :
#            print ("COMPILED SUCCESS")
#            print (run_cmd)
#
##            execution_status = subprocess.run(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#            execution_status = subprocess.run(run_cmd, shell=True, stdout=subprocess.PIPE)
#            exetime = float(execution_status.stdout.decode('utf-8'))
#            print("exetime= " + exetime)
#            print("exection_status = " + execution_status)
#            if exetime == 0:
#                print ("RUN SUCCESS")
#                exetime = 1
#            else:
#                print ("RUN ERROR")
#        else:
#            print(compilation_status.stderr)
#            print("compile failed")
#        return exetime #return execution time as cost
#
                                                                                                                                 

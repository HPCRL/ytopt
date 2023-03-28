import numpy as np
from autotune import TuningProblem
from autotune.space import *
import os, sys, time, json, math
import ConfigSpace as CS
import ConfigSpace.hyperparameters as CSH
from skopt.space import Real, Integer, Categorical

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.dirname(HERE)+ '/plopper')
from plopper_amir_transformdialect_test import Plopper

# create an object of ConfigSpace
cs = CS.ConfigurationSpace(seed=1234)
#block size for openmp dynamic schedule
# p0= CSH.OrdinalHyperparameter(name='BLOCK_SIZE', sequence=['1','2','3','4','5','6','7','8','9','10'], default_value='5')
p0= CSH.UniformIntegerHyperparameter(name='BX', lower=64, upper=65, default_value=64)
p1= CSH.UniformIntegerHyperparameter(name='BY', lower=32, upper=33, default_value=32)
p2= CSH.UniformIntegerHyperparameter(name='TX', lower=16, upper=17, default_value=16)
p3= CSH.UniformIntegerHyperparameter(name='TY', lower=64, upper=65, default_value=64)
cs.add_hyperparameters([p0, p1, p2, p3])

# problem space
task_space = None
input_space = cs
output_space = Space([
     Real(0.0, inf, name="time")
])

output_dir_path = os.path.dirname(os.path.realpath(__file__))
# TODO: Modify it to make it generic somehow.
input_dir_path = "/uufs/chpc.utah.edu/common/home/u1418973/other/llvm_stuff/IREE/htd-codegen/"
##kernel_idx = dir_path.rfind('/')
#kernel = dir_path[kernel_idx+1:]
#TODO:replace me with the location to transform dialect script to change.
obj = Plopper(input_dir_path+'/main.cpp',output_dir_path)

#x1=['FILL_ME']
def myobj(point: dict):
    def plopper_func(x):
        x = np.asarray_chkfinite(x)  # ValueError if any NaN or Inf
#        value = [point[x1[0]]]
        value = list(point.values())
        print('CONFIG:',point)
#        params = ["FILL_ME"]
        params = {k.upper(): v for k, v in point.items()}
        result = obj.findRuntime(value, params)
        return result

#    x = np.array([point['FILL_ME']])
    x = np.array(list(point.values()))
    results = plopper_func(x)
    print('OUTPUT: ',results)
    
    return results

Problem = TuningProblem(
    task_space=None,
    input_space=input_space,
    output_space=output_space,
    objective=myobj,
    constraints=None,
    model=None
    )

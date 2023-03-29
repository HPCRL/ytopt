import json
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

##############################Automate the inputs from json################################################
input_json_file_name = "input_config.json"
# Read the JSON input file
with open(input_json_file_name, 'r') as f:
    input_data = json.load(f)
##############################Bookkeeping part#################################
input_dir_path = input_data['bookkeeping']['autotuner_target_dir']
input_hl_td_file_name = input_data['bookkeeping']['autotuner_target_file']
output_dir_path = os.path.dirname(os.path.realpath(__file__))
obj = Plopper(input_dir_path + '/' + input_hl_td_file_name ,output_dir_path)
##############################Configuration#####################################

# Create a ConfigurationSpace object
cs = CS.ConfigurationSpace(seed=1234)

# Add hyperparameters to the ConfigurationSpace object
for param in input_data['configuration']:
    name = param['name']
    lower = int(param['lower'])
    upper = int(param['upper'])
    default_value = int(param['default_value'])
    cs.add_hyperparameter(CSH.UniformIntegerHyperparameter(name, lower, upper, default_value))
##############################################################################

# problem space
task_space = None
input_space = cs
output_space = Space([
     Real(0.0, inf, name="time")
])

############################################################################
# The input parameters setting is done by now, let's into the main code now.
############################################################################
def myobj(point: dict):
    def plopper_func(x):
        x = np.asarray_chkfinite(x)  # ValueError if any NaN or Inf
        value = list(point.values())
        print('CONFIG:',point)
        params = {k.upper(): v for k, v in point.items()}
        result = obj.findRuntime(value, params)
        return result

    x = np.array(list(point.values()))
    results = plopper_func(x)
    print('OUTPUT: ',results)
    return results

##############################Pass all inputs to tuning####################
Problem = TuningProblem(
    task_space=None,
    input_space=input_space,
    output_space=output_space,
    objective=myobj,
    constraints=None,
    model=None
    )
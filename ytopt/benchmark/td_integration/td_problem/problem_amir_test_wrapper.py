import json
import numpy as np
from autotune import TuningProblem
from autotune.space import *
import os, sys, time, json, math
import ConfigSpace as CS
import ConfigSpace.hyperparameters as CSH
from skopt.space import Real, Integer, Categorical

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(1, os.path.dirname(HERE) + "/plopper")
from plopper_amir_transformdialect_test import Plopper

##############################Automate the inputs from json################################################
input_json_file_name = "input_config.json"
# Read the JSON input file
with open(input_json_file_name, "r") as f:
    input_data = json.load(f)
##############################Bookkeeping part#################################
bookkeeping = input_data["bookkeeping"]
autotuner_target_dir = bookkeeping["autotuner_target_dir"]
autotuner_highlevel_td_spec_file = bookkeeping["autotuner_highlevel_td_spec_file"]

output_dir_path = os.path.dirname(os.path.realpath(__file__))
obj = Plopper(
    autotuner_target_dir + "/" + autotuner_highlevel_td_spec_file,
    output_dir_path,
    bookkeeping,
)
##############################Configuration#####################################

# Create a ConfigurationSpace object
cs = CS.ConfigurationSpace(seed=1234)

# Add hyperparameters to the ConfigurationSpace object
for param in input_data["configuration"]:
    name_t = param["name"]
    type_t = param["type"]

    if type_t == "integer":
        lower_t = int(param["lower"])
        upper_t = int(param["upper"])
        default_value_t = int(param["default_value"])
        cs.add_hyperparameter(
            CSH.UniformIntegerHyperparameter(name_t, lower_t, upper_t, default_value_t)
        )
    elif type_t == "float":
        lower_t = float(param["lower"])
        upper_t = float(param["upper"])

        default_value_t = float(param["default_value"])
        cs.add_hyperparameter(
            CSH.UniformFloatHyperparameter(name_t, lower_t, upper_t, default_value_t)
        )
    elif type_t == "categorical":
        if "choices" not in param:
            raise ValueError(
                "Input error: 'choices' key is missing for 'categorical' type"
            )
        listp = param["choices"]
        default_value_t = param["default_value"]
        cs.add_hyperparameter(
            CSH.CategoricalHyperparameter(
                name=name_t, choices=listp, default_value=default_value_t
            )
        )
    else:
        print("Unknown 'type' value from" + input_json_file_name + " file")
        sys.exit(1)
##############################################################################

# problem space
task_space = None
input_space = cs
output_space = Space([Real(0.0, inf, name="time")])


############################################################################
# The input parameters setting is done by now, let's into the main code now.
############################################################################
def myobj(point: dict):
    def plopper_func(x):
        x = np.asarray_chkfinite(x)  # ValueError if any NaN or Inf
        value = list(point.values())
        print("CONFIG:", point)
        txvalue = point["TX"]
        tyvalue = point["TY"]
        bxvalue = point["BX"]
        byvalue = point["BY"]

        totalthreads = txvalue * tyvalue
        params = {k.upper(): v for k, v in point.items()}
        if bxvalue * byvalue >= 16 and txvalue * tyvalue >=16 and totalthreads <= 1024 and totalthreads > 0:
            result = obj.findRuntime(value, params)
        else:
            result = float('+inf')
        return result

    x = np.array(list(point.values()))
    results = plopper_func(x)
    print("OUTPUT: ", results)
    return results


##############################Pass all inputs to tuning####################
Problem = TuningProblem(
    task_space=None,
    input_space=input_space,
    output_space=output_space,
    objective=myobj,
    constraints=None,
    model=None,
)

#!/bin/bash

python3 -W ignore -m ytopt.search.ambs --evaluator ray --problem problem_amir_test_wrapper.py --max-evals=100 --learner RF
python3 findMin.py

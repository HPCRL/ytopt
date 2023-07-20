#!/bin/csh
#SBATCH --time=12:00:00 # walltime, abbreviated by -t
#SBATCH -o matmul_timing_%j.sout # name of the stdout, using the job number (%j) and the first node (%N)
#SBATCH -e matmul_timing_%j.serr # name of the stderr, using job and first node values
#SBATCH --ntasks=8    # number of MPI tasks, abbreviated by -n
#SBATCH --account=soc-gpu-np     # account - abbreviated by -A
#SBATCH --partition=soc-gpu-np  # partition, abbreviated by -p
#SBATCH --gres=gpu:a100:1
#SBATCH --mem=16000

module load cuda python/3.10

python3 -W ignore -m ytopt.search.ambs --evaluator ray --problem problem_amir_test_wrapper.py --max-evals=1000 --learner GBRT
python3 findMin.py
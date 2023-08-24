#!/bin/csh
#SBATCH --time=12:00:00 # walltime, abbreviated by -t
#SBATCH -o matmul_timing_%j.sout # name of the stdout, using the job number (%j) and the first node (%N)
#SBATCH -e matmul_timing_%j.serr # name of the stderr, using job and first node values
#SBATCH --ntasks=16    # number of MPI tasks, abbreviated by -n
#SBATCH --account=soc-gpu-np     # account - abbreviated by -A
#SBATCH --partition=soc-gpu-np  # partition, abbreviated by -p
#SBATCH --gres=gpu:a100:1
#SBATCH --mem=32000
#SBATCH --exclude=notch369,notch370   # excluding nodes notch369 and notch370

module load cuda python/3.10

python3 -W ignore -m ytopt.search.ambs --evaluator ray --problem problem_amir_test_wrapper.py --max-evals=1000 --learner RF
python3 findMin.py

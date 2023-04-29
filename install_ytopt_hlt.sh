mkdir ytopt
cd ytopt
git clone https://github.com/ytopt-team/ConfigSpace.git
cd ConfigSpace
module load python/3.10
pip3.10 install -e .
cd ..
git clone https://github.com/ytopt-team/scikit-optimize.git
cd scikit-optimize
pip3.10 install -e .
cd ..
git clone -b version1 https://github.com/ytopt-team/autotune.git
cd autotune
pip3.10 install -e .
cd ..
module load gcc openmpi
git clone -b main https://github.com/HPCRL/ytopt
cd ytopt
pip3.10 install -e .

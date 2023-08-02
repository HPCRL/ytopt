sizesMatmul = [
    [1024, 1024, 1024],   
    [1024, 512, 1024],
    [1024, 256, 1024],
    [1024, 128, 1024],
    [512, 512, 512],
    [256, 256, 256],
    [1000, 1000, 1000],
    [510, 510, 510],
    [224, 224, 224],
    [120, 120, 120],
    [256, 1024, 256],
    [224, 1024, 224],
    [256, 1024, 256],
    [224, 512, 224],
    [120, 512, 120],
    [1024, 32, 1024],
    [1024, 1024, 32],
    [32, 1024, 1024],
]

def find_divisors(num):
    divisors = []
    for i in range(1, num + 1):
        if num % i == 0:
            divisors.append(str(i))
    return divisors
    
with open(f"./all_matmul_sbatch.sh", "w") as fout:
    fout.truncate()

for item in sizesMatmul:
    N, K, M = item
    import shutil
    import os
    src_folder = "./td_integration_mod"
    dst_folder = f"./td_integration_matmul_M{M}_K{K}_N{N}"

    # delete the destination folder if it already exists
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)

    # use shutil.copytree() to recursively copy the contents of the source folder to the destination folder
    shutil.copytree(src_folder, dst_folder)

    src_folder = "../../../htd-codegen"
    dst_folder = f"../../../htd-codegen_M{M}_K{K}_N{N}"

    # delete the destination folder if it already exists
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)

    # use shutil.copytree() to recursively copy the contents of the source folder to the destination folder
    shutil.copytree(src_folder, dst_folder)

    with open("./td_integration_mod/td_problem/input_config.json", "rt") as fin:
        with open(f"./td_integration_matmul_M{M}_K{K}_N{N}/td_problem/input_config.json", "wt") as fout:
            for line in fin:
                fout.write(line.replace('${N}', str(N)).replace("${K}", str(K)).replace("${M}", str(M)).replace("${M_DIVISORS}", ", ".join(find_divisors(M))).replace("${N_DIVISORS}", ", ".join(find_divisors(N))).replace("${K_DIVISORS}", ", ".join(find_divisors(K))))
    with open(f"./all_matmul_sbatch.sh", "a") as fout:
        fout.write(f"cd ./td_integration_matmul_M{M}_K{K}_N{N}/td_problem && sbatch run.sh && cd ../..\n")

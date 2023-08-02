sizesAnsor = [
    [1, 256, 64, 128, 3, 2, 1],
    [1, 128, 128, 256, 1, 2, 0],
    [1, 64, 256, 256, 5, 1, 2],
    [1, 32, 512, 512, 3, 1, 1]
]

def find_divisors(num):
    divisors = []
    for i in range(1, num + 1):
        if num % i == 0:
            divisors.append(str(i))
    return divisors
    
with open(f"./all_conv1d_sbatch.sh", "w") as fout:
    fout.truncate()

for item in sizesAnsor:
    N, W, CI, CO, KW, stride, pad = item
    output_width = (W + 2* pad - KW) // stride + 1


    import shutil
    import os
    src_folder = "./td_integration_mod_conv1d"
    dst_folder = f"./td_integration_conv1d_ncw_N{N}_W{W}_CO{CO}_CI{CI}_KW{KW}_ST_{stride}_padding_{pad}"

    # delete the destination folder if it already exists
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)

    # use shutil.copytree() to recursively copy the contents of the source folder to the destination folder
    shutil.copytree(src_folder, dst_folder)
    src_folder = "/scratch/general/vast/u1418973/porting-ytopt/ytopt/htd-codegen"
    dst_folder = f"/scratch/general/vast/u1418973/porting-ytopt/ytopt/htd-codegen_conv1d_ncw_N{N}_W{W}_CO{CO}_CI{CI}_KW{KW}_ST_{stride}_padding_{pad}"

    # delete the destination folder if it already exists
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)

    # use shutil.copytree() to recursively copy the contents of the source folder to the destination folder
    shutil.copytree(src_folder, dst_folder)

    with open("./td_integration_mod_conv1d/td_problem/input_config.json", "rt") as fin:
        with open(f"./td_integration_conv1d_ncw_N{N}_W{W}_CO{CO}_CI{CI}_KW{KW}_ST_{stride}_padding_{pad}/td_problem/input_config.json", "wt") as fout:
            for line in fin:
                fout.write(line.replace('${N}', str(N))
                           .replace("${W}", str(W + 2 * pad)).replace("${CO}", str(CO)).replace("${CI}", str(CI))
                           .replace("${KW}", str(KW)).replace("${ST}", str(stride))
                           .replace("${OW}", str(output_width)).replace("${OLD_W}", str(W)).replace("${PAD}", str(pad)).replace("${N_DIVISORS}", ", ".join(find_divisors(N)))
                           .replace("${F_DIVISORS}", ", ".join(find_divisors(CO)))
                           .replace("${OW_DIVISORS}", ", ".join(find_divisors(output_width))).replace("${CI_DIVISORS}", ", ".join(find_divisors(CI)))
                           .replace("${KW_DIVISORS}", ", ".join(find_divisors(KW))))
    with open(f"./all_conv1d_sbatch.sh", "a") as fout:
        fout.write(f"cd ./td_integration_conv1d_ncw_N{N}_W{W}_CO{CO}_CI{CI}_KW{KW}_ST_{stride}_padding_{pad}/td_problem && sbatch run.sh && cd ../..\n")
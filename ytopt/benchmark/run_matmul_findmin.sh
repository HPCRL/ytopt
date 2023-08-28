#!/bin/bash

# List of directories
conv_directories=(
  "td_integration_conv2d_nchw_N1_H112_W112_CO128_CI128_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H28_W28_CO512_CI512_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H136_W136_CO128_CI64_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H34_W34_CO256_CI512_KH1_KW1_ST_1_padding_0"
  "td_integration_conv2d_nchw_N1_H136_W136_CO64_CI128_KH1_KW1_ST_1_padding_0"
  "td_integration_conv2d_nchw_N1_H34_W34_CO512_CI256_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H14_W14_CO1024_CI256_KH1_KW1_ST_1_padding_0"
  "td_integration_conv2d_nchw_N1_H544_W544_CO32_CI3_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H14_W14_CO256_CI256_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H56_W56_CO128_CI256_KH1_KW1_ST_2_padding_0"
  "td_integration_conv2d_nchw_N1_H14_W14_CO512_CI1024_KH1_KW1_ST_2_padding_0"
  "td_integration_conv2d_nchw_N1_H56_W56_CO256_CI256_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H14_W14_CO512_CI512_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H56_W56_CO256_CI64_KH1_KW1_ST_1_padding_0"
  "td_integration_conv2d_nchw_N1_H17_W17_CO1024_CI512_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H56_W56_CO64_CI64_KH1_KW1_ST_1_padding_0"
  "td_integration_conv2d_nchw_N1_H17_W17_CO512_CI1024_KH1_KW1_ST_1_padding_0"
  "td_integration_conv2d_nchw_N1_H56_W56_CO64_CI64_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H224_W224_CO64_CI3_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H68_W68_CO128_CI256_KH1_KW1_ST_1_padding_0"
  "td_integration_conv2d_nchw_N1_H224_W224_CO64_CI3_KH7_KW7_ST_2_padding_3"
  "td_integration_conv2d_nchw_N1_H272_W272_CO64_CI32_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H68_W68_CO512_CI256_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H28_W28_CO128_CI128_KH3_KW3_ST_1_padding_1"
  "td_integration_conv2d_nchw_N1_H7_W7_CO2048_CI512_KH1_KW1_ST_1_padding_0"
  "td_integration_conv2d_nchw_N1_H28_W28_CO256_CI512_KH1_KW1_ST_2_padding_0"
  "td_integration_conv2d_nchw_N1_H28_W28_CO512_CI128_KH1_KW1_ST_1_padding_0"
)

matmul_directories=(
"td_integration_matmul_M512_K512_N512"
"td_integration_matmul_M510_K510_N510"
"td_integration_matmul_M32_K1024_N1024"
"td_integration_matmul_M256_K256_N256"
"td_integration_matmul_M256_K1024_N256"
"td_integration_matmul_M224_K512_N224"
"td_integration_matmul_M224_K224_N224"
"td_integration_matmul_M224_K1024_N224"
"td_integration_matmul_M120_K512_N120"
"td_integration_matmul_M120_K120_N120"
"td_integration_matmul_M1024_K512_N1024"
"td_integration_matmul_M1024_K32_N1024"
"td_integration_matmul_M1024_K256_N1024"
"td_integration_matmul_M1024_K128_N1024"
"td_integration_matmul_M1024_K1024_N32"
"td_integration_matmul_M1024_K1024_N1024"
"td_integration_matmul_M1000_K1000_N1000"

)

matvec_directories=(
"td_integration_matvec_M1000_K1000"
"td_integration_matvec_M1024_K1024"
"td_integration_matvec_M1024_K128"
"td_integration_matvec_M1024_K256"
"td_integration_matvec_M1024_K32"
"td_integration_matvec_M1024_K512"
"td_integration_matvec_M120_K120"
"td_integration_matvec_M120_K512"
"td_integration_matvec_M224_K1024"
"td_integration_matvec_M224_K224"
"td_integration_matvec_M224_K512"
"td_integration_matvec_M256_K1024"
"td_integration_matvec_M256_K256"
"td_integration_matvec_M32_K1024"
"td_integration_matvec_M510_K510"
"td_integration_matvec_M512_K512"
)

transpose_gemm_directories=(
"td_integration_transposed_gemm_M1000_K1000_N1000"
"td_integration_transposed_gemm_M1024_K1024_N1024"
"td_integration_transposed_gemm_M1024_K1024_N32"
"td_integration_transposed_gemm_M1024_K128_N1024"
"td_integration_transposed_gemm_M1024_K256_N1024"
"td_integration_transposed_gemm_M1024_K32_N1024"
"td_integration_transposed_gemm_M1024_K512_N1024"
"td_integration_transposed_gemm_M120_K120_N120"
"td_integration_transposed_gemm_M120_K512_N120"
"td_integration_transposed_gemm_M224_K1024_N224"
"td_integration_transposed_gemm_M224_K224_N224"
"td_integration_transposed_gemm_M224_K512_N224"
"td_integration_transposed_gemm_M256_K1024_N256"
"td_integration_transposed_gemm_M256_K256_N256"
"td_integration_transposed_gemm_M32_K1024_N1024"
"td_integration_transposed_gemm_M510_K510_N510"
"td_integration_transposed_gemm_M512_K512_N512"
)

conv1d_directories=(
"td_integration_conv1d_ncw_N1_W128_CO256_CI128_KW1_ST_2_padding_0"
"td_integration_conv1d_ncw_N1_W256_CO128_CI64_KW3_ST_2_padding_1"
"td_integration_conv1d_ncw_N1_W32_CO512_CI512_KW3_ST_1_padding_1"
"td_integration_conv1d_ncw_N1_W64_CO256_CI256_KW5_ST_1_padding_2"
)
# Current directory
current_dir=$(pwd)

# Iterate over the directories
for dir in "${matmul_directories[@]}"; do
  # Change to directory
  cd "$dir/td_problem"
  #echo "$dir"
  # Modify the Python file using sed
#  sed -i 's/\b12\b/11/g' findMin.py

  # print file name 
  #echo $current_dir | awk -F'/' '{sub("td_integration_", "", $(NF-1)); print $(NF-1)}'
  # Run Python file
  #python3 findMin.py
  #python3 -W ignore findMin.py | grep -E '^\s*[0-9.]+\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+$' | awk '{print $4}'
  python3 -W ignore findMin.py | grep -E '^\s*[0-9.]+\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+\s+[0-9.]+$' | awk '{print $6}'


  # Return to current directory
  cd "$current_dir"
done

#!/bin/bash

folders=(
  "N1_H112_W112_CO128_CI128_KH3_KW3_ST_1_padding_1"
  "N1_H56_W56_CO128_CI256_KH1_KW1_ST_2_padding_0"
  "N1_H14_W14_CO512_CI1024_KH1_KW1_ST_2_padding_0"
  "N1_H56_W56_CO256_CI256_KH3_KW3_ST_1_padding_1"
  "N1_H56_W56_CO256_CI64_KH1_KW1_ST_1_padding_0"
  "N1_H56_W56_CO64_CI64_KH1_KW1_ST_1_padding_0"
  "N1_H17_W17_CO512_CI1024_KH1_KW1_ST_1_padding_0"
  "N1_H56_W56_CO64_CI64_KH3_KW3_ST_1_padding_1"
  "N1_H224_W224_CO64_CI3_KH3_KW3_ST_1_padding_1"
  "N1_H68_W68_CO128_CI256_KH1_KW1_ST_1_padding_0"
  "N1_H224_W224_CO64_CI3_KH7_KW7_ST_2_padding_3"
  "N1_H28_W28_CO128_CI128_KH3_KW3_ST_1_padding_1"
  "N1_H7_W7_CO2048_CI512_KH1_KW1_ST_1_padding_0"
  "N1_H28_W28_CO256_CI512_KH1_KW1_ST_2_padding_0"
  "N1_H28_W28_CO512_CI128_KH1_KW1_ST_1_padding_0"
)
for folder in "${folders[@]}"
do
  cd "td_integration_conv2d_nchw_$folder/td_problem" || exit
#  sed -i s/1000/3000/g run.sh 
#  sbatch run.sh
#  print "done $i"

	# Store the result of `wc -l results.json` in a variable
result=$(wc -l results.json)

# Extract the count from the result using awk
count=$(echo "$result" | awk '{print $1}')

# Compare the count with the desired value
if [ "$count" -eq 3001 ]; then
  echo "$folder - done"
else
  echo "$folder - running"
fi

  # Run your desired commands within the folder
  # Example: ls (to list the contents of the folder)
  # Return to the parent directory
  cd ../..
done


import pandas
import numpy as np
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression

dataframe = pandas.read_csv("results.csv")
array = dataframe.values
# Create a boolean mask of rows where column 4 is not -1
mask = array[:, 11] != float("inf")
# Create a new array that only contains the rows that meet the condition
new_array = array[mask, :]
x = new_array[:,11]

print("Performance (accuracy) summary based on", len(new_array), "evaluations:")
print("Min: ", 1/x.max())
print("Max: ", 1/x.min())
print("Mean: ", 1/x.mean())
print("The best configurations (for the smallest 1/accuracy) of P1, P2, P3 and P4 is:\n")
print("P1		P2 	   P3 	     P4		1/accuracy	     elapsed time\n")

print("Performance (accuracy) summary based on", len(new_array), "evaluations:")
print("Min: ", 1/x.max())
print("Max: ", 1/x.min())
print("Mean: ", 1/x.mean())
print("The best configurations (for the smallest 1/accuracy) of P1, P2, P3 and P4 is:\n")
print("BF\t\tBN\t\tBOH\t\tBOW\t\tTC\t\tTF\t\tTKH\t\tTKW\t\tTN\t\tTOH\t\tTOW\t\tVECTORIZATION\t\texecution time\t\tscore\n")
mn = x.min()
for i in range(len(new_array)): 
   if x[i] == mn:
      print("\t\t".join(map(str, new_array[i,:])))
      print("\n")
      print(f"#define BN {int(new_array[i,1])}")
      print(f"#define BF {int(new_array[i,0])}")
      print(f"#define BOH {int(new_array[i,2])}")
      print(f"#define BOW {int(new_array[i,3])}")

      print(f"#define TN {int(new_array[i,8])}")
      print(f"#define TF {int(new_array[i,5])}")
      print(f"#define TOH {int(new_array[i,9])}")
      print(f"#define TOW {int(new_array[i,10])}")

      print(f"#define TC {int(new_array[i,4])}")
      print(f"#define TKH {int(new_array[i,6])}")
      print(f"#define TKW {int(new_array[i,7])}")
      print(f"#define VECTORIZATION {int(new_array[i,11])}")


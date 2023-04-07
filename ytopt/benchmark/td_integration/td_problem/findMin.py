import pandas
import numpy as np
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression

dataframe = pandas.read_csv("results.csv")
array = dataframe.values
# Create a boolean mask of rows where column 4 is not -1
mask = array[:, 4] != -1
# Create a new array that only contains the rows that meet the condition
new_array = array[mask, :]
x = new_array[:,4]

print("Performance (accuracy) summary based on", len(new_array), "evaluations:")
print("Min: ", 1/x.max())
print("Max: ", 1/x.min())
print("Mean: ", 1/x.mean())
print("The best configurations (for the smallest 1/accuracy) of P1, P2, P3 and P4 is:\n")
print("P1		P2 	   P3 	     P4		1/accuracy	     elapsed time\n")
mn = x.min()
for i in range(len(new_array)): 
   if x[i] == mn:
    print (new_array[i,:])

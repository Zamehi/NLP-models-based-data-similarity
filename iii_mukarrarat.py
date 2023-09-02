

# In this file we read from mukarrarat file

# ------------------------------- LIBRARIES --------------------------------
import pandas as pd
import math
import numpy as np
# ------------------------------- FUNCTIONS --------------------------------

# --------------------------------- MAIN -----------------------------------

# .................................reading..................................
file_path= 'csb_hadith.xlsx'
sheet_name = 'Sheet1'

df = pd.read_excel(file_path) # df is data frame
#print(df)


array_2d = df.values # converting data frame to 2D numpy array

arr_col= array_2d.shape[1] # 37
arr_row= array_2d.shape[0] # 7593
print ("col are ", arr_col, arr_row )
#array_2d= str(array_2d)
i =0; j =0

# removing nans and converting to a jagged array
i =0; j= 1

while i< arr_row:
    j = 1
    while j< arr_col:
        if  math.isnan(float(array_2d[i][j])):
           array_2d[i][j]= -1
        j+=1
    # _________ removing nans _________

    i+=1
print(array_2d)
print ("End of sim1")
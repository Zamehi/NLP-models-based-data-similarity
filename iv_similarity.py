
# In this file we find similarity + equivalence classes + store the results

# ------------------------------- LIBRARIES --------------------------------
import pandas as pd
import ii_reading
import iii_mukarrarat
import numpy as np
import math
from openpyxl import load_workbook


# .................................function..................................


def equi_class (string):
    if string >= 0.8 and string < 0.988:
        return "similar"

    elif string >= 0.9888:
        return "identical"

    else:
        return "not similar"


# finding the COSINE SIMILARITY

def create_2d_array(rows, cols):
   # Create a 2D array with 'rows' rows and 'cols' columns filled with zeros
   my_2d_array = [[0 for _ in range(cols)] for _ in range(rows)]
   return my_2d_array


# --------------------------------- MAIN -----------------------------------

# --------------------------------------------------------------------------
# --------------------------- COSINE SIMILARITY ----------------------------


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



size2 = ii_reading.size
sim_arr =create_2d_array(iii_mukarrarat.arr_row, iii_mukarrarat.arr_col)
sim_arr2 = create_2d_array(iii_mukarrarat.arr_row, iii_mukarrarat.arr_col)
print ("Printing cosine similarity...")
i =0
j =1; z= 0;
string1= ""; string2 = ""; string3 = "" ; string4 = ""; string5 = ""# strings used to store the data in file
data= [] # gonna append all the data to write to this array

row =-1;col=-1; hadis1 = -1; hadis2 = -1
# working with array_2d from iii_mukarrarat file
while i< iii_mukarrarat.arr_row:#i< 12
   while  j<iii_mukarrarat.arr_col:# i < 13
      # checking value of row and col for hadis array ... check index
      while z<len (ii_reading.hadis_number):
           if (iii_mukarrarat.array_2d[i][0] != -1) and (ii_reading.hadis_number[z]== iii_mukarrarat.array_2d[i][0]) and row ==-1:
               row = z
               hadis1 = ii_reading.hadis_number[z]
           if (iii_mukarrarat.array_2d[i][j]!= -1) and (ii_reading.hadis_number[z]== iii_mukarrarat.array_2d[i][j]) and col == -1:
                col = z
                hadis2 = ii_reading.hadis_number[z]
           if row!= -1 and col != -1:
               break
           z+=1
      z=0
      if row!=-1 and col!= -1: # both are found


          cosine_sim = cosine_similarity(ii_reading.tfidf_matrix[row], ii_reading.tfidf_matrix[col])
          cosine_sim2= cosine_similarity(ii_reading.tfidf_matrix2[row].reshape(1,-1), ii_reading.tfidf_matrix2[col].reshape(1,-1))
          #sim_arr[i][j] = cosine_sim[0][0]

          sim_arr[i][j]= round(cosine_sim[0][0], 4)
          sim_arr2[i][j]= round(cosine_sim2[0][0], 4)
          #print(sim_arr[i][j])
          # ############################## writing in file ########################
          string1 = str(hadis1) + "," + str(hadis2)
          string2 = sim_arr[i][j]                  # tdfidf similarity
          string3 = equi_class(sim_arr[i][j])      # status
          string4 = sim_arr2[i][j]                 # bert similariyt
          string5 = equi_class(sim_arr2[i][j])     # status

          #print(string1, string2)
          data_to_write = {
              'Ahadis': string1,
              'Similarity tdfidf': string2,
              'Status I': string3,
              'Similarity Bert': string4,
              'Status II':string5
          }
          data_to_write['Ahadis'] = string1
          data_to_write['Similarity tdfidf'] = string2
          data_to_write['Status I']= string3
          data_to_write['Similarity Bert'] = string4
          data_to_write['Status II'] = string5

          print(data_to_write)
         # print (data)
          data.append(data_to_write)
          #print (data)
          # ############################## writing in file ########################
      else :
          sim_arr[i][j]= -1
      j = j + 1
      row = -1;  col = -1
      #print ("j is ", j)

   j =1
   #print ("yes")
  # print(sim_arr[i])
   print("i is ->", i)

   i= i+1
   # if (i == 50):
   #     break

# ############################## writing in file ########################

# Convert the list of dictionaries to a DataFrame
print (data)
df = pd.DataFrame(data)
# Save the DataFrame to an Excel file
file_path = 'data2.xlsx'  # Replace with the desired file path
df.to_excel(file_path, index=False)

print("Data successfully written to the Excel file.")

# sim_arr contains similarities of all ahadis
print ("End of sim2")

# In this file we do vectroization + reading from file

import numpy as np
import pandas as pd
import nltk
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from pyarabic.araby import strip_tashkeel
import gensim
import math


# ---------------------
import i_column_reading

# downloading pyarabic language module
#--------------------------------------
# #####################################
def all_present (arr):

     sim=[]; flag = 0;     i =1; j=0

     while i< 7563:
         j = 0; flag =0
         while j<len (arr):
             if i==arr[j]:
                 flag = 1
                 break
             j+=1
         if flag ==0:
             sim.append(i)
         i+=1
     return sim

#--------------------------------------
# #####################################
# -------- checking for arabic text ........function
def contains_arabic(text):
    # Regular expression pattern to match Arabic characters
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDCF\uFDF0-\uFDFF\uFE70-\uFEFF]+')
    return bool(arabic_pattern.search(text))

# Reading distinct chapters and grouping ahadis based on the chapters

# #####################################
# ------------- removing nans from the hadis ----------------
def check_nans(arr, arr2):
    #          hadis_number,   hadis

    # Iterate in reverse to avoid index shifting
    i = len(arr) - 1
    while i >= 0:
        if math.isnan(arr[i]):
            del arr[i]
            del arr2[i]
        i -= 1



# --------------------------------- MAIN -----------------------------------

# .................................reading..................................
df = pd.read_excel('bukhari.xlsx')
column_name = 'Arabic_Matn'  # Replace with the name of the desired column
column_data = df[column_name]
chapter_name = 'Chapter_Arabic'
chapter_data= df[chapter_name]
hadith_number= 'Hadith_number'
hadith_no = df[hadith_number]

hadis = [] # this is a vector
hadis_number=[]
 # Print the column data
i=0 # i is rows
p=0
string = ""
for index, row in df.iterrows():
    if i_column_reading.choice== 1:
        if  chapter_data[i] == i_column_reading.distinct_strings[i_column_reading.ans-1]:
          # print("hELLO -> ",i,"->",i_column_reading.distinct_strings[i_column_reading.ans-1])
           str3 = column_data[i]
           # ------------------------------------
           # 23-45-678-9-0 seperating hadith number and
           # duplicating hadis on the next hadis
           duplicate_no = 0
           if (type(hadith_no[i])==  'str'):
               line = hadith_no[i]
               numbers_list = re.findall(r'\d+', hadith_no[i])
               numbers_list = [int(num) for num in numbers_list] # convert string to integer
               duplicate_no = len(numbers_list)
               dup = 0
               while (dup<duplicate_no):
                   hadis_number.append(numbers_list[dup])
                   hadis.append(str3)
                   dup+=1
           #---------------------------------------
           else:
               str2= hadith_no[i]
                # "" condition on hadees
               hadis.append(str3)
               hadis_number.append(str2)
               #print (hadis[p])
           #---------------------------------------
           p+=1
        #i+=1
    else:
        #print("hELLO -> ", i, "->")
        str3 = column_data[i]
        str2 = hadith_no[i]

        duplicate_no = 0
        if (type(hadith_no[i]) == str):
            line = hadith_no[i]
            numbers_list = re.findall(r'\d+', hadith_no[i])  # 408-409->
            numbers_list = [int(num) for num in numbers_list] # convert string to integer
            duplicate_no = len(numbers_list)
            dup = 0
            while (dup < duplicate_no):
                hadis_number.append(numbers_list[dup])
                hadis.append(str3)
                dup += 1
                p+=1

        # ---------------------------------------
        else:
            str2 = hadith_no[i]
            # "" condition on hadees
            hadis.append(str3)
            hadis_number.append(str2)
            #print(hadis[p])
        # ---------------------------------------
        p += 1
    i += 1

#------------- REMOVING AARAB -----------------

print ("******************************")
print ("Removing aarab...")
new_hadis = [""]

# Remove diacritic marks ("aarab") from the Arabic word
d =0
size = len(hadis)
while d<len(hadis):
    if type(hadis[d]) !='str':
        hadis[d]= str(hadis[d])

    if (contains_arabic(hadis[d])== True):
        modified_word = strip_tashkeel(hadis[d])
        new_hadis.append(modified_word)
    else:
        new_hadis.append("")
    d+=1
# new_hadis had ahadis with no aarab

# ------------arabic hadis --------------------
# --------------- checking for nan presence ------------
check_nans(hadis_number, new_hadis)

print ("The number of ahadis is ", len (new_hadis))

print ("----------------")
#print (sorted(hadis_number))

# ------------------------------------------
# ---- checking for all ahadis to be present ----
# ------------------------------------------
# ###########################################

missing_numbers =all_present(hadis_number)
hadis_number.extend(missing_numbers)

# ---- appending empty strings ------
i =0
while i< len (missing_numbers):
    new_hadis.append("")
    i+=1
#print ("The number of ahadis is ", len (new_hadis))
# ###########################################

# --------------- VECTORIZATION -------------

# ###########################################


# Initialize the TF-IDF vectorizer
vectorizer = TfidfVectorizer()
print ("******************************")
# Fit and transform the documents

tfidf_matrix = vectorizer.fit_transform(new_hadis)

# Get the feature names (terms)
feature_names = vectorizer.get_feature_names_out(new_hadis)
matrix2 = tfidf_matrix.toarray()

print ("Printing vector...")
#  Print the feature names
print("Printing features... " );
#print (feature_names)

# ###########################################

# --------------- VECTORIZATION -------------
# ---------------     BERT    ---------------

# ###########################################

tfidf_matrix2 = []
#=================== library ================
from transformers import BertTokenizer, BertModel


tokenizer = BertTokenizer.from_pretrained("aubmindlab/bert-base-arabert")
model = BertModel.from_pretrained("bert-base-multilingual-cased")
#aubmindlab/bert-base-arabert

import torch

# Sample Arabic string to vectorize

i =0
while i< len(new_hadis):
    if i == 1000 or i == 2000 or i == 3000  or i ==4000 or i == 5000 or i == 6000 or i == 7000:
        print(i)
    # Tokenize the sequence
    tokens = tokenizer.tokenize(new_hadis[i])
    # Define the maximum sequence length for BERT (512 tokens)
    max_seq_length = 510
    # Truncate the sequence to fit within the maximum length
    if len(tokens) > max_seq_length:
        tokens = tokens[:max_seq_length]

    # Convert the truncated tokens back to text
    truncated_text = tokenizer.convert_tokens_to_string(tokens)

    inputs = tokenizer(truncated_text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    #bert_embedding = outputs.pooler_output
    bert_embedding = outputs.last_hidden_state[0][0]
    tfidf_matrix2.append(bert_embedding)

    i+=1


print (bert_embedding.size())
print("End of reading")
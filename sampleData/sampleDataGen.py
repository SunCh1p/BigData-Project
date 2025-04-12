#!/bin/python
##### ===========
##### Alex Tregub
##### 2025-04-11
##### Generates sample data according to in-file config / cmdline arguments?
##### v1.0.1
##### ===========
#### Imports
import random as r
from time import time as time
# import argparse
import namemaker # > pip3 install namemaker
import string
import pandas as pd
import sys



#### Setup
## Default vals
r.seed(time()) # SEED

TARGET_DATA_SIZE = -1 # CLIENT/ATTACKER DATA SIZE
MAX_MISMATCH = -1 # MAXIMUM USERS DIFFERENT BETWEEN CLIENT AND ATTACKER DATA
DISEASES = [
    "Influenza",
    "Strep Throat",
    "Sinus Infection",
    "Bronchitis",
    "Pneumonia",
    "Ear Infection",
    "Asthma",
    "Migraine",
    "Heart Disease",
    "Lung Cancer",
    "Diabetes"
] # Sample list of diseases to assign (11)
COLUMN_NAMES=["uid","name","age","gender","zip","disease"] # Keep order same, allows easy name changes


## Post-setup configuration
if (MAX_MISMATCH == -1): MAX_MISMATCH = int(0.1*TARGET_DATA_SIZE) # Set to default 10%
if (TARGET_DATA_SIZE == -1): TARGET_DATA_SIZE = 200_000 # Set to default 200k



#### Generate 'full' data, all entries being key-unique
maleNames = namemaker.make_name_set('male first names.txt')
femaleNames = namemaker.make_name_set('female first names.txt')
lastNames = namemaker.make_name_set('last names.txt')

# fullDataset = pd.DataFrame(columns=COLUMN_NAMES)
listDataset = []

for uid in range(0,(MAX_MISMATCH+TARGET_DATA_SIZE)):
    row = [uid] 

    # Full name string
    if r.random() < 0.5: 
        first = maleNames.make_name()
        gender = "M"
    else:
        first = femaleNames.make_name()
        gender = "F"

    second = r.choice(string.ascii_uppercase)

    third = lastNames.make_name()

    row.append(first+' '+second+' '+third)

    # print(row) # uid, name

    row.append(r.randint(1,100)) # + age

    row.append(gender) # + gender

    row.append((r.getrandbits(16)+10000)%99999) # + zip
    # if len(str((row[-1]))) != 5: # Ensures zip of size 5, sanity check during testing
    #     print("Error")
    #     print(row[-1])
    #     exit(0)

    # print(row)

    row.append(r.choice(DISEASES)) # + disease

    # print(row)
    # pd.concat(fullDataset,row)
    listDataset.append(row)

fullDataset = pd.DataFrame(listDataset,columns=COLUMN_NAMES) # Get full dataset as dataframe for manipulation
# print(fullDataset)



#### Split 'full' data into subsets - attacker, and client
clientData = fullDataset.sample(n=TARGET_DATA_SIZE, replace=False,random_state=r.randint(0,100_000_000))
attackerData = fullDataset.sample(n=TARGET_DATA_SIZE, replace=False,random_state=r.randint(0,100_000_000))

# print(clientData)
# print(attackerData)

clientData.sort_values("uid",inplace=True)
attackerData.sort_values("uid",inplace=True)



#### Remove target data from attacker's data
attackerData.drop(labels=COLUMN_NAMES[-1],axis=1,inplace=True) # Drop target association column

clientData_noUid = clientData.copy(deep=True)
attackerData_noUid = attackerData.copy(deep=True)

clientData_noUid.drop(labels="uid",axis=1,inplace=True)
attackerData_noUid.drop(labels="uid",axis=1,inplace=True)



#### Export
clientData.to_csv("./clientData_"+str(TARGET_DATA_SIZE)+"-"+str(MAX_MISMATCH)+".csv",index=False)
attackerData.to_csv("./attackerData_"+str(TARGET_DATA_SIZE)+"-"+str(MAX_MISMATCH)+".csv",index=False)

clientData_noUid.to_csv("./clientData_"+str(TARGET_DATA_SIZE)+"-"+str(MAX_MISMATCH)+"_nouid.csv",index=False)
attackerData_noUid.to_csv("./attackerData_"+str(TARGET_DATA_SIZE)+"-"+str(MAX_MISMATCH)+"_nouid.csv",index=False)

fullDataset.to_csv("./debug_fullDataset_"+str(TARGET_DATA_SIZE)+"-"+str(MAX_MISMATCH)+".csv",index=False)
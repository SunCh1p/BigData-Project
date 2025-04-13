#!/bin/python
##### ===========
##### Alex Tregub
##### 2025-04-12
##### Attempts to associate anonymized data with provided background knowledge. Assumes fixed data format,uids included
##### v1.0.0
##### ===========
#### Imports
import pandas as pd



#### Setup
BACKGROUND_DATASETS_PATH = "../sampleData/attackerData_1000-100.csv"
ANON_DATA_PATH = "../sampleData/clientData_1000-100.csv"
FULL_DATA_PATH = "../sampleData/debug_fullDataset_1000-100.csv"

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
# COLUMN_NAMES=["uid","name","age","gender","zip","disease"]

## Post-setup config
bkgdKnowledge = pd.read_csv(BACKGROUND_DATASETS_PATH)
anonData = pd.read_csv(ANON_DATA_PATH)
fullData = pd.read_csv(FULL_DATA_PATH)



#### (Inefficient) Association attack - get potential match list
assocData = [] # Stores data related to association attack
for index,targetUser in bkgdKnowledge.iterrows():
    # print(targetUser)
    targetName = targetUser["name"]
    targetUID = targetUser["uid"]
    targetPotentialDisease = [] # Preps list for potential matches

    for sIndex,searchUser in anonData.iterrows(): # Get potential diseases
        # if type(searchUser["age"]) == int: # If not-anonymized...
        #     if targetUser["age"] != searchUser["age"]: continue # DO NOT ADD
        # else: # NOTE: Anonymized as range list
        #     if searchUser["age"] == "discard": # If anonymized via discarding
        #         continue
        #     if (searchUser["age"][0] > searchUser["age"]) or (searchUser["age"][1] < searchUser["age"]):
        #         # eg. if search users age is out of range, discard
        #         continue

        # if searchUser["gender"] != targetUser["gender"] and searchUser["gender"] != "discard":
        #     continue # Not matched + not anonymized

        # if searchUser["zip"] != targetUser["zip"] and searchUser["zip"] != "discard":
        #     continue # Not matched + not anonymized

        # New range-based application
        if int(targetUser["age"]) != int(searchUser["age"]):
            # Not directly equal, if not anonymized - discard. If anonymized but out of range, discard.
            sampleRange = str(searchUser["age"]).split("-") # Split range string
            if len(sampleRange) != 2: 
                continue # If not a range, do not continue. Just not equal

            if (targetUser["age"] < int(sampleRange[0])) or (targetUser["age"] > int(sampleRange[1])):
                continue # Age out of range.

        # Gender is not anonymized
        if targetUser["gender"] != searchUser["gender"]:
            continue

        # Zip with range-based anonymization
        if int(targetUser["zip"]) != int(searchUser["zip"]):
            # Not directly equal, if not anonymized - discard. If anonymized but out of range, discard.
            sampleRange = str(searchUser["zip"]).split("-") # Split range string
            if len(sampleRange) != 2: 
                continue # If not a range, do not continue. Just not equal

            if (targetUser["zip"] < int(sampleRange[0])) or (targetUser["zip"] > int(sampleRange[1])):
                continue # Out of range.

        # Else if not rejected:
        targetPotentialDisease.append(searchUser["disease"])

    # Collect + Store stats in assoc data
    assocData.append(
        [targetName, targetPotentialDisease, targetUID]
    )



#### Check k-anonymity condition + probability of correct vs incorrect diagnosis guess
totalResultCount = [] # Len of targetPotentialDisease per user (k level)
intersectCount = 0 # Size of intersection between attacker and client dataset
correctProb = [] # Probability of correctness of most likely disease guess
notInDBFound = 0

for userStat in assocData:
    totalResultCount.append(len(userStat[1]))

    if totalResultCount[-1] == 0:
        notInDBFound += 1

    if (userStat[2] in list(anonData["uid"])):
        intersectCount += 1 

    if fullData.at[userStat[2],"uid"] == userStat[2]: # If data correlated by uid (should always be true)
        if len(userStat[1]) != 0:
            correctProb.append(
                userStat[1].count(fullData.at[userStat[2],"disease"])
                / len(userStat[1])
            )
        else: 
            correctProb.append(1/(len(DISEASES)+1)) # User known not in DB, no info gained. Can have 'uniform' chance of possible diseases or 'other'
            pass
        
        # print(fullData.at[userStat[2],"disease"])

# print(totalResultCount)
# print(intersectCount)
# print(notInDBFound)
# print(correctProb)



#### Report k-anonymity min/max/avg. levels, uses UID to verify if real result included.
filteredResultCount = [x for x in totalResultCount if x != 0]
print("Minimum k: "+str(min(filteredResultCount)))
print("Average k: "+str(sum(filteredResultCount)/len(filteredResultCount)))
print("Maximum k: "+str(max(filteredResultCount)))

print("Users in both datasets: "+str(intersectCount)+", Known not found in client data: "+str(notInDBFound))
print("Maximum probability of association: "+str(max(correctProb)))
print("Average probability of association: "+str(sum(correctProb)/len(correctProb)))
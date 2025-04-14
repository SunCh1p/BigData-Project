#!/bin/python
##### Alex Tregub, Connor Blaha (SunCh1p)
##### 2025-04-13
##### Multi-variable Adapted 'Glutton' Algorithm from previous implementation by Connor
##### v1.1.2
##### ===========
import pandas as pd
import random as r
from time import time as time
from math import sqrt



#### UTIL FUNCS
def getRealPoint(row):
    gender_encoded = 0 if row["gender"] == "M" else 1
    return [row["age"], gender_encoded, row["zip"]]


def distanceCalc(point1, point2):
    return sqrt(sum((a - b) ** 2 for a, b in zip(point1, point2)))

#### GLUTTON FUNCTION PROVIDED BY THIS FILE:
def glutton(data, k, QI=["age","gender","zip"]): # data ~ pandas dataframe, QI is 'sensitive' variables (fixed), k is the target k-level.
    # Will: 
    #   Get k-sized nearest neighbor greedy clusters
    #   Merge in remaining (<k) outlier nodes to existing clusters
    #   Anonymize clusters via min/max method
    #   Clean data for similar output to Mondrian func.

    r.seed(time())  # Seed RNG with current time

    dataSet = data.copy(deep=True)
    clusterList = []  # Will hold tuples of (centroid, points)

    while dataSet.shape[0] >= k:
        # Step 1: Start new cluster with a random point
        seedPointDF = dataSet.sample(n=1, replace=False, random_state=r.randint(0, 100_000_000))
        seedIndx = seedPointDF.index[0]
        dataSet.drop(seedIndx, inplace=True)

        clusterPoints = [seedPointDF.iloc[0]]
        centroid = getRealPoint(clusterPoints[0])

        # Step 2: Find k-1 nearest neighbors
        for _ in range(k - 1):
            minDist = float('inf')
            sIdx = None

            for i in range(dataSet.shape[0]):
                candidate = dataSet.iloc[i]
                dist = distanceCalc(centroid, getRealPoint(candidate))

                if dist < minDist:
                    minDist = dist
                    sIdx = i

            # Add the selected point to the cluster
            selectPoint = dataSet.iloc[sIdx]
            clusterPoints.append(selectPoint)
            dataSet.drop(dataSet.index[sIdx], inplace=True)

            # Update centroid (average of all current points in cluster)
            centroidPoints = [getRealPoint(p) for p in clusterPoints]
            centroid = [
                sum(dim) / len(centroidPoints) for dim in zip(*centroidPoints)
            ]

        # clusterList.append(clusterPoints)

        # Cluster list and centroid formed
        # print(centroid)
        clusterList.append([centroid, clusterPoints]) # Store as 'cluster'

    # print(clusterList)
    ## Cluster remaining outliers...
    for i in range(dataSet.shape[0]):
        testPoint = getRealPoint(dataSet.iloc[i])

        # Compare against datasets...
        compDist = float('inf')
        compIndex = -1
        for j,existClusters in enumerate(clusterList):
            if (
                distanceCalc(testPoint,existClusters[0]) < compDist
            ):
                compDist = distanceCalc(testPoint,existClusters[0])
                compIndex = j

        # Insert into closest cluster...
        clusterList[compIndex][1].append(dataSet.iloc[i])

        # Update centroid...
        centroidPoints = [getRealPoint(p) for p in clusterList[compIndex][1]]
        clusterList[compIndex][0] = [
            sum(dim) / len(centroidPoints) for dim in zip(*centroidPoints)
        ] # Update centroid

    # print(clusterList)

    ### Clusters formed, now need to anonymize data and convert into DB
    dataframeList = []
    for cluster in clusterList:
        clusterDf = pd.concat(cluster[1],axis=1)
        clusterDf = clusterDf.transpose()
        # for i in range(1,len(cluster[1])):
        # print(clusterDf)

        ## Anonymize data per-cluster
        minAge = clusterDf["age"].min()
        maxAge = clusterDf["age"].max()

        minGen = clusterDf["gender"].min()
        maxGen = clusterDf["gender"].max()

        # print(minGen)
        # print(maxGen)

        minZip = clusterDf["zip"].min()
        maxZip = clusterDf["zip"].max()

        for i,_ in clusterDf.iterrows():
            if minAge == maxAge:
                clusterDf.at[i,"age"] = minAge
            else:
                clusterDf.at[i,"age"] = f"{minAge}-{maxAge}"

            if minGen == maxGen:
                clusterDf.at[i,"gender"] = minGen
            else:
                clusterDf.at[i,"gender"] = "discard"

            if minZip == maxZip:
                clusterDf.at[i,"zip"] = minZip
            else:
                clusterDf.at[i,"zip"] = f"{minZip}-{maxZip}"

        dataframeList.append(clusterDf)

    finalDf = pd.concat(dataframeList)
    # print(finalDf)
    return finalDf


#### DEBUGGING / PREVENT EXECUTION IF NOT NEEDED
if __name__ == "__main__":
    # inputData = pd.read_csv("./sampleData/clientData_20-2.csv")

    # glutton(inputData,4)
    pass
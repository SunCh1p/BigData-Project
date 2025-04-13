import pandas as pd
import random


#Extraction function to extract needed columns from dataframe
def extractQI(data, QI):
    return list(zip(data['ID'], data[QI]))

#function to calculate centroids
def calCentroid(cluster):
    n = len(cluster)
    sum = 0
    for item in cluster:
        sum += item[1]
    return sum/n

#greedy glutton algorithm - assuming extraction has already occurred
#expected input data is list of pairs [[id, age], [id,age], .....]
def glutton(data, QI, k):
  #extract the column with the QI
  data_to_sort = extractQI(data, QI)
  
  #sort the ages from smallest the largest
  sorted_data = sorted(data_to_sort, key=lambda x: x[1])

  #create a list of lists[[]] for result
  resGluttons = []

  #add gluttons until sorted data is empty
  while len(sorted_data) > 0:
    #create the current glutton
    glutton = []

    #get size of sorted data
    size = len(sorted_data)

    #feed data at that index to the glutton from the smallest index
    glutton.append(sorted_data[0])

    #remove data at rIndex from sorted_data
    sorted_data.pop(0)

    #find k-1 nearest points forward if they exist using n^2 dumb approach
    while len(glutton) < k and len(sorted_data) > 0:
      #calculate centroid of glutton cluster
      gluttonCentroid = calCentroid(glutton)
      #find closest item to centroid 
      closestItem = [-1,-1]
      for item in sorted_data:
        #compare item to closest item
        #if closest item hasn't been filled yet, fill it
        if closestItem[0] == -1 and closestItem[1] == -1:
          closestItem = item
          #continue to next iteration
          continue
        #otherwise compare distnace to glutton, if item is closer than closest item
        #make that item the closest item
        elif(abs(item[1]-gluttonCentroid) < abs(closestItem[1]-gluttonCentroid)):
          closestItem = item
      #the closest item to the glutton
      glutton.append(closestItem)
      #remove closest item from the data(dumb way)
      sorted_data = [item for item in sorted_data if item[0] != closestItem[0]]
    #append glutton to resGluttons
    resGluttons.append(glutton)
  #check the last glutton in resGluttons and redistribute if necessary
  size = len(resGluttons)
  if(size == 0):
    return []
  lastGlutton = resGluttons[size-1]
  #if last glutton has points less than k
  if(len(lastGlutton) < k):
    resGluttons.pop()
    #redistribute points in closest cluster
    #get new size
    size = len(resGluttons)
    #distribute points to next max glutton
    for point in lastGlutton:
      resGluttons[size-1].append(point)

  #now that clustering is complete, anonymize the ages by using max and min
  for i in range(len(resGluttons)):
    #get current glutton
    glutton = resGluttons[i]
    size = len(glutton)
    #calculate qi range to anonymize data
    minQI = glutton[0][1]
    maxQI = glutton[size - 1][1]
    QIRange = f"{minQI}-{maxQI}"
    #modify glutton with anonymized data
    for j in range(size):
      glutton[j] = (glutton[j][0], QIRange)

  #take modified data from resGluttons and convert it back to a usable table in the format
  #given by the data.csv file
  #convert tuples to dictionary
  idToQI = {}
  for glutton in resGluttons:
    for point in glutton:
      id, QIRange = point
      idToQI[id] = QIRange
  data[QI] = data['ID'].map(idToQI)
  return data

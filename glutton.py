import pandas as pd

# Extraction function to extract needed columns from dataframe
def extractQI(data, QIs):
    return list(zip(data['ID'], data[QIs].values.tolist()))

# Function to calculate centroids for multiple QIs
def calCentroid(cluster):
    n = len(cluster)
    dim = len(cluster[0][1])
    sums = [0] * dim
    for item in cluster:
        for i in range(dim):
            sums[i] += item[1][i]
    return [s / n for s in sums]

# Euclidean distance between vectors
def euclidean_dist(p1, p2):
    return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** 0.5

# Glutton algorithm supporting multiple QIs
def glutton(data, QIs, k):
    data_to_sort = extractQI(data, QIs)
    sorted_data = sorted(data_to_sort, key=lambda x: x[1])
    resGluttons = []

    while len(sorted_data) > 0:
        glutton = []
        glutton.append(sorted_data[0])
        sorted_data.pop(0)

        while len(glutton) < k and len(sorted_data) > 0:
            gluttonCentroid = calCentroid(glutton)
            closestItem = None
            closestDist = float('inf')
            for item in sorted_data:
                dist = euclidean_dist(item[1], gluttonCentroid)
                if dist < closestDist:
                    closestItem = item
                    closestDist = dist
            glutton.append(closestItem)
            sorted_data = [item for item in sorted_data if item[0] != closestItem[0]]

        resGluttons.append(glutton)

    if len(resGluttons) > 0 and len(resGluttons[-1]) < k:
        lastGlutton = resGluttons.pop()
        for point in lastGlutton:
            resGluttons[-1].append(point)

    for i in range(len(resGluttons)):
        glutton = resGluttons[i]
        dim = len(glutton[0][1])
        mins = [min(point[1][i] for point in glutton) for i in range(dim)]
        maxs = [max(point[1][i] for point in glutton) for i in range(dim)]
        ranges = [f"{mins[i]}-{maxs[i]}" for i in range(dim)]
        for j in range(len(glutton)):
            glutton[j] = (glutton[j][0], ranges)

    idToQI = {}
    for glutton in resGluttons:
        for point in glutton:
            id, QIRanges = point
            idToQI[id] = QIRanges

    for i, QI in enumerate(QIs):
        data[QI] = data['ID'].map(lambda x: idToQI[x][i])

    return data

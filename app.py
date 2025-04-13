from flask import Flask, request, render_template
import pandas as pd
import os
import random
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#Mondrian algorithm
def mondrian(data, k):
    partition = []
    if len(data) <= 2 * k - 1:
        return [data]

    #sort by the predefined quasidenfier 
    data = data.sort_values(by=['Age'])
    #define partition point
    mid = len(data) // 2
    #split the sorted data left and right
    lhs = data[:mid]
    rhs = data[mid:]
    #splits each half until k anonymity condition is met
    partition.extend(mondrian(lhs, k))
    partition.extend(mondrian(rhs, k))
    return partition

#TODO: write extraction function so convert table data to form readable by glutton algorithm

def calCentroid(cluster):
    n = len(cluster)
    sum = 0
    for item in cluster:
        sum += item[1]
    return sum/n

#greedy glutton algorithm - assuming extraction has already occurred
#expected input data is list of pairs [[id, age], [id,age], .....]
def glutton(data, k):
    #sort the ages from smallest the largest
    sorted_data = sorted(data, key=lambda x: x[1])

    #create a list of lists[[]] for result
    resGluttons = []

    #add gluttons until sorted data is empty
    while len(sorted_data) > 0:
        #create the current glutton
        glutton = []

        #get size of sorted data
        size = len(sorted_data)

        #choose random index in sorted_data
        rIndex = random.randint(0, size-1)

        #feed data at that index to the glutton
        glutton.append(sorted_data[rIndex])

        #remove data at rIndex from sorted_data
        sorted_data.pop(rIndex)

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
                #otherwise, compare distance to glutton, if item is closer than closest item
                #make item the closestitem
                if(abs(item[1]-gluttonCentroid) < abs(closestItem[1]-gluttonCentroid)):
                    closestItem = item
            #feed closest item to the glutton
            glutton.append(closestItem)
            #remove closest item from the data (dumb way which iterates through whole list every time)
            sorted_data = [item for item in sorted_data if item[0] != closestItem[0]]

        #Append glutton to resGluttons
        resGluttons.append(glutton)

    #check the last glutton in resGluttons and redistribute if necessary
    size = len(resGluttons)
    lastGlutton = resGluttons[size-1]
    #if the last glutton is empty, pop it from resGluttons
    if(len(lastGlutton) == 0):
        resGluttons.pop()
    #otherwise check if its less than size of k
    elif(len(lastGlutton) < k):
        resGluttons.pop()
        #redistribute points in closest cluster
        for item in lastGlutton:
            #closest glutton
            closestGlutton = [-1,1]
            for glutton in resGluttons:
                if(closestGlutton[0][0] == -1):
                    closestGlutton = glutton
                    continue
                #otherwise
                centroidClosest = calCentroid(closestGlutton)
                centroidCurr = calCentroid(glutton)
                #TODO: finish the code distributing lastGlutton points to clusters

    return resGluttons

                






@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process():
    k = int(request.form['k'])
    file = request.files['file']

    if file.filename == '':
        return "No file selected."

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    df = pd.read_csv(filepath)

    partitions = mondrian(df.copy(), k)
    results = []

    for part in partitions:
        age_range = f"[{part['Age'].min()} - {part['Age'].max()}]"
        part['Age'] = age_range
        results.append(part)

    result_df = pd.concat(results, ignore_index=True)
    table_html = result_df.to_html(classes='styled-table', index=False)

    return render_template("index.html", table=table_html)

if __name__ == '__main__':
    app.run(debug=True)

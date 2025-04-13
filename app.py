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

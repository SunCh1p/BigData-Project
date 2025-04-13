from flask import Flask, request, render_template
import pandas as pd
import os
from werkzeug.utils import secure_filename
from Mondrian import mondrian
from glutton import glutton
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process():
    k = int(request.form['k'])
    algorithm = request.form['algorithm']
    file = request.files['file']

    if file.filename == '':
        return "No file selected."

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    df = pd.read_csv(filepath)

    if algorithm == 'mondrian':
        partitions = mondrian(df.copy(), k)
        results = []

        for part in partitions:
            age_range = f"[{part['Age'].min()} - {part['Age'].max()}]"
            part['Age'] = age_range
            results.append(part)

        result_df = pd.concat(results, ignore_index=True)

    elif algorithm == 'glutton':
        result_df = glutton(df.copy(), 'Age', k)

    else:
        return "Invalid algorithm selected."

    table_html = result_df.to_html(classes='styled-table', index=False)
    return render_template("index.html", table=table_html)

if __name__ == '__main__':
    app.run(debug=True)

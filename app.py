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
    outputPath = request.form['outpath']

    if file.filename == '':
        return "No file selected."

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    df = pd.read_csv(filepath)

    if algorithm == 'mondrian':
        partitions = mondrian(df.copy(), k, 0)
        results = []

        for part in partitions:
            # Handle min and max val anonymization:
            if part['age'].min() == part['age'].max():
                age_range = part['age'].max()
            else:
                age_range = f"{part['age'].min()}-{part['age'].max()}"

            if part['zip'].min() == part['zip'].max():
                zip_range = part['zip'].max()
            else:
                zip_range = f"{part['zip'].min()}-{part['zip'].max()}"

            if part['gender'].min() == part['gender'].max():
                gen_range = part['gender'].max()
            else:
                gen_range = "discard" # If not uniform M or F, discard instead
            
            # Update values for anonymization
            part['age'] = age_range
            part['zip'] = zip_range
            part['gender'] = gen_range
            results.append(part)

        result_df = pd.concat(results, ignore_index=True)

    elif algorithm == 'glutton':
        result_df = glutton(df.copy(), 'age', k)

    else:
        return "Invalid algorithm selected."

    table_html = result_df.to_html(classes='styled-table', index=False)
    
    result_df.to_csv(outputPath,index=False)

    return render_template("index.html", table=table_html)

if __name__ == '__main__':
    app.run(debug=True)

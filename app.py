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
    QIs = request.form.getlist('qis')
    file = request.files['file']

    if file.filename == '':
        return "No file selected."

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    df = pd.read_csv(filepath)

    if not QIs:
        return "No quasi-identifiers selected."

    if algorithm == 'mondrian':
        if len(QIs) > 1:
            return "Mondrian currently supports only one quasi-identifier."
        partitions = mondrian(df.copy(), k, QIs[0])
        results = []
        for part in partitions:
            col = QIs[0]
            range_value = f"[{part[col].min()} - {part[col].max()}]"
            part[col] = range_value
            results.append(part)
        result_df = pd.concat(results, ignore_index=True)

    elif algorithm == 'glutton':
        result_df = glutton(df.copy(), QIs, k)

    else:
        return "Invalid algorithm selected."

    table_html = result_df.to_html(classes='styled-table', index=False)
    return render_template("index.html", table=table_html)

if __name__ == '__main__':
    app.run(debug=True)

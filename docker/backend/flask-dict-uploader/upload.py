#!/usr/bin/python3
import os
from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER="/tmp/dicts"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploader', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename

@app.route('/remover/<fileid>', methods = ['GET'])
def delete_file(fileid):
    if request.method == 'GET':
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], fileid))
        return fileid

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

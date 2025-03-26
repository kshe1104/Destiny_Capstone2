# https://flask.palletsprojects.com/en/3.0.x/patterns/fileuploads/
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS
import uuid

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'json'}

# https://hwangtoemat.github.io/computer-science/2020-10-21-CORS/
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # https://dpdpwl.tistory.com/77
            uuid_test = uuid.uuid4()
            # str(uuid_test)[:6]
            random_file_name = str(uuid_test)[:6]
            random_file_name_json = random_file_name + '.json'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], random_file_name_json))
            # return redirect(url_for('download_file', name=filename))
            return random_file_name

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1219)
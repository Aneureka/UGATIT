from flask import Flask, request, render_template, send_from_directory, url_for
from flask_script import Manager, Shell
import requests
import json
import os
import uuid

from main import setup_for_web, eval_for_web
from utils import build_resp

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__, static_url_path='')

s2a_model = setup_for_web()


# config goes here
APP_NAME = 's2a'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
RESULT_FOLDER = 'results'
ALLOWED_EXTENSIONS = set(['.txt', '.pdf', '.png', '.jpg', '.jpeg'])

@app.route('/%s/ping' % APP_NAME, methods=['GET'])
def ping():
    return 'Ping successfully!'

@app.route('/%s/convert' % APP_NAME, methods=['POST'])
def convert():
    # upload
    if 'file' not in request.files:
        print('no photo detected')
        return 'No file detected', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    file_ext = os.path.splitext(file.filename)[-1]
    if file_ext not in ALLOWED_EXTENSIONS:
        return 'Unsupported file type', 415
    filename = '%s%s' % (str(uuid.uuid4()), file_ext)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    result_image_path = eval_for_web(s2a_model, file_path)
    return os.path.join(RESULT_FOLDER, filename)

if __name__ == "__main__":
    manager = Manager(app)
    manager.add_command("shell", Shell(make_context=dict(app=app)))
    manager.run()


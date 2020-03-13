from flask import Flask, request, render_template, send_from_directory, url_for
from flask_script import Manager, Shell
import requests
import json
import os
import uuid
import shutil

from main import setup_for_web, eval_for_web
from wechat import wechat_client
from utils import build_resp

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__, static_url_path='')

# config goes here
APP_NAME = 's2a'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
RESULT_FOLDER = 'results'
ALLOWED_EXTENSIONS = set(['.txt', '.pdf', '.png', '.jpg', '.jpeg'])
API_HOST=os.environ.get('API_HOST')
API_KEY=os.environ.get('API_KEY')
USE_API=True

if not USE_API:
    s2a_model = setup_for_web()

def check_image(image_path):
    resp = requests.post(
        url='https://api.weixin.qq.com/wxa/img_sec_check?access_token=%s' % wechat_client.access_token,
        files={
            'media': open(image_path, 'rb')
        }
    )
    # print(resp.status_code)
    if resp.status_code >= 300:
        return True
    data = json.loads(resp.text)
    # print(data)
    if data.get('errcode') == 87014:
        return False
    else:
        return True


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
    if check_image(file_path): 
        if USE_API:
            resp = requests.post(
                url=API_HOST,
                headers={
                    'accept': 'image/png',
                    'X-OVH-Api-Key': API_KEY,
                },
                files={
                    'file': open(file_path, 'rb')
                },
                timeout=240
            )
            if resp.status_code >= 300:
                return build_resp(code=1, msg='Failed to convert image.')
            else:
                with open(os.path.join(RESULT_FOLDER, filename), 'wb') as f:
                    f.write(resp.content)
        else:
            result_image_path = eval_for_web(s2a_model, file_path)
        return os.path.join(RESULT_FOLDER, filename)
    else:
        return build_resp(code=2, msg='Risky content detected.')


if __name__ == "__main__":
    manager = Manager(app)
    manager.add_command("shell", Shell(make_context=dict(app=app)))
    manager.run()


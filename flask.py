from flask import Flask, request, render_template
import requests
import json
import os


app = Flask(__name__)


# Some config goes here
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'


@app.route('/api/s2a/ping', methods=['GET'])
def ping():
    return 'Ping successfully!'

@app.route('/api/s2a/convert', methods=['POST'])
def convert():
    # TODO
    pass

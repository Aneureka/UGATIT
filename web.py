from flask import Flask, request, render_template
import requests
import json
import os
from main import setup_web, eval_web


# app = Flask(__name__)


# # Some config goes here
# app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/uploads'


# @app.route('/ping', methods=['GET'])
# def ping():
#     return 'Ping successfully!'

# @app.route('/convert', methods=['POST'])
# def convert():
#     # TODO
#     pass

def test():
    gan = setup_web()
    result_image_path = eval_web(gan, 'dataset/selfie2anime/testA/faceu_20170331221722.jpg')
    result_image_path = eval_web(gan, 'dataset/selfie2anime/testA/faceu_20170331221722.jpg')
    result_image_path = eval_web(gan, 'dataset/selfie2anime/testA/faceu_20170331221722.jpg')
    result_image_path = eval_web(gan, 'dataset/selfie2anime/testA/faceu_20170331221722.jpg')
    result_image_path = eval_web(gan, 'dataset/selfie2anime/testA/faceu_20170331221722.jpg')
    print(result_image_path)

if __name__ == "__main__":
    test()

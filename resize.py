from PIL import Image
import os
import sys
from tqdm import tqdm

paths = [
    'dataset/selfie2anime/testA',
    'dataset/selfie2anime/testB',
    'dataset/selfie2anime/trainA',
    'dataset/selfie2anime/trainB'
]


def resize():
    for path in tqdm(paths):
        dirs = os.listdir(path)
        for item in tqdm(dirs):
            file_path = os.path.join(path, item)
            if os.path.isfile(file_path):
                im = Image.open(file_path)
                f, _ = os.path.splitext(file_path)
                imResize = im.resize((256, 256), Image.ANTIALIAS)
                imResize.save(f + '.png', 'PNG')


resize()
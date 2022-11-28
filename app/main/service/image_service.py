import os, pathlib

from flask_restx import abort
from google.api_core import exceptions

from app.main.utils.image_helper import gcs_bucket


def serve_image(image):

    if os.environ.get('UPLOAD_STORAGE') == 'cloud':
        bucket = gcs_bucket()
        try:
            blob = bucket.blob(image)
            with blob.open('rb') as f:
                content = f.read()
        except exceptions.NotFound:
            blob = bucket.blob('default.jpg')
            with blob.open('rb') as f:
                content = f.read()

    elif os.environ.get('UPLOAD_STORAGE') == 'local':
        path = pathlib.Path().resolve()/"assets/images"
        try:
            with open(path/image, 'rb') as f:
                content = f.read()
        except:
            with open(path/"default.jpg", 'rb') as f:
                content = f.read()

    else:
        abort(500, "Can't determine storage location")
    
    return content
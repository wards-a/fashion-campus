import os

from flask import abort
from google.cloud import storage

def check_extension(image):
    ALLOWED_EXTENSIONS = {'jpg', 'png', 'webp'}
    try:
        extension = image.split('.')[1]
    except IndexError:
        abort(400, description="Invalid Extension")

    if extension not in ALLOWED_EXTENSIONS:
        abort(400)

    return "jpeg" if extension=="jpg" else extension

def serve_image(image):
    # get bucket name from env
    bucket_name = os.environ.get('BUCKET_NAME')

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob('product/'+image)

    with blob.open('rb') as f:
        content = f.read()

    return content
    
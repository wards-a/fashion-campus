from app.main.utils.image_helper import gcs_bucket
from google.api_core import exceptions


def serve_image(image):
    bucket = gcs_bucket()
    try:
        blob = bucket.blob(image)
        with blob.open('rb') as f:
            content = f.read()
    except exceptions.NotFound:
        blob = bucket.blob('default.jpg')
        with blob.open('rb') as f:
            content = f.read()
    return content
    
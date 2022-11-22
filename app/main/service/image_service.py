from app.main.utils.image_helper import allowed_file_media, gcs_bucket
from google.api_core import exceptions


def allowed_file(filename):
    return allowed_file_media(filename=filename)

def serve_image(image):
    bucket = gcs_bucket()
    try:
        blob = bucket.blob('product/'+image)
        with blob.open('rb') as f:
            content = f.read()
    except exceptions.NotFound:
        blob = bucket.blob('product/404notfound.jpg')
        with blob.open('rb') as f:
            content = f.read()
    return content
    
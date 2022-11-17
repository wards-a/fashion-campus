from app.main.utils.image_helper import allowed_file_media, gcs_bucket


def allowed_file(filename):
    return allowed_file_media(filename=filename)

def serve_image(image):
    bucket = gcs_bucket()
    blob = bucket.blob('product/'+image)
    with blob.open('rb') as f:
        content = f.read()
    return content
    
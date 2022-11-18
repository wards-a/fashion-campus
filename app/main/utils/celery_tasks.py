import base64, io

from werkzeug.datastructures import FileStorage
from google.cloud import storage

from app.main import celery
from app.main.utils.image_helper import gcs_bucket

@celery.task(name="app.main.utils.celery_tasks.upload_to_gcp")
def upload_to_gcp(data: list):
    file = data['file']
    path = data['path']
    if 'bucket' in data:
        bucket = gcs_bucket(data['bucket'])
    else:
        bucket = gcs_bucket()

    file['stream'] = base64.b64decode(file['stream'])
    file['stream'] = io.BytesIO(file['stream'])

    _file = FileStorage(**file)

    ## For slow upload speed
    storage.blob._DEFAULT_CHUNKSIZE = 2097152 # 1024 * 1024 B * 2 = 2 MB
    storage.blob._MAX_MULTIPART_SIZE = 2097152 # 2 MB

    blob = bucket.blob(path+_file.filename)
    blob.content_type = _file.mimetype
    blob.upload_from_file(_file)

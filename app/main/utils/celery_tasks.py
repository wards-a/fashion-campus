from google.cloud import storage

from app.main import celery
from app.main.utils.image_helper import gcs_bucket

@celery.task(name="app.main.utils.celery_tasks.upload_to_gcs")
def upload_to_gcs(file=None, bucket=None, path=None):
    if bucket:
        bucket = gcs_bucket(bucket)
    else:
        bucket = gcs_bucket()

    ## For slow upload speed
    storage.blob._DEFAULT_CHUNKSIZE = 2097152 # 1024 * 1024 B * 2 = 2 MB
    storage.blob._MAX_MULTIPART_SIZE = 2097152 # 2 MB

    blob = bucket.blob(path+file['filename'])
    blob.content_type = file['media_type']
    with blob.open('wb') as f:
        f.write(file['file'])

@celery.task(name="app.main.utils.celery_tasks.remove_from_gcs")
def remove_from_gcs(filename=None, bucket=None, path=None):
    if bucket:
        bucket = gcs_bucket(bucket)
    else:
        bucket = gcs_bucket()

    blob = bucket.blob(path+filename)
    blob.delete()
    

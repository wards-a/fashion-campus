import os, base64

from flask_restx import abort
from google.cloud import storage

    
ALLOWED_EXTENSIONS = {'jpg', 'png', 'svg', 'webp'}
ALLOWED_MIMETYPE = {'image/jpeg', 'image/png', 'image/svg', 'image/webp'}

def gcs_bucket(bucket: str = None):
    bucket_name = bucket if bucket else os.environ.get('BUCKET_NAME')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    return bucket

def allowed_file_media(filename, allowed_extensions: set = None) -> str:
    _allowed_extensions = ALLOWED_EXTENSIONS if not allowed_extensions else allowed_extensions
    try:
        extension = filename.split('.')[1]
    except IndexError:
        abort(400, "Invalid filename")

    if extension not in _allowed_extensions:
        abort(
            415,
            "Media types are not allowed, {0} are allowed.".format(_allowed_extensions)
        )
    return extension

def allowed_mimetype(mimetype, allowed_mimetype: set = None) -> str:
    _allowed_mimetype = ALLOWED_MIMETYPE if not allowed_mimetype else allowed_mimetype

    if mimetype not in _allowed_mimetype:
        abort(
            415,
            "Media types are not allowed, {0} are allowed.".format(_allowed_mimetype)
        )
    return mimetype

def generate_filename(name: str, media_type: str, condition: str = None, other: str = None):
    name_convention = [name]
    if condition:
        name_convention.append(condition)
    if other:
        name_convention.append(other)

    extension = media_type.split('/')[1]
    extension = 'jpg' if extension=='jpeg' else extension

    filename = '-'.join(name_convention)
    filename += "."+extension
    return filename

def b64str_to_byte(b64_string):
    ### decode base64 string image ###
    if 'data' in b64_string:
        b64_string_list = b64_string.split(',')
        result = base64.b64decode(b64_string_list[1])
    else:
        result = base64.b64decode(b64_string)

    return result
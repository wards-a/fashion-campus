import os

from flask_restx import abort
from google.cloud import storage

    
ALLOWED_EXTENSIONS = {'jpg', 'png', 'svg', 'webp'}

def gcs_bucket(bucket: str = None):
    bucket_name = bucket if bucket else os.environ.get('BUCKET_NAME')
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    return bucket

def allowed_file_media(filename=None, allowed_extensions: set = None) -> str:
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

def rename_filestorage(filestorage, name: str = None, condition: str = None, many: bool = False):
    name_convention = [name]
    if condition:
        name_convention.append(condition)
    if many:
        no = 1
        name_convention.append(str(no).zfill(2))
        for file in filestorage:
            extension = get_extension_filestorage(file)
            file.filename = '-'.join(name_convention)
            file.filename += "."+extension
            no += 1
            name_convention[-1] = str(no).zfill(2)

    else:
        extension = get_extension_filestorage(filestorage)
        filestorage.filename = '-'.join(name_convention)
        filestorage.filename += "."+extension
    return filestorage

def get_extension_filestorage(filestorage):
    mimetype = filestorage.mimetype
    mimetype = mimetype.split("/")
    if len(mimetype) > 1:
        extension = mimetype[-1]
        if extension == "jpeg":
            extension = "jpg"
        return extension
    else:
        return None
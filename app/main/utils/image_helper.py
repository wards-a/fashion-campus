import os, base64, pathlib, io

from PIL import Image
from flask_restx import abort
from google.cloud import storage

    
UPLOAD_FOLDER = pathlib.Path().resolve()/"assets/images"

ALLOWED_EXTENSIONS = {'jpg', 'png', 'svg', 'webp'}
ALLOWED_MIMETYPE = {'image/jpeg', 'image/png', 'image/svg', 'image/webp'}

def gcs_bucket():
    bucket_name = os.environ.get('BUCKET_NAME')
    if not bucket_name:
        abort(500, "Bucket name does not exists")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    return bucket

def allowed_file_media(filename, allowed_extensions: set = None) -> str:
    _allowed_extensions = ALLOWED_EXTENSIONS if not allowed_extensions else allowed_extensions
    try:
        extension = filename.split('.')[1]
    except IndexError:
        return {'message': 'Invalid filename'}, 400

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

    # extension = media_type.split('/')[1]
    # extension = 'jpg' if extension=='jpeg' else extension

    filename = '-'.join(name_convention)
    filename += ".jpg"
    return filename

def b64str_to_byte(b64_string):
    ### decode base64 string image ###
    if ',' in b64_string:
        b64_string_list = b64_string.split(',')
        result = base64.b64decode(b64_string_list[1])
    else:
        result = base64.b64decode(b64_string)

    return result

def resize_image(img_byte, basewidth=300, format='jpeg'):
        

    img_io = io.BytesIO()
    im = Image.open(io.BytesIO(img_byte))
    wpercent = (basewidth/float(im.size[0]))
    hsize = int((float(im.size[1])*float(wpercent)))
    im = im.resize((basewidth,hsize), Image.Resampling.LANCZOS)
    if format == 'jpeg':
        im.save(img_io, format=format, quality=100)
    else:
        im.save(img_io, format=format)

    img_io.seek(0)
    return img_io

def secure_name(name):
        ### replace some special characters with hyphens ###
        name = name.translate({ord(c): "-" for c in " `~!@#$%^*()_={}[]|\:;'\"<>,.?/"})
        name = name.replace('+', 'plus')
        name = name.replace('&', 'and')
        return name.lower()
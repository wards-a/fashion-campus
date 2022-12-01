"""
Universal Endpoint
To get or display picture in the platform

[Show Image]
- URL: /image/{image_name.extension}
- Method: GET
- Access URL last segment

- Response: image file

- Requirements:
    - Only image extension (jpg, jpeg, png)
    - or webp
"""
import io

from flask import send_file
from flask_restx import Namespace, Resource

from app.main.service.image_service import serve_image
from app.main.utils.image_helper import allowed_file_media


image_ns = Namespace("image")

@image_ns.route('/<image_name_extension>', endpoint="image")
@image_ns.doc(params={'image_name_extension': 'image_name.extension'})
class ImageController(Resource):
    def get(self, image_name_extension):
        extension = allowed_file_media(image_name_extension)
        mime_type = "jpeg" if extension=="jpg" else extension
        content =  serve_image(image_name_extension)
        return send_file(io.BytesIO(content), mimetype=f"image/{mime_type}")

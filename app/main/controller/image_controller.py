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

- NOTE:
    - For any error messages, should return (message=error, user already exists)
"""
import io

from flask import send_file
from flask_restx import Resource

from app.main.api_model.image_am import ImageApiModel
from app.main.service.image_service import allowed_file, serve_image


image_ns = ImageApiModel.api

@image_ns.route('/<image_extension>', endpoint="image")
class ImageController(Resource):
    def get(self, image_extension):
        extension = allowed_file(image_extension)
        extension = "jpeg" if extension=="jpg" else extension
        content =  serve_image(image_extension)
        return send_file(io.BytesIO(content), mimetype=f"image/{extension}")

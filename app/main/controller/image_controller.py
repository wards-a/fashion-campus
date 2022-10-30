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

from flask import Blueprint, send_file

from app.main.service.image_service import check_extension, serve_image

image_bp = Blueprint("image", __name__, url_prefix="/image/")

@image_bp.route("<image_extension>")
def image(image_extension):
    extension = check_extension(image_extension)
    content =  serve_image(image_extension)
    return send_file(io.BytesIO(content), mimetype=f"image/{extension}")



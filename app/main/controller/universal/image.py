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

from flask import Blueprint

image_bp = Blueprint("image", __name__, url_prefix="/image")

@image_bp.route("/<image_extension>", methods=["GET"])
def image(image_extension):
    return {"image": image_extension}, 200

from flask import Blueprint

image_bp = Blueprint("image", __name__, url_prefix="/image")

@image_bp.route("/<image_extension>", methods=["GET"])
def image(image_extension):
    return {"image": image_extension}, 200

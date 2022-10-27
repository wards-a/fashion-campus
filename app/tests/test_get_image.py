import pytest

from ..main import app

def test_successful_getImage():
    image = "jeans.jpg"

    response = app.test_client().get(f"/image/{image}")

    assert image == response.json["image"]
    assert 200 == response.status_code

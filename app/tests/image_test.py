import pytest

from app.main import app


@pytest.fixture()
def client():
    return app.test_client()

def test_successful_getImage(client):
    image = "jeans.jpg"

    response = client.get(f"/image/{image}")

    assert image == response.json["image"]
    assert 200 == response.status_code

def test_failed_getImage(client):
    """
    This test will fail due to an incorrect image extension.
    """
    images = ["shoe.gif", "t-shirt"]
    error_msg = "error, user already exists"
    for image in images:
        response = client.get(f"/image/{image}")

        assert error_msg == response.json["message"]
        assert 403 == response.status_code

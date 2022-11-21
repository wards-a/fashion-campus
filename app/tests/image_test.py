# import pytest

# from app.main import app


# @pytest.fixture()
# def client():
#     return app.test_client()

# def test_successful_getImage(client):
#     image = "Goodiebag-blacucream- g.jpg"
#     content_type = ['image/jpeg', 'image/png', 'image/svg', 'image/webp']

#     response = client.get(f"/image/{image}")

#     assert response.headers[0][1] in content_type
#     assert 200 == response.status_code

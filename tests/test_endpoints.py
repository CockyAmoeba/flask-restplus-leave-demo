import pytest


@pytest.mark.parametrize('http_method,http_path', (
        ('GET', '/api/v1/users/1'),
        ('GET', '/api/v1/users/test')
))
def test_unauthorized_user_access(http_method, http_path, flask_app_client):
    response = flask_app_client.open(method=http_method, path=http_path)
    assert response.status_code == 200
    assert set(response.json.keys()) >= {'email', 'username', 'first_name', 'last_name'}

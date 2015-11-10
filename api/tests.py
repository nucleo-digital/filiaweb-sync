import pytest

def test_view(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json
    assert response.json['message'] == 'hello'

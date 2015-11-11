"""
API basic tests.
To run just use:

DATABASE_URL=postgresql://user:password@host:port/database py.test -xs api/tests.py
"""
import os
import pytest
import json

def test_view(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json
    assert response.json['message'] == 'hello'

def test_process_csv(client):
    file_dir = "{}/csv_test.csv".format(os.getcwd())
    body_content = {
        'file_name': 'csv_text.csv',
        'file_text': open(file_dir, 'rb').read()}

    response = client.post('/process-csv', body_content)

    assert response.status_code == 200
    assert response.json

    assert response.json['json'][0]['email'] == 'lorem@ipsum.com'
    assert response.json['json'][0]['found'] == False
